#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
import tomllib
import hashlib
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
STATIC = ROOT / "static"
ERRORS: list[str] = []
WARNINGS: list[str] = []


def fail(message: str) -> None: ERRORS.append(message)
def warn(message: str) -> None: WARNINGS.append(message)

def load_yaml(path: Path) -> Any:
    try: return yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"YAML parse failed: {path.relative_to(ROOT)}: {exc}")
        return None

def front_matter(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail(f"Missing YAML front matter: {path.relative_to(ROOT)}")
        return {}, text
    end = text.find("\n---", 4)
    if end < 0:
        fail(f"Unclosed YAML front matter: {path.relative_to(ROOT)}")
        return {}, text
    try: data = yaml.safe_load(text[4:end]) or {}
    except Exception as exc:
        fail(f"Front matter parse failed: {path.relative_to(ROOT)}: {exc}")
        return {}, text
    if not isinstance(data, dict):
        fail(f"Front matter is not a mapping: {path.relative_to(ROOT)}")
        data = {}
    return data, text[end+4:]

def static_target(value: str) -> Path | None:
    if not value or not value.startswith("/"): return None
    return STATIC / value.lstrip("/")

def require(data: dict[str, Any], keys: tuple[str, ...], path: Path) -> None:
    for key in keys:
        if data.get(key) in (None, "", []): fail(f"Missing required field '{key}': {path.relative_to(ROOT)}")

def check_static_reference(value: Any, label: str, path: Path) -> None:
    if not isinstance(value, str) or not value: return
    target = static_target(value)
    if target and not target.exists(): fail(f"Missing static {label} '{value}' referenced by {path.relative_to(ROOT)}")

def content_route_exists(route: str) -> bool:
    if not route.startswith("/") or route.startswith(("/images/", "/downloads/", "/icons/")): return True
    clean = route.split("#", 1)[0].split("?", 1)[0].strip("/")
    if not clean: return True
    direct = CONTENT / f"{clean}.md"
    index = CONTENT / clean / "_index.md"
    return direct.exists() or index.exists()

def main() -> int:
    try:
        with (ROOT / "hugo.toml").open("rb") as handle: config = tomllib.load(handle)
    except Exception as exc:
        fail(f"hugo.toml parse failed: {exc}")
        config = {}
    check_static_reference((config.get("params") or {}).get("defaultImage"), "default social image", ROOT / "hugo.toml")
    if not (CONTENT / "search" / "_index.md").exists(): fail("Missing search content page")
    if not (ROOT / "layouts" / "search" / "list.html").exists(): fail("Missing search layout")

    disciplines = load_yaml(ROOT / "data" / "disciplines.yaml") or []
    stages = load_yaml(ROOT / "data" / "study-stages.yaml") or []
    stage_steps = {item.get("step") for item in stages if isinstance(item, dict)}
    if stage_steps != set(range(1, 6)): fail("Study stages must define steps 1 through 5")
    discipline_slugs = {item.get("slug") for item in disciplines if isinstance(item, dict)}
    expected_paths = {"workbench", "workspace", "editions"}
    if len(discipline_slugs) != len(disciplines): fail("Discipline slugs are missing or duplicated")
    for item in disciplines:
        if not isinstance(item, dict):
            fail("Each discipline entry must be a mapping"); continue
        require(item, ("slug", "page", "name", "plain_name", "description", "paths"), ROOT / "data" / "disciplines.yaml")
        actual_paths = {entry.get("slug") for entry in item.get("paths", []) if isinstance(entry, dict)}
        if actual_paths != expected_paths: fail(f"Discipline '{item.get('slug')}' must define exactly: {sorted(expected_paths)}")
        if not (CONTENT / "disciplines" / f"{item.get('slug')}.md").exists(): fail(f"Missing discipline content page for {item.get('slug')}")

    reserved_front_matter = {"path"}
    counts = {"works": 0, "downloads": 0, "journal": 0, "roadmap": 0}
    routes: list[tuple[str, Path]] = []
    for path in sorted(CONTENT.rglob("*.md")):
        data, body = front_matter(path)
        for key in reserved_front_matter.intersection(data): fail(f"Reserved Hugo front matter key '{key}' used in {path.relative_to(ROOT)}")
        section = path.relative_to(CONTENT).parts[0]
        if path.name == "_index.md": continue
        if section in counts: counts[section] += 1
        if section == "works": require(data, ("title", "summary", "discipline", "release_path", "audience", "moment", "need", "format", "status", "rights"), path)
        elif section == "downloads":
            require(data, ("title", "summary", "discipline", "release_path", "audience", "moment", "need", "format", "status", "rights"), path)
            if not data.get("files") and not data.get("package_files"): fail(f"Download release needs files or package_files: {path.relative_to(ROOT)}")
        elif section == "journal": require(data, ("title", "date", "summary", "status", "journal_kind", "journal_kind_label"), path)
        elif section == "disciplines": require(data, ("title", "description", "discipline_slug"), path)
        elif section == "roadmap":
            require(data, ("title", "weight", "summary", "stage", "stage_step", "discipline_slug", "release_path", "format", "audience", "moment", "need", "visual", "design_test", "details"), path)
            if not isinstance(data.get("details"), list) or len(data.get("details", [])) < 3: fail(f"Study needs at least three details: {path.relative_to(ROOT)}")
            if data.get("stage_step") not in stage_steps: fail(f"Invalid stage_step in {path.relative_to(ROOT)}")
        discipline = data.get("discipline") or data.get("discipline_slug")
        if discipline and discipline not in discipline_slugs: fail(f"Unknown discipline '{discipline}' in {path.relative_to(ROOT)}")
        release_path = data.get("release_path")
        if release_path and release_path not in expected_paths: fail(f"Unknown release_path '{release_path}' in {path.relative_to(ROOT)}")
        for field in ("image", "preview_image", "file_url", "card_image", "hero_image", "bundle_url"): check_static_reference(data.get(field), field.replace("_", " "), path)
        for entry in data.get("files", []) or []:
            if not isinstance(entry, dict): fail(f"Invalid file entry in {path.relative_to(ROOT)}")
            else: check_static_reference(entry.get("url"), "download", path)
        for entry in data.get("package_files", []) or []:
            if not isinstance(entry, dict): fail(f"Invalid package file in {path.relative_to(ROOT)}")
            else:
                require(entry, ("label", "type", "url", "description"), path)
                check_static_reference(entry.get("url"), "package file", path)
        for entry in data.get("companion_previews", []) or []:
            if not isinstance(entry, dict): fail(f"Invalid companion preview in {path.relative_to(ROOT)}")
            else:
                require(entry, ("title", "image", "alt", "caption"), path)
                check_static_reference(entry.get("image"), "companion preview", path)
        for entry in data.get("adoption_steps", []) or []:
            if not isinstance(entry, dict): fail(f"Invalid adoption step in {path.relative_to(ROOT)}")
            else: require(entry, ("title", "text"), path)
        for entry in data.get("release_history", []) or []:
            if not isinstance(entry, dict): fail(f"Invalid release history entry in {path.relative_to(ROOT)}")
            else: require(entry, ("version", "date", "note"), path)
        for entry in data.get("preview_pages", []) or []:
            if not isinstance(entry, dict): fail(f"Invalid preview page in {path.relative_to(ROOT)}")
            else:
                require(entry, ("image", "alt", "caption"), path)
                check_static_reference(entry.get("image"), "preview page", path)
        for entry in data.get("prototype_images", []) or []:
            if not isinstance(entry, dict): fail(f"Invalid prototype image in {path.relative_to(ROOT)}")
            else:
                require(entry, ("image", "alt", "caption"), path)
                check_static_reference(entry.get("image"), "prototype image", path)
        for entry in data.get("gallery", []) or []:
            if not isinstance(entry, dict): fail(f"Invalid gallery image in {path.relative_to(ROOT)}")
            else:
                require(entry, ("image", "alt", "caption"), path)
                check_static_reference(entry.get("image"), "gallery image", path)
        for entry in data.get("prototype_source_files", []) or []:
            if not isinstance(entry, str) or not entry:
                fail(f"Invalid prototype source file entry in {path.relative_to(ROOT)}")
            else:
                prototype_target = ROOT / entry
                if not prototype_target.exists():
                    fail(f"Missing prototype source file '{entry}' referenced by {path.relative_to(ROOT)}")
                elif prototype_target.suffix.lower() == ".pdf" and not prototype_target.read_bytes().startswith(b"%PDF"):
                    fail(f"Prototype PDF signature is invalid: {prototype_target.relative_to(ROOT)}")
        if data.get("prototype_images"):
            require(data, ("prototype_title", "prototype_intro", "open_questions"), path)
            if not isinstance(data.get("open_questions"), list) or len(data.get("open_questions", [])) < 3:
                fail(f"Prototype study needs at least three open questions: {path.relative_to(ROOT)}")
        checksum_entries = data.get("checksums", []) or []
        for entry in checksum_entries:
            if not isinstance(entry, dict):
                fail(f"Invalid checksum entry in {path.relative_to(ROOT)}"); continue
            require(entry, ("label", "file", "algorithm", "value"), path)
            target = STATIC / "downloads" / str(entry.get("file", ""))
            if not target.exists():
                fail(f"Checksum target missing: {target.relative_to(ROOT)}")
            elif str(entry.get("algorithm", "")).upper() == "SHA-256":
                actual = hashlib.sha256(target.read_bytes()).hexdigest()
                if actual.lower() != str(entry.get("value", "")).lower(): fail(f"SHA-256 mismatch for {target.relative_to(ROOT)}")
        check_static_reference(data.get("manifest_url"), "checksum manifest", path)
        for route in re.findall(r"\]\((/[^)]+)\)", body): routes.append((route, path))
        related = data.get("related_work")
        if related: routes.append((related, path))
        related_release = data.get("related_release")
        if related_release: routes.append((related_release, path))
        related_journal = data.get("related_journal")
        if related_journal: routes.append((related_journal, path))

    for route, source in routes:
        if not content_route_exists(route): fail(f"Broken internal content link '{route}' in {source.relative_to(ROOT)}")

    import zipfile
    for artifact in sorted((STATIC / "downloads").rglob("*")):
        if not artifact.is_file():
            continue
        suffix = artifact.suffix.lower()
        if suffix == ".pdf" and not artifact.read_bytes().startswith(b"%PDF"):
            fail(f"PDF signature is invalid: {artifact.relative_to(ROOT)}")
        elif suffix == ".docx":
            try:
                with zipfile.ZipFile(artifact) as archive:
                    if "[Content_Types].xml" not in archive.namelist() or archive.testzip():
                        fail(f"DOCX archive is invalid: {artifact.relative_to(ROOT)}")
            except zipfile.BadZipFile:
                fail(f"DOCX archive is invalid: {artifact.relative_to(ROOT)}")
        elif suffix == ".zip":
            try:
                with zipfile.ZipFile(artifact) as archive:
                    bad = archive.testzip()
                    if bad: fail(f"ZIP archive is invalid at {bad}: {artifact.relative_to(ROOT)}")
            except zipfile.BadZipFile:
                fail(f"ZIP archive is invalid: {artifact.relative_to(ROOT)}")

    data_keys = {p.stem for p in (ROOT / "data").iterdir() if p.is_file() and p.suffix.lower() in {".yaml", ".yml", ".json", ".toml"}}
    for template in sorted((ROOT / "layouts").rglob("*.html")):
        text = template.read_text(encoding="utf-8")
        if text.count("{{") != text.count("}}"): fail(f"Unbalanced template delimiters: {template.relative_to(ROOT)}")
        for key in re.findall(r"hugo\.Data\.([A-Za-z0-9_]+)", text):
            if key not in data_keys:
                fail(f"Template references missing Hugo data key '{key}' in {template.relative_to(ROOT)}; use index for filenames containing hyphens")
    css = (ROOT / "assets" / "css" / "main.css").read_text(encoding="utf-8")
    if css.count("{") != css.count("}"): fail("Unbalanced CSS braces in assets/css/main.css")
    js = (ROOT / "assets" / "js" / "site.js").read_text(encoding="utf-8")
    if js.count("{") != js.count("}"): warn("JavaScript brace count differs; review assets/js/site.js manually")

    if WARNINGS:
        print("Warnings:")
        for item in WARNINGS: print(f"  - {item}")
    if ERRORS:
        print("Validation failed:")
        for item in ERRORS: print(f"  - {item}")
        return 1
    print("Forge & Verse validation passed.")
    print(f"  Disciplines: {len(disciplines)}")
    print(f"  Study stages: {len(stages)}")
    print(f"  Works: {counts['works']}")
    print(f"  Free works: {counts['downloads']}")
    print(f"  Journal pieces: {counts['journal']}")
    print(f"  Design studies: {counts['roadmap']}")
    print(f"  Content files: {len(list(CONTENT.rglob('*.md')))}")
    return 0

if __name__ == "__main__": sys.exit(main())
