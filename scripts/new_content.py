from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
ARCHETYPES = ROOT / "archetypes"
SECTIONS = {"works", "downloads", "journal", "roadmap"}
DISCIPLINES = {"examiner-bench", "evidence-room", "watch", "signal"}
RELEASE_PATHS = {"workbench", "workspace", "editions"}


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a Forge & Verse content draft from an archetype.")
    parser.add_argument("section", choices=sorted(SECTIONS))
    parser.add_argument("title")
    parser.add_argument("--discipline", choices=sorted(DISCIPLINES), default="examiner-bench")
    parser.add_argument("--release-path", choices=sorted(RELEASE_PATHS), default="workbench")
    parser.add_argument("--slug")
    args = parser.parse_args()

    slug = slugify(args.slug or args.title)
    if not slug:
        raise SystemExit("The title did not produce a usable slug.")

    archetype = ARCHETYPES / f"{args.section}.md"
    target = CONTENT / args.section / f"{slug}.md"
    if not archetype.exists():
        raise SystemExit(f"Missing archetype: {archetype}")
    if target.exists():
        raise SystemExit(f"Refusing to overwrite: {target}")

    text = archetype.read_text(encoding="utf-8")
    safe_title = args.title.replace(chr(34), chr(39))
    text = re.sub(r'(?m)^title:.*$', f'title: "{safe_title}"', text, count=1)
    text = re.sub(r"(?m)^discipline(_slug)?:.*$", lambda m: f"discipline{m.group(1) or ''}: {args.discipline}", text)
    text = re.sub(r"(?m)^release_path:.*$", f"release_path: {args.release_path}", text)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    print(target.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
