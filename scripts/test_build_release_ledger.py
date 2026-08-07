#!/usr/bin/env python3
from __future__ import annotations

import unittest
from pathlib import Path

from build_release_ledger import canonical_media_type


class ReleaseLedgerPortabilityTests(unittest.TestCase):
    def test_zip_is_canonical(self) -> None:
        self.assertEqual(canonical_media_type(Path("release.ZIP")), "application/zip")

    def test_pdf_is_canonical(self) -> None:
        self.assertEqual(canonical_media_type(Path("guide.pdf")), "application/pdf")

    def test_docx_is_canonical(self) -> None:
        self.assertEqual(
            canonical_media_type(Path("guide.docx")),
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

    def test_json_is_canonical(self) -> None:
        self.assertEqual(canonical_media_type(Path("manifest.json")), "application/json")

    def test_sha256_is_plain_text(self) -> None:
        self.assertEqual(canonical_media_type(Path("release.sha256")), "text/plain")

    def test_unknown_extension_is_binary(self) -> None:
        self.assertEqual(
            canonical_media_type(Path("artifact.unknown")),
            "application/octet-stream",
        )


if __name__ == "__main__":
    unittest.main()
