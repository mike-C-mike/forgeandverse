from __future__ import annotations

import hashlib
import json
import mimetypes
import zipfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOWNLOADS = ROOT / "static" / "downloads"
KIT = DOWNLOADS / "intake-kit"
VERSION = "1.2"
BUNDLE_NAME = f"forge-and-verse-digital-forensics-intake-kit-v{VERSION}.zip"
BUNDLE_PATH = DOWNLOADS / BUNDLE_NAME
MANIFEST_PATH = DOWNLOADS / f"forge-and-verse-digital-forensics-intake-kit-v{VERSION}.sha256"
JSON_MANIFEST_PATH = DOWNLOADS / f"forge-and-verse-digital-forensics-intake-kit-v{VERSION}.json"

COMPONENTS = [
    "digital-forensics-intake-request.pdf",
    "digital-forensics-intake-request-fillable.pdf",
    "digital-forensics-intake-request.docx",
    "digital-forensics-intake-request-field-map.json",
    "digital-forensics-intake-requester-guide.pdf",
    "digital-forensics-intake-requester-guide.docx",
    "digital-forensics-intake-implementation-guide.pdf",
    "digital-forensics-intake-implementation-guide.docx",
    "README.txt",
    "RELEASE-NOTES.txt",
    "LICENSE.txt",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def media_type(path: Path) -> str:
    known = {
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".sha256": "text/plain",
    }
    return known.get(path.suffix.lower()) or mimetypes.guess_type(path.name)[0] or "application/octet-stream"


def file_record(path: Path, public_path: str) -> dict[str, object]:
    return {
        "path": public_path,
        "filename": path.name,
        "bytes": path.stat().st_size,
        "media_type": media_type(path),
        "sha256": sha256(path),
    }


def main() -> None:
    missing = [name for name in COMPONENTS if not (KIT / name).exists()]
    if missing:
        raise SystemExit(f"Missing intake kit files: {', '.join(missing)}")

    component_lines = [f"{sha256(KIT / name)}  {name}" for name in COMPONENTS]
    internal_manifest = KIT / "SHA256SUMS.txt"
    internal_manifest.write_text("\n".join(component_lines) + "\n", encoding="utf-8")

    bundle_files = COMPONENTS + ["SHA256SUMS.txt"]
    if BUNDLE_PATH.exists():
        BUNDLE_PATH.unlink()
    with zipfile.ZipFile(BUNDLE_PATH, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        folder = f"forge-and-verse-digital-forensics-intake-kit-v{VERSION}"
        for name in bundle_files:
            archive.write(KIT / name, arcname=f"{folder}/{name}")

    with zipfile.ZipFile(BUNDLE_PATH) as archive:
        bad = archive.testzip()
        if bad:
            raise SystemExit(f"Bundle ZIP failed integrity check at {bad}")

    external_lines = [f"{sha256(KIT / name)}  intake-kit/{name}" for name in COMPONENTS] + [
        f"{sha256(internal_manifest)}  intake-kit/SHA256SUMS.txt",
        f"{sha256(BUNDLE_PATH)}  {BUNDLE_NAME}",
    ]
    MANIFEST_PATH.write_text("\n".join(external_lines) + "\n", encoding="utf-8")

    json_manifest = {
        "name": "Forge & Verse Digital Forensics Intake Kit",
        "version": VERSION,
        "updated": date(2026, 8, 5).isoformat(),
        "page": "/downloads/digital-forensics-intake-request/",
        "bundle": file_record(BUNDLE_PATH, f"/downloads/{BUNDLE_NAME}"),
        "files": [file_record(KIT / name, f"/downloads/intake-kit/{name}") for name in COMPONENTS],
        "checksum_manifest": file_record(MANIFEST_PATH, f"/downloads/{MANIFEST_PATH.name}"),
        "form_fields": {
            "count": 105,
            "text": 61,
            "checkbox": 44,
            "data_submission": False,
            "javascript": False,
        },
    }
    JSON_MANIFEST_PATH.write_text(json.dumps(json_manifest, indent=2) + "\n", encoding="utf-8")

    print(BUNDLE_PATH)
    print(MANIFEST_PATH)
    print(JSON_MANIFEST_PATH)


if __name__ == "__main__":
    main()
