# Prediction vs Annotation Audit

## Purpose
Compare the original model predictions embedded in the Label Studio
annotations with the final non-cancelled annotations.

## Source
Label Studio export:
project-6-at-2026-11-23-10-49-09e88c99.json

## 1. Overall comparison

- Pages with embedded predictions: 100
- Original prediction regions: 6,558
- Final annotation regions: 5,748
- Regions present in both: 5,745
- Regions added in annotations: 3
- Predicted regions missing from annotations: 813

## 2. Changes among matching region IDs

- Text differences: 0
- Label differences: 0
- Bounding-box differences: 5

These results describe differences between prediction and annotation
records. They do not establish transcription correctness or human
verification.

## 3. Missing prediction regions by original label

| Label | Missing regions |
|---|---:|
| BodyText | 588 |
| Headline | 122 |
| Subtitle | 58 |
| Image | 38 |
| Caption | 7 |
| Total | 813 |

Missing regions occurred on 81 pages.

## 4. OCR text availability in missing regions

| Label | Total | With OCR text | Without OCR text |
|---|---:|---:|---:|
| BodyText | 588 | 588 | 0 |
| Headline | 122 | 122 | 0 |
| Subtitle | 58 | 58 | 0 |
| Caption | 7 | 7 | 0 |
| Image | 38 | 0 | 38 |
| Total | 813 | 775 | 38 |

The 775 non-image missing regions contained OCR text in the original
prediction. This does not establish that the text was correct.

## 5. Median bounding-box area and OCR text length

The audit calculated the product of normalized width and height.
These are percentage-coordinate products, not pixel areas.

| Label | Median width × height | Median OCR text length |
|---|---:|---:|
| BodyText | 55.70173 | 141 |
| Caption | 29.09607 | 49 |
| Headline | 59.42684 | 26 |
| Image | 110.95153 | Not applicable |
| Subtitle | 5.88201 | 12 |

## 6. Interpretation and limitations

- Most missing prediction regions were BodyText.
- 775 missing non-image regions had predicted OCR text.
- Matching region IDs showed no text or label differences in this audit.
- Five matching regions had bounding-box differences.
- The audit does not explain why regions were removed.
- The audit does not establish whether retained or removed OCR text is correct.
- The OCR text has not been established as human-verified ground truth.

## 7. Next investigation

Investigate representative missing prediction regions in their original
page-image context to understand possible reasons for removal.

No source annotations, original images, or dataset_v0 files were modified
by the audits documented here.
