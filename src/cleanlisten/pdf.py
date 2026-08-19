from __future__ import annotations

from pathlib import Path

import pdfplumber


def extract_lines(path: str | Path) -> list[str]:
    """Extract non-empty text lines from a text-based PDF in page reading order."""
    pdf_path = Path(path)
    if not pdf_path.exists():
        raise FileNotFoundError(pdf_path)
    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(f"Expected a PDF file, got {pdf_path.name!r}")

    lines: list[str] = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            lines.extend(line.strip() for line in text.splitlines() if line.strip())
    return lines
