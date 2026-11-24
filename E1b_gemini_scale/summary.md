# E1b: Gemini on body-text crops

Sample: 25 kept + 25 rejected body boxes (seed 42). No reference text, so accuracy is NOT measured here.

- Boxes tried: 50 | failed after retries: 43 (86%)
- Mean seconds per box (including retries): 70.1 | median 69.1
- Estimate for all 3729 body boxes: about 72.6 hours (plus 1.0 h of pauses)

Errors seen (count of occurrences):

- 503 UNAVAILABLE. {'error': {'code': 503, 'mes: 143
- 429 RESOURCE_EXHAUSTED. {'error': {'code': 42: 131
- The read operation timed out: 4
- 504 DEADLINE_EXCEEDED. {'error': {'code': 504: 2

| Group | Boxes ok | Old share | Gemini share | Old length | Gemini length |
|---|---|---|---|---|---|
| kept | 7 | 0.71 | 0.97 | 361 | 507 |
