# Bengali Historical Newspaper OCR Dataset

A research project for preparing Bengali image–text pairs from annotated historical newspaper pages, evaluating OCR engines, and documenting dataset quality and limitations.

> **Project status:** Cycle 1 paired-dataset preparation, Unicode NFC normalization, structural validation, and initial quality audits are complete. Final OCR model training and comprehensive transcription verification have not yet been completed.

## 1. Project Overview

Historical Bengali newspapers are valuable sources of linguistic, cultural, and historical information. Making their contents searchable and machine-readable requires reliable Optical Character Recognition (OCR).

This project focuses on preparing image–text training data from annotated Bengali newspaper pages.

The central objective is to create records in which each newspaper-region image crop is paired with its corresponding Bengali transcription.

Example JSONL record (illustrative only):

```json
{
  "image": "crops/001.png",
  "text": "আজ দেশের নানা স্থানে বৃষ্টি হইয়াছে।"
}
## 4. Research and Initial Data Inspection

### E0 — Initial Data Summary

The initial data inspection examined 100 pages and reported 6,558 original prediction regions.

| Measurement | Result |
|---|---:|
| Pages examined | 100 |
| Original prediction regions | 6,558 |
| Text-field regions, excluding Image | 6,481 |
| Empty text fields | 0 |
| Placeholder text records | 402 |
| Records containing real text | 6,079 |
| Real-text records with Bengali share below 50% | 940 |
| Real-text records with Bengali share below 80% | 3,204 |

The original region labels were:

| Label | Count |
|---|---:|
| BodyText | 4,314 |
| Headline | 1,137 |
| Subtitle | 980 |
| Image | 77 |
| Caption | 50 |

The Bengali-share calculation uses Bengali letters, Bengali digits, or danda relative to the non-space characters in a text field.

**Interpretation:** The initial data contained a substantial number of records with low Bengali-character share. This indicates that language-content filtering and manual quality inspection are important parts of dataset preparation.

The 6,558 figure refers to the original prediction-region data described in the initial inspection. It should not be confused with the later final annotation-region count.

Detailed report: `E0_data_summary/summary.md`

### E1 — OCR Engine Comparison

A small comparison was conducted using 20 sample regions.

Google Lens output was used as the reference text. It was not fully verified by a Bengali reader, so the results measure agreement with that reference rather than guaranteed transcription accuracy.

Character Error Rate (CER) was calculated as:

`CER = character edit distance / reference text length`

Whitespace was ignored. Lower CER indicates closer agreement with the reference.

#### Overall results

| OCR source | Mean CER | Median CER |
|---|---:|---:|
| EasyOCR | 0.457 | 0.470 |
| Gemini | 0.113 | 0.065 |
| Saved draft | 0.425 | 0.458 |

#### Mean CER by region label

| Label | EasyOCR | Gemini | Saved draft |
|---|---:|---:|---:|
| All samples | 0.457 | 0.113 | 0.425 |
| BodyText | 0.742 | 0.175 | 0.756 |
| Headline | 0.175 | 0.037 | 0.131 |
| Subtitle | 0.170 | 0.065 | 0.058 |

Gemini showed the lowest overall mean CER and the lowest mean CER for BodyText and Headline in this sample. The saved draft performed slightly better than Gemini on Subtitle.

**Limitations:**
- The evaluation used only 20 samples.
- Google Lens was not independently verified as ground truth.
- A lower CER against an unverified reference does not establish actual transcription correctness.
- These results should not be generalized to the complete newspaper dataset.

Detailed report: `E1_ocr_engines/summary.md`

### E1b — Gemini Scale Feasibility Test

A separate experiment investigated whether Gemini could reliably process a larger number of newspaper regions.

The test included 50 BodyText boxes:
- 25 retained boxes.
- 25 rejected boxes.
- Random seed: 42.

No independently verified reference text was available for this experiment, so OCR accuracy was not measured.

#### Observed results

| Measurement | Result |
|---|---:|
| Boxes attempted | 50 |
| Boxes failing after retries | 43 |
| Failure proportion | 86% |
| Mean time per box | 70.1 seconds |
| Median time per box | 69.1 seconds |
| Estimated time for 3,729 BodyText boxes | Approximately 72.6 hours |

Recorded errors included:

| Error | Recorded count |
|---|---:|
| 503 UNAVAILABLE | 143 |
| 429 RESOURCE_EXHAUSTED | 131 |
| Read timeout | 4 |
| 504 DEADLINE_EXCEEDED | 2 |

These counts represent recorded errors across retries, not unique failed boxes.

The estimated processing time is a rough extrapolation under the tested conditions. It is not a guaranteed processing-time benchmark.

**Conclusion:** Under the tested configuration, quota, and timing conditions, API requests were not sufficiently reliable for straightforward bulk OCR generation.

Detailed report: `E1b_gemini_scale/summary.md`
## 5. Dataset Preparation

### Earlier Dataset Version

An earlier dataset preparation stage produced `dataset_v0`.

| Measurement | Result |
|---|---:|
| Pages | 100 |
| Original boxes | 5,748 |
| Retained lines | 4,422 |
| Rejected regions | 1,326 |
| Retention rate | 76.9% |

The report records the following rejection reasons:

- Low Bengali share: 892
- Placeholder text: 388
- Image box: 39
- Short text: 4
- No text: 3

The report also notes that the retained BodyText transcriptions were largely based on EasyOCR output and had a mean CER of approximately 0.74 in the E1 comparison.

This version is preserved as an earlier preparation result. It is not the same as the later Cycle 1 paired dataset.

Detailed report: `dataset_v0/report.md`

### Cycle 1 — Paired Dataset Construction

The main Cycle 1 pipeline was implemented in:

`src/build_paired_datasets.py`

Its purpose is to extract image crops from annotated newspaper regions and pair them with the corresponding annotation text.

Two source collections were processed separately.

#### Manual-reference collection

| Measurement | Result |
|---|---:|
| Pages/tasks | 100 |
| Original images matched | 100 |
| Retained records | 2,083 |
| Rejected regions | 1,363 |
| Conflict records | 0 |
| Image regions excluded | 65 |
| Repeated region IDs merged | 0 |

Text-origin metadata:

| Text origin | Records |
|---|---:|
| `manual` | 288 |
| `unknown` | 1,795 |

The collection name describes its source. It does not mean that every transcription was independently verified by a human.

#### Model-assisted collection

| Measurement | Result |
|---|---:|
| Pages/tasks | 100 |
| Original images matched | 100 |
| Retained records | 5,982 |
| Rejected regions | 4 |
| Conflict records | 1 |
| Image regions excluded | 53 |
| Repeated region IDs merged | 79 |

Text-origin metadata:

| Text origin | Records |
|---|---:|
| `prediction` | 5,812 |
| `prediction-changed` | 170 |

The 79 repeated region IDs were merged within their respective annotation tasks by the preparation script. This should not be interpreted as global duplicate removal across all pages.

#### Combined Cycle 1 results

| Measurement | Combined result |
|---|---:|
| Source collection page/task records | 200 |
| Original images matched across collections | 200 |
| Retained image–text pairs | 8,065 |
| Rejected regions | 1,367 |
| Conflict records | 1 |
| Image regions excluded | 118 |
| Repeated region IDs merged | 79 |

The combined count of 200 represents 100 page/task records in each of two source collections. It has not been established that these represent 200 unique newspaper pages across both collections.

#### Output structure

```text
data/
├── raw/
│   ├── annotations/
│   │   ├── manual_reference/
│   │   │   └── teammate_manual.json
│   │   └── model_assisted/
│   │       └── your_model_assisted.json
│   └── images/
│       └── teammate_original/
└── processed/
    ├── manual_reference/
    │   ├── dataset.jsonl
    │   ├── rejected.jsonl
    │   ├── conflicts.jsonl
    │   ├── report.md
    │   └── crops/
    └── model_assisted/
        ├── dataset.jsonl
        ├── rejected.jsonl
        ├── conflicts.jsonl
        ├── report.md
        └── crops/
## 6. Unicode NFC Normalization

Bengali text can contain visually similar strings represented by different Unicode character sequences.

Unicode normalization helps make equivalent character sequences consistent.

The project uses NFC normalization through Python's `unicodedata` module.

Implementation:

```python
unicodedata.normalize("NFC", text)
## 8. Overall Workflow

The project contains several related but distinct research and preparation activities.

```mermaid
flowchart TD
    A["Original newspaper images and annotation exports"]

    A --> B["E0: Initial data summary"]
    A --> C["E1: OCR engine comparison"]
    A --> D["E1b: Gemini scale feasibility test"]

    A --> E["Prediction-versus-annotation audit"]

    A --> F["Cycle 1: Paired dataset construction"]

    F --> G["Manual-reference collection"]
    F --> H["Model-assisted collection"]

    G --> I["Image crops + Bengali text pairs"]
    H --> I

    I --> J["Structural validation"]
    J --> K["Unicode NFC normalization"]
    K --> L["Normalized datasets"]

    I --> M["Human transcription audit"]
    E --> N["Annotation quality findings"]
    B --> N
    C --> N
    D --> N
    M --> N

    L --> O["Future OCR training and evaluation"]
    N --> O
