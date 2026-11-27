# Bengali OCR Dataset — NFC Normalization Report

## 1. Objective

Standardize canonically equivalent Unicode representations in Bengali
transcriptions using Unicode NFC normalization.

## 2. Method

Python's `unicodedata.normalize("NFC", text)` was applied to the
`text` field of each JSONL record.

No OCR was performed and no spelling or transcription corrections
were made.

Original datasets were preserved. Normalized outputs were stored
separately.

## 3. Results

| Dataset | Total records | Changed | Unchanged |
|---|---:|---:|---:|
| Manual-reference | 2,083 | 1,089 | 994 |
| Model-assisted | 5,982 | 1,348 | 4,634 |
| **Total** | **8,065** | **2,437** | **5,628** |

Approximately 30.2% of text fields changed their Unicode
representation during normalization.

## 4. Validation

- All 8,065 records passed NFC verification.
- All output records were parsed as JSON during generation.
- Non-text fields were checked for preservation.
- Original source datasets were not modified.
- A second NFC pass produced no further changes in the earlier pilot.

## 5. Output locations

- `data/processed/normalized_nfc/manual_reference/dataset.jsonl`
- `data/processed/normalized_nfc/model_assisted/dataset.jsonl`
- `data/processed/normalized_nfc/normalization_report.md`

## 6. Limitations

NFC normalization standardizes canonically equivalent Unicode
representations. It does not correct spelling, OCR errors,
historical Bengali spellings, or transcription mistakes.

The normalized text should not be treated as independently
verified ground truth.

## 7. Reproducibility

The reusable normalization script is stored at:

`src/normalize_nfc.py`
