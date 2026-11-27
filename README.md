### Cycle 1 source collections and outputs

Cycle 1 processed two separate source collections:

**Manual-reference collection**
- 100 pages/tasks and 100 matched original images.
- 2,083 retained image–text pairs.
- 1,363 rejected regions.
- 65 Image regions excluded.
- No conflict records and no repeated region IDs merged.
- Text origin: 288 records marked `manual` and 1,795 marked `unknown`.

**Model-assisted collection**
- 100 pages/tasks and 100 matched original images.
- 5,982 retained image–text pairs.
- 4 rejected regions.
- 53 Image regions excluded.
- 1 conflict record and 79 repeated region IDs merged.
- Text origin: 5,812 records marked `prediction` and 170 marked `prediction-changed`.

Together, the two collections produced 8,065 retained image–text pairs and 1,367 rejected regions.

These are two source collections of 100 pages/tasks each. The combined count of 200 refers to collection-level page/task records; it should not be interpreted as 200 unique newspaper pages without checking image identity across the collections.

Neither collection is fully independently verified. The source labels describe text origin, not guaranteed transcription accuracy.
