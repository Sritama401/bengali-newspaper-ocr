
# Bengali Historical Newspaper OCR

A research and dataset-preparation project focused on extracting Bengali text from historical newspaper images and preparing image–text pairs for Optical Character Recognition (OCR).

## 1. Project Overview

The objective of this project is to prepare Bengali newspaper data for OCR research and model training.

The work focuses on:
- Inspecting annotated newspaper pages.
- Comparing OCR engines.
- Preparing paired image crops and Bengali transcriptions.
- Applying Unicode NFC normalization.
- Auditing transcription quality.
- Validating dataset structure and documenting limitations.

**Important:** This project has completed its first dataset-preparation cycle. Final OCR model training has not yet been performed.

## 2. Research and Initial Data Inspection

### E0 — Initial Data Summary

The initial inspection examined 100 pages and reported 6,558 original prediction regions.

| Measurement | Result |
|---|---:|
| Pages examined | 100 |
| Original regions | 6,558 |
| Text-field regions (excluding Image) | 6,481 |
| Empty text fields | 0 |
| Placeholder text | 402 |
| Real-text regions | 6,079 |
| Real-text regions with Bengali share below 50% | 940 |
| Median text length | 74 characters |

The inspection identified issues involving placeholder labels, Bengali character share and text quality.

### E1 — OCR Engine Comparison

The comparison used 20 samples. Google Lens output was used as the reference, but it was not fully verified by a Bengali reader.

Character Error Rate (CER) measures character-level edits divided by reference length. Whitespace was ignored. Lower CER is better.

| OCR source | Mean CER | Median CER |
|---|---:|---:|
| EasyOCR | 0.457 | 0.470 |
| Gemini | 0.113 | 0.065 |
| Saved draft | 0.425 | 0.458 |

Gemini performed best overall in this sample. However, agreement with Google Lens does not establish transcription correctness.

### E1b — Gemini Scale Test

A sample of 50 body-text boxes was tested: 25 retained and 25 rejected examples.

| Measurement | Result |
|---|---:|
| Boxes attempted | 50 |
| Boxes failed after retries | 43 |
| Mean time per box | 70.1 seconds |
| Median time per box | 69.1 seconds |
| Estimated time for 3,729 body boxes | Approximately 72.6 hours |

The test experienced API availability, resource-exhaustion and timeout errors.

This was a limited test, not a reliable throughput benchmark. Under the tested conditions, the API was not sufficiently reliable for bulk generation.

## 3. Dataset Preparation

### Dataset v0

The initial dataset preparation produced:

| Measurement | Result |
|---|---:|
| Retained records | 4,422 |
| Rejected records | 1,326 |
| Total boxes considered | 5,748 |

The dataset report is available at `dataset_v0/report.md`.

### Cycle 1 — Paired Dataset Preparation

Two separate source collections were processed.

| Measurement | Manual-reference collection | Model-assisted collection |
|---|---:|---:|
| Pages/tasks | 100 | 100 |
| Paired records | 2,083 | 5,982 |
| Rejected records | 1,363 | 4 |
| Conflicts | 0 | 1 |
| Image regions excluded | 65 | 53 |
| Crops generated | 2,083 | 5,982 |

**Combined output:**
- 8,065 image–text pairs.
- 8,065 image crops.
- 200 collection-level page/task records.

The 200 records should not be interpreted as 200 unique newspaper pages because uniqueness across the two collections was not established.

### Dataset Record Structure

Each JSONL record contains:

| Field | Description |
|---|---|
| `image` | Path to the corresponding image crop |
| `text` | Bengali transcription |
| `page` | Page/task identifier |
| `region_id` | Annotation region identifier |
| `label` | Region label |
| `labels` | Associated labels |
| `label_conflict` | Indicates a label conflict |
| `annotation_ids` | Associated annotation identifiers |
| `bbox` | Original percentage-based bounding box |
| `text_origin` | Origin of the transcription |
| `verification_status` | Independent verification status |

Example JSONL record:

```json
{
  "image": "crops/001.png",
  "text": "আজ দেশের নানা স্থানে বৃষ্টি হইয়াছে।"
}
```

### Important Dataset Details

- Image regions were excluded from the paired text dataset.
- Repeated region IDs were merged within tasks where applicable.
- Geometry and transcription conflicts were recorded separately.
- The model-assisted collection contained one label conflict.
- Original annotation text was retained without new OCR correction.
- The script converts percentage-based bounding boxes into pixel coordinates for cropping.
- Crop coordinates are rounded and clamped to image boundaries.
- Transcriptions are marked `not_independently_verified`.

## 4. Unicode NFC Normalization

Unicode NFC normalization was applied to the transcription field using Python's `unicodedata.normalize("NFC", text)`.

| Collection | Records | Changed by normalization |
|---|---:|---:|
| Manual-reference | 2,083 | 1,089 (52.28%) |
| Model-assisted | 5,982 | 1,348 (22.53%) |
| Combined | 8,065 | 2,437 (30.22%) |

The normalization process:
- Preserved the original source data.
- Created separate normalized outputs.
- Changed only the text field.
- Preserved other record fields.
- Checked NFC normalization and crop-path existence.
- Refused to overwrite an existing output directory.

Validation results:
- 8,065 records checked.
- Zero missing crop files.
- Zero structural validation errors.

Normalization improves Unicode consistency; it does not correct spelling or transcription errors.

## 5. Quality-Control Audits

### Human Transcription Audit

A sample of 20 records was inspected: 10 from each collection.

| Assessment | Manual-reference | Model-assisted | Combined |
|---|---:|---:|---:|
| Correct | 6 | 2 | 8 |
| Partial | 1 | 1 | 2 |
| Incorrect | 2 | 6 | 8 |
| Unreadable/uncertain | 1 | 0 | 1 |
| Not recorded | 0 | 1 | 1 |

Among assessable records, exact transcription accuracy was:

| Collection | Exact matches |
|---|---:|
| Manual-reference | 6/9 (66.7%) |
| Model-assisted | 2/9 (22.2%) |
| Combined | 8/18 (44.4%) |

This was a small sample reviewed by one person without adjudication. It is not representative of the entire dataset and does not establish full ground-truth accuracy.

### Prediction-versus-Annotation Audit

The audit compared original prediction regions with final annotation regions across 100 pages.

| Measurement | Result |
|---|---:|
| Original prediction regions | 6,558 |
| Final annotation regions | 5,748 |
| Matching region IDs | 5,745 |
| Added regions | 3 |
| Missing regions | 813 |
| Text differences among matching IDs | 0 |
| Label differences among matching IDs | 0 |
| Bounding-box differences among matching IDs | 5 |

Among the missing regions, 775 non-image regions had OCR text in the original predictions.

The audit does not establish why regions were removed or whether the retained transcriptions are correct.

## 6. Repository Structure

```text
bengali-newspaper-ocr/
│
├── README.md
├── .gitignore
│
├── E0_data_summary/
│   └── summary.md
│
├── E1_ocr_engines/
│   └── summary.md
│
├── E1b_gemini_scale/
│   └── summary.md
│
├── dataset_v0/
│   └── report.md
│
├── audit_inspection/
│   ├── human_transcription_audit_report.md
│   └── prediction_annotation_audit.md
│
├── reports/
│   └── quality_control/
│       └── normalization_report.md
│
└── src/
    ├── build_paired_datasets.py
    └── normalize_nfc.py
```

Generated datasets, original images, crops, intermediate files and other local working data are excluded from the public Git repository.

## 7. Reproducibility

The main processing scripts are:

| Script | Purpose |
|---|---|
| `src/build_paired_datasets.py` | Builds paired datasets from annotation inputs |
| `src/normalize_nfc.py` | Creates NFC-normalized dataset outputs |

The dataset-building script uses the original annotation and image inputs. It records rejected records and conflicts separately and prevents accidental overwriting of existing output directories.

The normalization script preserves non-text fields and produces separate outputs.

The original input files and generated datasets are maintained separately from the public repository.

## 8. Limitations

The following limitations must be considered when interpreting the results:

1. Transcriptions have not been independently verified across the entire dataset.
2. The human audit covered only 20 samples.
3. Google Lens was used as a comparison reference but was not fully verified.
4. OCR engine agreement does not guarantee transcription correctness.
5. Gemini API failures limited the feasibility of large-scale processing under the tested conditions.
6. Unicode normalization does not repair incorrect Bengali text.
7. Structural validation does not establish image–text semantic accuracy.
8. The two source collections should not automatically be treated as 200 unique newspaper pages.
9. No final OCR model has been trained or evaluated in this project cycle.

## 9. Future Work

Potential next steps include:

- Expand human transcription verification.
- Correct transcription errors through Bengali-language review.
- Inspect bounding-box and crop quality.
- Investigate rejected records and conflicts.
- Improve reproducibility and dataset documentation.
- Establish a verified training and evaluation split.
- Train and evaluate a Bengali OCR model using the prepared data.

## 10. Reports and Documentation

| Report | Location |
|---|---|
| Initial data summary | `E0_data_summary/summary.md` |
| OCR engine comparison | `E1_ocr_engines/summary.md` |
| Gemini scale test | `E1b_gemini_scale/summary.md` |
| Dataset v0 report | `dataset_v0/report.md` |
| Human transcription audit | `audit_inspection/human_transcription_audit_report.md` |
| Prediction-annotation audit | `audit_inspection/prediction_annotation_audit.md` |
| NFC normalization report | `reports/quality_control/normalization_report.md` |

---

## Conclusion

This project has established a documented Bengali historical newspaper OCR data-preparation workflow. It includes initial data inspection, OCR engine comparison, paired dataset construction, Unicode normalization, structural validation and quality-control audits.

The Cycle 1 output contains 8,065 image–text pairs across two source collections. However, independent transcription verification remains necessary before treating the complete dataset as reliable ground truth for OCR training.

**The current achievement is a documented and structurally validated dataset-preparation cycle, not a completed OCR model.**
