#!/usr/bin/env python3
from __future__ import annotations

import unittest

from validate_public import PageParser, unresolved_render_markers


class RenderedSiteValidatorTests(unittest.TestCase):
    def parse_images(self, html: str) -> list[tuple[str, bool, str | None]]:
        parser = PageParser()
        parser.feed(html)
        return parser.images

    def test_minified_empty_alt_is_present(self) -> None:
        images = self.parse_images('<img src="/decorative.png" alt>')
        self.assertEqual(images, [("/decorative.png", True, None)])

    def test_explicit_empty_alt_is_present(self) -> None:
        images = self.parse_images('<img src="/decorative.png" alt="">')
        self.assertEqual(images, [("/decorative.png", True, "")])

    def test_missing_alt_is_still_detectable(self) -> None:
        images = self.parse_images('<img src="/meaningful.png">')
        self.assertEqual(images, [("/meaningful.png", False, None)])

    def test_json_closing_braces_are_not_template_markers(self) -> None:
        text = '<script type="application/ld+json">{"mainEntity":{"name":"Example"}}</script>'
        self.assertEqual(unresolved_render_markers(text), [])

    def test_unresolved_hugo_opening_delimiter_is_detected(self) -> None:
        self.assertEqual(unresolved_render_markers('<h1>{{ .Title }}</h1>'), ["{{"])

    def test_hugo_failure_tokens_are_detected(self) -> None:
        self.assertEqual(
            unresolved_render_markers('ZgotmplZ <no value> <nil>'),
            ["ZgotmplZ", "<no value>", "<nil>"],
        )


if __name__ == "__main__":
    unittest.main()
