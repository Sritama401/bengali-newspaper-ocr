# E1: engine accuracy against the reference text

Reference text: Google Lens output, not fully verified by a Bengali reader.
CER = character edits needed / reference length (whitespace ignored). Lower is better.

| Engine | Samples | Mean CER | Median CER |
|---|---|---|---|
| EasyOCR (fresh) | 20 | 0.457 | 0.470 |
| Gemini (fresh) | 20 | 0.113 | 0.065 |
| Saved draft | 20 | 0.425 | 0.458 |

Mean CER by label:

| Engine | All | BodyText | Headline | Subtitle |
|---|---|---|---|---|
| EasyOCR (fresh) | 0.457 | 0.742 | 0.175 | 0.170 |
| Gemini (fresh) | 0.113 | 0.175 | 0.037 | 0.065 |
| Saved draft | 0.425 | 0.756 | 0.131 | 0.058 |
