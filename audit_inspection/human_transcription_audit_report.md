# Human Transcription Quality Audit

## 1. Objective

A preliminary human inspection was conducted to examine whether the Bengali transcriptions corresponded to their associated newspaper image crops.

## 2. Sample

A total of 20 samples were inspected:
- 10 from the manual-reference collection.
- 10 from the model-assisted collection.

## 3. Results

| Judgment | Manual-reference | Model-assisted |
|---|---:|---:|
| Correct | 6 | 2 |
| Partially correct | 1 | 1 |
| Incorrect | 2 | 6 |
| Unreadable / uncertain | 1 | 0 |
| Not recorded | 0 | 1 |
| Total | 10 | 10 |

## 4. Exact-match proportions

For this preliminary analysis, only samples marked Correct, Partially correct, or Incorrect were treated as assessable.

- Manual-reference: 6/9 exact matches (66.7%).
- Model-assisted: 2/9 exact matches (22.2%).
- Combined: 8/18 exact matches (44.4%).

Partially correct records were not counted as exact matches. Unreadable and unrecorded samples were excluded from the denominator.

## 5. Interpretation

The inspected samples show a higher proportion of exact matches in the manual-reference collection than in the model-assisted collection. The model-assisted sample also contained more records judged incorrect.

These observations suggest that transcription quality requires further human verification, particularly for model-assisted records.

## 6. Limitations

- The audit covered only 20 samples.
- The results are not statistically representative estimates of the complete datasets.
- One sample in each collection was excluded from the exact-match calculation.
- The judgments represent a preliminary human inspection and were not independently adjudicated by multiple reviewers.
- Structural validation of image paths and JSONL records does not establish transcription correctness.

## 7. Conclusion

The preliminary audit demonstrates the importance of human transcription quality assessment in addition to structural dataset validation. A larger and more systematic review is required before treating the transcriptions as verified OCR training ground truth.
