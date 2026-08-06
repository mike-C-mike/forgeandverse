#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import mimetypes
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
STATIC = ROOT / "static"
OUTPUT_DIR = STATIC / "releases"
JSON_PATH = OUTPUT_DIR / "forge-and-verse-release-ledger.json"
HASH_PATH = OUTPUT_DIR / "forge-and-verse-release-ledger.sha256"


def read_front_matter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"Missing YAML front matter: {path}")
    end = text.find("\n---", 4)
    if end < 0:
        raise ValueError(f"Unclosed YAML front matter: {path}")
    data = yaml.safe_load(text[4:end]) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Front matter is not a mapping: {path}")
    return data


def iso(value: Any) -> str:
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    return str(value or "")


def static_file(url: str) -> Path:
    if not url.startswith("/"):
        raise ValueError(f"Expected root-relative static URL, received: {url}")
    path = STATIC / url.lstrip("/")
    if not path.is_file():
        raise FileNotFoundError(f"Published file does not exist: {path.relative_to(ROOT)}")
    return path


def file_record(url: str, *, label: str, file_type: str = "") -> dict[str, Any]:
    path = static_file(url)
    media_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return {
        "label": label,
        "type": file_type or path.suffix.lstrip(".").upper(),
        "path": url,
        "bytes": path.stat().st_size,
        "media_type": media_type,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def unique_file_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    found: set[str] = set()
    result: list[dict[str, Any]] = []
    for record in records:
        path = record["path"]
        if path in found:
            continue
        found.add(path)
        result.append(record)
    return result


def route_for(path: Path) -> str:
    section = path.parent.name
    return f"/{section}/{path.stem}/"


def open_release_entry(path: Path, data: dict[str, Any]) -> dict[str, Any]:
    files: list[dict[str, Any]] = []
    bundle_url = str(data.get("bundle_url") or "")
    if bundle_url:
        files.append(file_record(bundle_url, label=str(data.get("bundle_label") or "Complete release"), file_type="ZIP bundle"))
    for item in data.get("package_files") or data.get("files") or []:
        if not isinstance(item, dict) or not item.get("url"):
            continue
        files.append(file_record(str(item["url"]), label=str(item.get("label") or Path(str(item["url"])).name), file_type=str(item.get("type") or "")))
    for label, key, kind in (
        ("Checksum manifest", "manifest_url", "SHA-256 manifest"),
        ("Release manifest", "release_manifest_url", "JSON manifest"),
    ):
        url = str(data.get(key) or "")
        if url:
            files.append(file_record(url, label=label, file_type=kind))
    files = unique_file_records(files)
    primary = next((record for record in files if record["path"] == bundle_url), files[0] if files else None)
    return {
        "id": path.stem,
        "title": str(data.get("title") or path.stem),
        "kind": "open-release",
        "status": "released",
        "version": str(data.get("version") or ""),
        "updated": iso(data.get("updated")),
        "page": route_for(path),
        "discipline": str(data.get("discipline") or ""),
        "release_path": str(data.get("release_path") or ""),
        "audience": str(data.get("audience") or ""),
        "moment": str(data.get("moment") or ""),
        "need": str(data.get("need") or ""),
        "format": str(data.get("format_label") or data.get("format") or ""),
        "summary": str(data.get("summary") or ""),
        "permission": str(data.get("license_note") or data.get("usage") or ""),
        "primary_download": primary,
        "files": files,
    }


def field_proof_entry(path: Path, data: dict[str, Any]) -> dict[str, Any]:
    files: list[dict[str, Any]] = []
    bundle_url = str(data.get("proof_bundle_url") or "")
    if bundle_url:
        files.append(file_record(bundle_url, label=str(data.get("proof_bundle_label") or "Complete field proof"), file_type="ZIP bundle"))
    for item in data.get("proof_files") or []:
        if not isinstance(item, dict) or not item.get("url"):
            continue
        files.append(file_record(str(item["url"]), label=str(item.get("label") or Path(str(item["url"])).name), file_type=str(item.get("type") or "")))
    files = unique_file_records(files)
    primary = next((record for record in files if record["path"] == bundle_url), files[0] if files else None)
    return {
        "id": path.stem,
        "title": str(data.get("title") or path.stem),
        "kind": "field-proof",
        "status": "testing",
        "version": str(data.get("proof_version") or ""),
        "updated": iso(data.get("proof_updated")),
        "page": f"{route_for(path)}#field-proof",
        "discipline": str(data.get("discipline_slug") or ""),
        "release_path": str(data.get("release_path") or ""),
        "audience": str(data.get("audience") or ""),
        "moment": str(data.get("moment") or ""),
        "need": str(data.get("need") or ""),
        "format": str(data.get("format") or ""),
        "summary": str(data.get("summary") or ""),
        "test": str(data.get("design_test") or ""),
        "notice": str(data.get("proof_notice") or ""),
        "primary_download": primary,
        "files": files,
    }


def build() -> tuple[Path, Path]:
    entries: list[dict[str, Any]] = []
    for path in sorted((CONTENT / "downloads").glob("*.md")):
        if path.name == "_index.md":
            continue
        entries.append(open_release_entry(path, read_front_matter(path)))
    for path in sorted((CONTENT / "roadmap").glob("*.md")):
        if path.name == "_index.md":
            continue
        data = read_front_matter(path)
        if data.get("proof_available"):
            entries.append(field_proof_entry(path, data))
    entries.sort(key=lambda entry: (entry["kind"], entry["title"].lower()))
    dates = [entry["updated"] for entry in entries if entry.get("updated")]
    ledger = {
        "schema": "https://forgeandverse.com/schemas/release-ledger-v1",
        "schema_version": 1,
        "studio": "Forge & Verse",
        "site": "https://forgeandverse.com",
        "updated": max(dates) if dates else "",
        "entry_count": len(entries),
        "entries": entries,
    }
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    manifest_records: dict[str, str] = {}
    for entry in entries:
        for record in entry["files"]:
            manifest_records[record["path"].lstrip("/")] = record["sha256"]
    manifest_records["releases/forge-and-verse-release-ledger.json"] = hashlib.sha256(JSON_PATH.read_bytes()).hexdigest()
    lines = [f"{digest}  {path}" for path, digest in sorted(manifest_records.items())]
    HASH_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return JSON_PATH, HASH_PATH


if __name__ == "__main__":
    json_path, hash_path = build()
    print(f"Wrote {json_path.relative_to(ROOT)}")
    print(f"Wrote {hash_path.relative_to(ROOT)}")
