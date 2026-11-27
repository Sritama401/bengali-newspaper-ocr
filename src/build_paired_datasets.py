import json
import os
import re
from pathlib import Path
from collections import Counter, defaultdict
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent

COLLECTIONS = {
    "manual_reference": {
        "annotation": ROOT / "data/raw/annotations/manual_reference/teammate_manual.json",
        "image_dirs": [
            ROOT / "data/raw/images/teammate_original"
        ],
        "filename_field": "file_upload",
    },
    "model_assisted": {
        "annotation": ROOT / "data/raw/annotations/model_assisted/your_model_assisted.json",
        "image_dirs": [
            ROOT / "batches",
            Path(os.environ["BATCH_08_DIR"]) if os.environ.get("BATCH_08_DIR") else ROOT / "batches/batch_08",
        ],
        "filename_field": "original_filename",
    },
}

ALLOWED_LABELS = {"BodyText", "Headline", "Subtitle", "Caption"}


def get_page_filename(task, collection):
    data = task.get("data", {})

    if collection == "manual_reference":
        value = task.get("file_upload", "")
        match = re.search(
            r"\d{4}-\d{2}-\d{2}_page_\d+\.[A-Za-z0-9]+",
            str(value)
        )
        return match.group(0) if match else None

    value = (
        data.get("original_filename")
        or data.get("filename")
    )
    return Path(str(value)).name if value else None


def get_image_index(directories):
    index = defaultdict(list)

    for directory in directories:
        if not directory.exists():
            continue

        for path in directory.rglob("*"):
            if path.is_file() and path.suffix.lower() in {
                ".jpg", ".jpeg", ".png", ".tif", ".tiff"
            }:
                index[path.name].append(path)

    return index


def extract_regions(annotation):
    regions = {}

    for item in annotation.get("result", []):
        rid = item.get("id")
        if not rid:
            continue

        if item.get("type") not in {"rectanglelabels", "textarea"}:
            continue

        regions.setdefault(rid, {})
        regions[rid][item["type"]] = item

    return regions


def build_collection(name, config):
    annotation_path = config["annotation"]
    output = ROOT / "data/processed" / name
    crops_dir = output / "crops"

    # Never overwrite existing outputs.
    if output.exists() and any(output.iterdir()):
        raise SystemExit(
            f"STOP: {output} already contains files. "
            "Move or rename it before running this script."
        )

    if not annotation_path.exists():
        raise SystemExit(f"Missing annotation file: {annotation_path}")

    image_index = get_image_index(config["image_dirs"])

    print(f"\nProcessing: {name}")
    print("Loading annotation JSON...")

    with annotation_path.open(encoding="utf-8") as f:
        tasks = json.load(f)

    output.mkdir(parents=True, exist_ok=True)
    crops_dir.mkdir(parents=True, exist_ok=True)

    records = []
    rejected = []
    conflicts = []
    label_counts = Counter()
    origin_counts = Counter()
    missing_sources = []
    image_regions = 0
    duplicate_regions = 0

    for task in tasks:
        filename = get_page_filename(task, name)

        if not filename:
            rejected.append({
                "reason": "page_filename_missing"
            })
            continue

        matches = image_index.get(filename, [])

        if len(matches) != 1:
            missing_sources.append({
                "page": filename,
                "matching_images": len(matches)
            })
            continue

        annotations = [
            a for a in task.get("annotations", [])
            if not a.get("was_cancelled", False)
            and isinstance(a.get("result"), list)
        ]

        if not annotations:
            rejected.append({
                "page": filename,
                "reason": "no_active_annotation"
            })
            continue

        merged = {}

        for annotation in annotations:
            annotation_id = annotation.get("id")
            regions = extract_regions(annotation)

            for rid, region in regions.items():
                entry = merged.setdefault(rid, {
                    "rectangles": [],
                    "textareas": [],
                    "annotation_ids": [],
                })

                if region.get("rectanglelabels"):
                    entry["rectangles"].append(region["rectanglelabels"])

                if region.get("textarea"):
                    entry["textareas"].append(region["textarea"])

                if annotation_id is not None:
                    entry["annotation_ids"].append(annotation_id)

        with Image.open(matches[0]) as original:
            image = original.convert("RGB")
            W, H = image.size

            for rid, entry in merged.items():
                rectangles = entry["rectangles"]
                textareas = entry["textareas"]

                if not rectangles:
                    continue

                # Compare rectangle geometry across annotations.
                geometries = {
                    tuple(
                        round(float(r["value"][key]), 5)
                        for key in ("x", "y", "width", "height")
                    )
                    for r in rectangles
                }

                texts = {
                    tuple(
                        str(t) for t in
                        item.get("value", {}).get("text", [])
                    )
                    for item in textareas
                }

                if len(geometries) > 1 or len(texts) > 1:
                    conflicts.append({
                        "page": filename,
                        "region_id": rid,
                        "reason": "conflicting_geometry_or_text",
                        "annotation_ids": entry["annotation_ids"],
                        "geometries": [list(g) for g in geometries],
                        "texts": [list(t) for t in texts],
                    })
                    continue

                if len(rectangles) > 1:
                    duplicate_regions += 1

                rect = rectangles[0]
                value = rect.get("value", {})
                labels = sorted({
                    str(label)
                    for r in rectangles
                    for label in r.get("value", {}).get(
                        "rectanglelabels", []
                    )
                })

                label = labels[0] if labels else "Unknown"

                if label == "Image":
                    image_regions += 1
                    continue

                if not set(labels).intersection(ALLOWED_LABELS):
                    continue

                if len(labels) > 1:
                    conflicts.append({
                        "page": filename,
                        "region_id": rid,
                        "reason": "label_conflict",
                        "labels": labels,
                        "annotation_ids": entry["annotation_ids"],
                    })

                if not textareas:
                    rejected.append({
                        "page": filename,
                        "region_id": rid,
                        "label": label,
                        "reason": "missing_textarea",
                    })
                    continue

                text_values = list(texts)[0] if texts else ()
                text = " ".join(text_values).strip()

                if not text:
                    rejected.append({
                        "page": filename,
                        "region_id": rid,
                        "label": label,
                        "reason": "empty_transcription",
                    })
                    continue

                x = float(value["x"])
                y = float(value["y"])
                w = float(value["width"])
                h = float(value["height"])

                left = max(0, min(W, round(x * W / 100)))
                top = max(0, min(H, round(y * H / 100)))
                right = max(0, min(W, round((x + w) * W / 100)))
                bottom = max(0, min(H, round((y + h) * H / 100)))

                if right <= left or bottom <= top:
                    rejected.append({
                        "page": filename,
                        "region_id": rid,
                        "label": label,
                        "reason": "invalid_crop_coordinates",
                    })
                    continue

                crop = image.crop((left, top, right, bottom))

                safe_id = re.sub(r"[^A-Za-z0-9_-]", "_", str(rid))
                crop_name = f"{Path(filename).stem}__{safe_id}.png"
                crop_path = crops_dir / crop_name

                if crop_path.exists():
                    raise SystemExit(
                        f"Unexpected duplicate crop path: {crop_path}"
                    )

                crop.save(crop_path)

                origins = {
                    t.get("origin", "unknown")
                    for t in textareas
                }
                text_origin = sorted(origins)[0]
                origin_counts[text_origin] += 1
                label_counts[label] += 1

                records.append({
                    "image": f"crops/{crop_name}",
                    "text": text,
                    "page": filename,
                    "region_id": rid,
                    "label": label,
                    "labels": labels,
                    "label_conflict": len(labels) > 1,
                    "annotation_ids": entry["annotation_ids"],
                    "bbox": {
                        "x": x,
                        "y": y,
                        "width": w,
                        "height": h,
                    },
                    "text_origin": text_origin,
                    "verification_status": "not_independently_verified",
                })

    if missing_sources:
        print("\nERROR: Missing or ambiguous original images:")
        for item in missing_sources[:20]:
            print(item)

        raise SystemExit(
            "No JSONL export written. Resolve missing images first."
        )

    def write_jsonl(path, items):
        with path.open("w", encoding="utf-8") as f:
            for item in items:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

    write_jsonl(output / "dataset.jsonl", records)
    write_jsonl(output / "rejected.jsonl", rejected)
    write_jsonl(output / "conflicts.jsonl", conflicts)

    report = f"""# Bengali OCR Paired Dataset: {name}

## Source
- Annotation file: {annotation_path.name}
- Pages/tasks: {len(tasks)}
- Original images matched: {len(tasks) - len(missing_sources)}

## Dataset
- Records: {len(records)}
- Rejected regions: {len(rejected)}
- Conflict records: {len(conflicts)}
- Image regions excluded: {image_regions}
- Repeated region IDs merged: {duplicate_regions}

## Labels
{chr(10).join(f"- {k}: {v}" for k, v in sorted(label_counts.items()))}

## Text origins
{chr(10).join(f"- {k}: {v}" for k, v in sorted(origin_counts.items()))}

## Important limitations
- Transcriptions have not been independently verified.
- Structural validation does not establish transcription accuracy.
- Conflicting geometry or text is excluded from the dataset.
- Label conflicts are preserved in metadata and conflicts.jsonl.
- Original annotation text is retained without OCR correction.

## Files
- dataset.jsonl: paired image crops and transcriptions.
- rejected.jsonl: excluded regions and reasons.
- conflicts.jsonl: annotation conflicts.
- crops/: cropped newspaper regions.
"""

    (output / "report.md").write_text(report, encoding="utf-8")

    print(f"\nCompleted: {name}")
    print("Pages:", len(tasks))
    print("Records:", len(records))
    print("Rejected:", len(rejected))
    print("Conflicts:", len(conflicts))
    print("Labels:", dict(label_counts))
    print("Output:", output)


if __name__ == "__main__":
    for name, config in COLLECTIONS.items():
        build_collection(name, config)

    print("\nBoth paired datasets have been created.")
