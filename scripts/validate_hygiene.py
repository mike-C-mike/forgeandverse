#!/usr/bin/env python3
from __future__ import annotations

import fnmatch
import subprocess
import sys
import tomllib
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []
WARNINGS: list[str] = []


def fail(message: str) -> None:
    ERRORS.append(message)


def warn(message: str) -> None:
    WARNINGS.append(message)


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def construct_mapping(loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"duplicate key: {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    construct_mapping,
)


def load_yaml_text(text: str, label: str) -> Any:
    try:
        return yaml.load(text, Loader=UniqueKeyLoader)
    except Exception as exc:
        fail(f"YAML parse failed for {label}: {exc}")
        return None


def load_yaml(path: Path) -> Any:
    try:
        return load_yaml_text(path.read_text(encoding="utf-8"), str(path.relative_to(ROOT)))
    except OSError as exc:
        fail(f"Unable to read {path.relative_to(ROOT)}: {exc}")
        return None


def front_matter(path: Path) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        fail(f"Unable to read {path.relative_to(ROOT)}: {exc}")
        return {}
    if not text.startswith("---\n"):
        fail(f"Missing YAML front matter: {path.relative_to(ROOT)}")
        return {}
    end = text.find("\n---", 4)
    if end < 0:
        fail(f"Unclosed YAML front matter: {path.relative_to(ROOT)}")
        return {}
    data = load_yaml_text(text[4:end], str(path.relative_to(ROOT)))
    if data is None:
        return {}
    if not isinstance(data, dict):
        fail(f"Front matter is not a mapping: {path.relative_to(ROOT)}")
        return {}
    return data


def tracked_files() -> list[str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT), "ls-files", "-z"],
            check=True,
            capture_output=True,
        )
        return [item.decode("utf-8") for item in result.stdout.split(b"\0") if item]
    except Exception:
        warn("Git tracked-file list unavailable; hygiene scan is using the working tree.")
        paths: list[str] = []
        for path in ROOT.rglob("*"):
            if not path.is_file() or ".git" in path.parts or ".forge-backups" in path.parts:
                continue
            paths.append(path.relative_to(ROOT).as_posix())
        return paths


def content_route_exists(route: str) -> bool:
    if not route.startswith("/"):
        return False
    clean = route.split("#", 1)[0].split("?", 1)[0].strip("/")
    if not clean:
        return True
    return (ROOT / "content" / f"{clean}.md").exists() or (ROOT / "content" / clean / "_index.md").exists()


def require_mapping_values(mapping: dict[str, Any], keys: tuple[str, ...], label: str) -> None:
    for key in keys:
        if mapping.get(key) in (None, "", []):
            fail(f"Missing required field '{key}' in {label}")


def check_versions() -> None:
    try:
        with (ROOT / "hugo.toml").open("rb") as handle:
            config = tomllib.load(handle)
    except Exception as exc:
        fail(f"hugo.toml parse failed: {exc}")
        return
    version = str((config.get("params") or {}).get("frameworkVersion") or "")
    if version != "19.0":
        fail(f"hugo.toml frameworkVersion must be 19.0, found {version!r}")
    expected_headings = {
        "README.md": "# Forge & Verse v19",
        "ITERATION-NOTES.md": "# Forge & Verse v19",
        "VALIDATION.md": "# Forge & Verse v19 Validation",
    }
    for name, heading in expected_headings.items():
        path = ROOT / name
        if not path.exists():
            fail(f"Missing versioned project file: {name}")
            continue
        first = path.read_text(encoding="utf-8").splitlines()[0] if path.stat().st_size else ""
        if first.strip() != heading:
            fail(f"Version heading mismatch in {name}: expected {heading!r}, found {first!r}")


def check_tracked_hygiene(files: list[str]) -> None:
    forbidden_patterns = (
        "public/*",
        "resources/_gen/*",
        "**/__pycache__/*",
        "**/*.pyc",
        "**/*.pyo",
        "hugo.exe",
        ".hugo_build.lock",
    )
    for item in files:
        normalized = item.replace("\\", "/")
        if not (ROOT / normalized).exists():
            continue
        if any(fnmatch.fnmatch(normalized, pattern) for pattern in forbidden_patterns):
            fail(f"Generated or local file is tracked: {normalized}")

    obsolete = (
        "content/downloads/verification-desk-card.md",
        "static/downloads/verification-desk-card-4x6.png",
        "static/downloads/verification-wallpaper-1920x1080.png",
        "static/downloads/digital-forensics-intake-request.docx",
        "static/downloads/digital-forensics-intake-request.pdf",
        "static/downloads/digital-forensics-intake-request.sha256",
        "static/downloads/forge-and-verse-digital-forensics-intake-kit-v1.1.zip",
        "static/downloads/forge-and-verse-digital-forensics-intake-kit-v1.1.sha256",
        "content/works/keeper-of-the-krapola.md",
        "content/works/a-hash-is-a-promise.md",
        "content/works/every-item-has-a-story.md",
        "content/works/the-hash-matched.md",
        "content/works/the-quiet-work-behind-the-case.md",
    )
    for item in obsolete:
        if (ROOT / item).exists():
            fail(f"Obsolete public file remains in the repository: {item}")


def check_ignore_rules() -> None:
    path = ROOT / ".gitignore"
    if not path.exists():
        fail("Missing .gitignore")
        return
    text = path.read_text(encoding="utf-8")
    required = (
        "/public/",
        "/resources/_gen/",
        "__pycache__/",
        "*.py[cod]",
        ".venv/",
        "/hugo.exe",
        "/.forge-backups/",
    )
    for token in required:
        if token not in text:
            fail(f".gitignore is missing required rule: {token}")


def check_yaml_files() -> None:
    for directory in (ROOT / "content", ROOT / "archetypes"):
        for path in sorted(directory.rglob("*.md")):
            front_matter(path)
    for directory in (ROOT / "data",):
        for path in sorted(directory.rglob("*")):
            if path.suffix.lower() in {".yaml", ".yml"}:
                load_yaml(path)


def check_physical_editions() -> None:
    states_data = load_yaml(ROOT / "data" / "edition-states.yaml") or []
    states = {item.get("slug") for item in states_data if isinstance(item, dict)}
    expected = {"in-studio", "proof-in-hand", "edition-approved", "available", "resting"}
    if states != expected:
        fail(f"Edition states must be exactly {sorted(expected)}")

    for path in sorted((ROOT / "content" / "works").glob("*.md")):
        if path.name == "_index.md":
            continue
        data = front_matter(path)
        if data.get("release_path") != "editions":
            continue
        edition = data.get("edition")
        label = str(path.relative_to(ROOT))
        if not isinstance(edition, dict) or not edition.get("enabled"):
            fail(f"Edition work requires edition.enabled: true: {label}")
            continue
        require_mapping_values(
            edition,
            ("state", "headline", "intended_room", "reading_distance", "edition_model", "study_url", "availability_note", "formats"),
            label,
        )
        state = edition.get("state")
        if state not in states:
            fail(f"Unknown edition state {state!r} in {label}")
        formats = edition.get("formats")
        if not isinstance(formats, list) or not formats:
            fail(f"Edition work requires at least one format direction: {label}")
        else:
            for index, item in enumerate(formats, start=1):
                if not isinstance(item, dict):
                    fail(f"Edition format {index} is not a mapping in {label}")
                    continue
                require_mapping_values(item, ("name", "status", "size_direction", "surface", "mount", "fit"), f"{label} format {index}")
        study_url = str(edition.get("study_url") or "")
        if study_url and not content_route_exists(study_url):
            fail(f"Edition study route does not exist in {label}: {study_url}")
        if state == "available":
            require_mapping_values(data, ("external_url", "partner_name", "fulfillment_note", "cta_label"), label)

    work_layout = ROOT / "layouts" / "works" / "single.html"
    if not work_layout.exists() or 'partial "edition-panel.html"' not in work_layout.read_text(encoding="utf-8"):
        fail("Work layout does not render the physical edition panel")
    head = ROOT / "layouts" / "partials" / "head.html"
    if not head.exists() or "edition-v19.css" not in head.read_text(encoding="utf-8"):
        fail("Head partial does not load the physical edition stylesheet")
    if not (ROOT / "assets" / "css" / "edition-v19.css").exists():
        fail("Missing assets/css/edition-v19.css")
    footer = ROOT / "layouts" / "partials" / "footer.html"
    if not footer.exists() or 'href="/editions/"' not in footer.read_text(encoding="utf-8"):
        fail("Footer does not link to the Editions archive")
    materials = ROOT / "layouts" / "materials" / "list.html"
    if not materials.exists() or 'href="/editions/"' not in materials.read_text(encoding="utf-8"):
        fail("Materials page does not link to the Editions archive")


def check_foundation_files() -> None:
    required = (
        ".editorconfig",
        ".github/workflows/site-validation.yml",
        "docs/REPOSITORY-HYGIENE.md",
        "docs/ARCHIVE-POLICY.md",
        "scripts/clean.ps1",
        "scripts/doctor.ps1",
    )
    for item in required:
        if not (ROOT / item).exists():
            fail(f"Missing v19 foundation file: {item}")


def main() -> int:
    files = tracked_files()
    check_versions()
    check_tracked_hygiene(files)
    check_ignore_rules()
    check_yaml_files()
    check_physical_editions()
    check_foundation_files()

    if WARNINGS:
        print("Hygiene warnings:")
        for item in WARNINGS:
            print(f"  - {item}")
    if ERRORS:
        print("Forge & Verse hygiene validation failed:")
        for item in ERRORS:
            print(f"  - {item}")
        return 1
    print("Forge & Verse repository hygiene passed.")
    print(f"  Tracked files reviewed: {len(files)}")
    print("  Framework version: 19.0")
    print("  Physical edition model: connected")
    return 0


if __name__ == "__main__":
    sys.exit(main())
