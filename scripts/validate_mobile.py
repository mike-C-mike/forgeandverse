#!/usr/bin/env python3
"""Headless mobile smoke test of the rendered Hugo site, without external networking.

Run after 'hugo --minify'. Requires Playwright and a local Chromium or Google Chrome.
It tests layout overflow, study artwork size, mobile navigation, and jump links.
"""
from __future__ import annotations

import functools
import http.server
import json
import os
from pathlib import Path
import shutil
import threading
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
OUT = ROOT / "mobile-audit"
PAGES = [
    "/", "/editions/", "/works/", "/roadmap/", "/journal/", "/series/",
    "/releases/", "/downloads/digital-forensics-intake-request/",
    "/disciplines/examiner-bench/", "/materials/", "/about/",
]
WIDTHS = (320, 360, 412, 768)


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, _format: str, *_args: object) -> None:
        pass


def main() -> int:
    if not (PUBLIC / "index.html").is_file():
        raise RuntimeError("Build the Hugo site first; public/index.html is missing.")
    OUT.mkdir(exist_ok=True)
    handler = functools.partial(QuietHandler, directory=str(PUBLIC))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_port}"
    problems: list[str] = []
    results = []
    browser_binary = next((shutil.which(name) for name in (
        "google-chrome", "google-chrome-stable", "chromium", "chromium-browser"
    ) if shutil.which(name)), None)
    try:
        with sync_playwright() as pw:
            kwargs = {"headless": True, "args": ["--no-sandbox"]}
            if browser_binary:
                kwargs["executable_path"] = browser_binary
            browser = pw.chromium.launch(**kwargs)
            try:
                for width in WIDTHS:
                    context = browser.new_context(
                        viewport={"width": width, "height": 850},
                        device_scale_factor=1, is_mobile=True, has_touch=True,
                    )
                    page = context.new_page()
                    for route in PAGES:
                        url = base + route.lstrip("/") if base.endswith("/") else base + route
                        try:
                            response = page.goto(url, wait_until="load", timeout=25000)
                            if not response or response.status >= 400:
                                problems.append(f"{width}px {route}: HTTP {getattr(response,'status','no response')}")
                                continue
                            info = page.evaluate("""() => {
                                const doc = document.documentElement;
                                const width = doc.clientWidth;
                                const scroll = doc.scrollWidth;
                                const offenders = [...document.querySelectorAll('body *')]
                                  .filter(el => {
                                    const cs = getComputedStyle(el), r = el.getBoundingClientRect();
                                    return cs.display !== 'none' && cs.visibility !== 'hidden'
                                      && r.width > 0 && (r.right > width + 3 || r.left < -3);
                                  })
                                  .slice(0, 8)
                                  .map(el => el.tagName.toLowerCase() + '.' + String(el.className).slice(0,80));
                                return {viewport: width, scrollWidth: scroll, offenders};
                            }""")
                            if info["scrollWidth"] > info["viewport"] + 2:
                                problems.append(
                                    f"{width}px {route}: horizontal overflow "
                                    f"{info['scrollWidth']-info['viewport']}px; {info['offenders']}"
                                )
                            results.append({"width": width, "path": route, **info})
                            if width == 412 and route == "/editions/":
                                page.locator("#edition-concepts").scroll_into_view_if_needed()
                                page.screenshot(path=str(OUT / "editions-concepts-412.png"))
                            if width == 412 and route == "/":
                                page.screenshot(path=str(OUT / "homepage-412.png"))
                        except Exception as exc:
                            problems.append(f"{width}px {route}: {type(exc).__name__}: {exc}")
                    context.close()

                phone = browser.new_context(
                    viewport={"width": 360, "height": 780}, is_mobile=True, has_touch=True
                )
                page = phone.new_page()
                page.goto(base + "/editions/", wait_until="load")
                gallery = page.locator("#edition-concepts .study-card")
                count = gallery.count()
                if count != 8:
                    problems.append(f"Expected 8 screen-only editorial cards; found {count}.")
                if count:
                    first = gallery.first
                    first.scroll_into_view_if_needed()
                    page.wait_for_function(
                        "() => { const img = document.querySelector('#edition-concepts .study-card img'); return img && img.complete && img.naturalWidth > 0; }",
                        timeout=8000,
                    )
                    metrics = first.evaluate("""card => {
                        const img = card.querySelector('img');
                        const r = card.getBoundingClientRect();
                        return {
                          width: r.width,
                          objectFit: img ? getComputedStyle(img).objectFit : '',
                          source: img ? img.getAttribute('src') : '',
                          imageNaturalWidth: img ? img.naturalWidth : 0
                        };
                    }""")
                    if metrics["width"] < 300:
                        problems.append(f"Concept card is only {metrics['width']:.0f}px at 360px viewport.")
                    if metrics["objectFit"] != "contain":
                        problems.append(f"Concept artwork uses {metrics['objectFit']}, not contain.")
                    if metrics["imageNaturalWidth"] == 0:
                        problems.append(f"Concept image failed to load: {metrics['source']}.")
                    page.screenshot(path=str(OUT / "editions-card-360.png"))
                jump = page.locator(".edition-room-jump a")
                if jump.count() != 4:
                    problems.append(f"Expected 4 profession jump links; found {jump.count()}.")
                else:
                    jump.last.click()
                    if not page.url.endswith("#edition-room-signal"):
                        problems.append("Cybersecurity profession jump did not navigate.")
                page.goto(base + "/", wait_until="load")
                menu = page.locator("[data-nav-toggle]")
                if not menu.is_visible():
                    problems.append("Phone navigation menu toggle is not visible.")
                else:
                    menu.click()
                    if menu.get_attribute("aria-expanded") != "true":
                        problems.append("Opening the navigation did not update aria-expanded.")
                    if not page.locator("[data-nav]").is_visible():
                        problems.append("Navigation links are not visible after opening menu.")
                    page.keyboard.press("Escape")
                    if menu.get_attribute("aria-expanded") != "false":
                        problems.append("Escape did not close navigation.")
                phone.close()
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()
    report = {"tested_paths": len(PAGES), "widths": WIDTHS, "checks": len(results),
              "issues": problems, "pages": results}
    (OUT / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Mobile audit: {len(results)} page/viewport checks, {len(problems)} issues.")
    for problem in problems:
        print("  ISSUE: " + problem)
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
