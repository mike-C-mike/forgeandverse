#!/usr/bin/env python3
from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
ERRORS: list[str] = []
WARNINGS: list[str] = []


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, str]] = []
        self.ids: list[str] = []
        self.title_parts: list[str] = []
        self.in_title = False
        self.description = ""
        self.html_lang = ""
        self.main_count = 0
        # src, whether the alt attribute exists, parsed alt value.
        # HTML5 minifiers may legally serialize alt="" as a valueless `alt`
        # attribute, which HTMLParser represents as ("alt", None).
        self.images: list[tuple[str, bool, str | None]] = []

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = dict(attrs_list)
        if tag == "html":
            self.html_lang = attrs.get("lang") or ""
        if tag == "title":
            self.in_title = True
        if tag == "main":
            self.main_count += 1
        if tag == "meta" and attrs.get("name") == "description":
            self.description = attrs.get("content") or ""
        if "id" in attrs and attrs["id"]:
            self.ids.append(attrs["id"] or "")
        if tag in {"a", "link"} and attrs.get("href"):
            self.links.append((tag, attrs["href"] or ""))
        if tag in {"img", "script", "source"} and attrs.get("src"):
            self.links.append((tag, attrs["src"] or ""))
        if tag == "img":
            alt_present = any(name.lower() == "alt" for name, _ in attrs_list)
            self.images.append((attrs.get("src") or "", alt_present, attrs.get("alt")))

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)


def unresolved_render_markers(text: str) -> list[str]:
    """Return markers that strongly indicate a failed Hugo render.

    A bare `}}` is intentionally not treated as an error because valid JSON-LD
    frequently contains adjacent closing braces. Any unresolved Hugo template
    expression will still contain its opening `{{` delimiter.
    """
    markers = [marker for marker in ("ZgotmplZ", "<no value>", "<nil>") if marker in text]
    if "{{" in text:
        markers.append("{{")
    return markers


def target_for_url(source: Path, value: str) -> tuple[Path | None, str]:
    value = value.strip()
    if not value or value.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
        return None, ""
    parsed = urlparse(value)
    if parsed.scheme or parsed.netloc:
        return None, parsed.fragment
    path = unquote(parsed.path)
    fragment = parsed.fragment
    if not path:
        return source, fragment
    if path.startswith("/"):
        target = PUBLIC / path.lstrip("/")
    else:
        target = source.parent / path
    if path.endswith("/"):
        target = target / "index.html"
    elif target.suffix == "":
        if target.is_dir() or not target.exists():
            target = target / "index.html"
    return target.resolve(), fragment


def main() -> int:
    if not PUBLIC.exists():
        print("Rendered-site validation skipped: public/ does not exist.")
        return 0

    html_files = sorted(PUBLIC.rglob("*.html"))
    if not html_files:
        ERRORS.append("No rendered HTML files found in public/.")

    parsed_pages: dict[Path, PageParser] = {}
    for page in html_files:
        text = page.read_text(encoding="utf-8", errors="replace")
        for marker in unresolved_render_markers(text):
            ERRORS.append(f"Unresolved render marker '{marker}' in {page.relative_to(PUBLIC)}")
        parser = PageParser()
        try:
            parser.feed(text)
        except Exception as exc:
            ERRORS.append(f"HTML parse failed for {page.relative_to(PUBLIC)}: {exc}")
            continue
        parsed_pages[page.resolve()] = parser
        title = "".join(parser.title_parts).strip()
        if not title:
            ERRORS.append(f"Missing title in {page.relative_to(PUBLIC)}")
        if not parser.description:
            WARNINGS.append(f"Missing meta description in {page.relative_to(PUBLIC)}")
        if parser.html_lang.lower() != "en":
            WARNINGS.append(f"Unexpected or missing html lang in {page.relative_to(PUBLIC)}")
        if parser.main_count != 1:
            ERRORS.append(f"Expected one main element in {page.relative_to(PUBLIC)}, found {parser.main_count}")
        duplicates = sorted({item for item in parser.ids if parser.ids.count(item) > 1})
        for item in duplicates:
            ERRORS.append(f"Duplicate id '{item}' in {page.relative_to(PUBLIC)}")
        for src, alt_present, _alt_value in parser.images:
            if not alt_present:
                ERRORS.append(f"Image missing alt attribute in {page.relative_to(PUBLIC)}: {src}")

    for source, parser in parsed_pages.items():
        for tag, value in parser.links:
            target, fragment = target_for_url(source, value)
            if target is None:
                continue
            try:
                target.relative_to(PUBLIC.resolve())
            except ValueError:
                ERRORS.append(f"Reference escapes public/: {value} in {source.relative_to(PUBLIC)}")
                continue
            if not target.exists():
                ERRORS.append(f"Broken {tag} reference '{value}' in {source.relative_to(PUBLIC)}")
                continue
            if fragment and target.suffix.lower() == ".html":
                target_parser = parsed_pages.get(target.resolve())
                if target_parser and fragment not in target_parser.ids:
                    WARNINGS.append(
                        f"Missing fragment '#{fragment}' in {target.relative_to(PUBLIC)} "
                        f"linked from {source.relative_to(PUBLIC)}"
                    )

    if WARNINGS:
        print("Rendered-site warnings:")
        for item in WARNINGS:
            print(f"  - {item}")
    if ERRORS:
        print("Rendered-site validation failed:")
        for item in ERRORS:
            print(f"  - {item}")
        return 1
    print("Rendered-site validation passed.")
    print(f"  HTML pages: {len(html_files)}")
    print(f"  Static files: {len([p for p in PUBLIC.rglob('*') if p.is_file()])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
