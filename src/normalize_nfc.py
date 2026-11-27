#!/usr/bin/env python3
"""
Normalize Bengali OCR dataset transcriptions using Unicode NFC.

Inputs:
    data/processed/manual_reference/dataset.jsonl
    data/processed/model_assisted/dataset.jsonl

Outputs:
    data/processed/normalized_nfc/

Only the text field is normalized. All other fields are preserved.
Original datasets are never modified.
"""

import json
import shutil
import unicodedata
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED = PROJECT_ROOT / "data" / "processed"
OUTPUT_ROOT = PROCESSED / "normalized_nfc"

COLLECTIONS = {
    "manual_reference": PROCESSED / "manual_reference" / "dataset.jsonl",
    "model_assisted": PROCESSED / "model_assisted" / "dataset.jsonl",
}


def normalize_collection(name, source, output):
    total = 0
    changed = 0

    with source.open("r", encoding="utf-8") as src, \
         output.open("x", encoding="utf-8") as dst:

        for line_number, line in enumerate(src, 1):
            record = json.loads(line)

            if not isinstance(record, dict):
                raise ValueError(
                    f"{name}, line {line_number}: expected JSON object"
                )

            original_text = record.get("text")

            if not isinstance(original_text, str):
                raise ValueError(
                    f"{name}, line {line_number}: invalid text field"
                )

            normalized_text = unicodedata.normalize("NFC", original_text)

            if normalized_text != original_text:
                changed += 1

            record["text"] = normalized_text

            if not unicodedata.is_normalized("NFC", normalized_text):
                raise ValueError(
                    f"{name}, line {line_number}: NFC verification failed"
                )

            dst.write(json.dumps(record, ensure_ascii=False) + "\n")
            total += 1

    return total, changed


def main():
    if OUTPUT_ROOT.exists():
        raise SystemExit(
            f"STOP: output already exists: {OUTPUT_ROOT}\n"
            "No files have been changed."
        )

    for name, source in COLLECTIONS.items():
        if not source.is_file():
            raise SystemExit(f"Missing input file: {source}")

    OUTPUT_ROOT.mkdir(parents=True)

    report = [
        "# Bengali OCR Dataset — NFC Normalization Report",
        "",
        "- Method: Python unicodedata.normalize('NFC', text)",
        "- Only the text field was normalized.",
        "- Original datasets were not modified.",
        "- No OCR or spelling correction was performed.",
        "",
    ]

    try:
        for name, source in COLLECTIONS.items():
            output_dir = OUTPUT_ROOT / name
            output_dir.mkdir()

            output = output_dir / "dataset.jsonl"
            total, changed = normalize_collection(name, source, output)

            report.extend([
                f"## {name}",
                f"- Records: {total}",
                f"- Text fields changed: {changed}",
                f"- Text fields unchanged: {total - changed}",
                f"- Output: `{output.relative_to(PROJECT_ROOT)}`",
                "",
            ])

        report.extend([
            "## Validation",
            "- Every output line was parsed as JSON during processing.",
            "- Every text field passed NFC verification.",
            "- Original source files were read only.",
            "",
        ])

        (OUTPUT_ROOT / "normalization_report.md").write_text(
            "\n".join(report), encoding="utf-8"
        )

    except Exception:
        shutil.rmtree(OUTPUT_ROOT, ignore_errors=True)
        raise

    print("NFC normalization completed.")
    print("\n".join(report))


if __name__ == "__main__":
    main()
