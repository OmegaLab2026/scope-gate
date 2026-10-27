from __future__ import annotations

import unittest
from pathlib import Path

from validate_scope import (
    HEADINGS,
    ValidationError,
    validate_repository,
    validate_scope_text,
)


ROOT = Path(__file__).resolve().parents[1]


class RepositoryValidationTests(unittest.TestCase):
    def test_repository_matches_public_contract(self) -> None:
        validate_repository(ROOT)

    def test_scope_heading_order_is_frozen(self) -> None:
        reordered = "\n".join(f"## {heading}\n" for heading in reversed(HEADINGS))
        with self.assertRaises(ValidationError):
            validate_scope_text(reordered)

    def test_scope_rejects_extra_sections(self) -> None:
        text = (
            "# Scope: test\n\n"
            "- Version: V1.0\n"
            "- First created: 2026-10-27 15:00\n"
            "- Updated: 2026-10-27 15:00\n\n"
            + "\n".join(f"## {heading}\nResult.\n" for heading in HEADINGS)
            + "\n## Risks\nNone.\n"
        )
        with self.assertRaises(ValidationError):
            validate_scope_text(text)


if __name__ == "__main__":
    unittest.main()
