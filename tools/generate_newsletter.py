import argparse
import json
import sys
from pathlib import Path


def _text(value) -> str | None:
    return value if isinstance(value, str) and value.strip() else None


def _joined_text(items, key: str) -> str | None:
    if not isinstance(items, list):
        return None
    values = [_text(item.get(key)) for item in items if isinstance(item, dict)]
    present = [value for value in values if value is not None]
    return "；".join(present) or None


def _fees(items) -> str | None:
    if not isinstance(items, list):
        return None
    rendered = []
    for item in items:
        if not isinstance(item, dict):
            continue
        amount_text = _text(item.get("amount_text"))
        if amount_text is None:
            continue
        notes = _text(item.get("notes"))
        rendered.append(
            f"{amount_text}（{notes}）"
            if notes is not None and notes not in amount_text
            else amount_text
        )
    return "；".join(rendered) or None


def publication_safe(record) -> bool:
    return (
        isinstance(record, dict)
        and record.get("qa_status") == "approved"
        and record.get("uncertain_fields") == []
    )


def render_newsletter(records) -> str:
    if not isinstance(records, list):
        raise ValueError("input must be a JSON array of activity records")

    safe_records = [record for record in records if publication_safe(record)]
    lines = [
        "# 虛構活動通訊草稿",
        "",
        "> 本文件只供本地原型測試，所有活動資料均為虛構示例，並非真實中心活動。",
        "",
    ]

    for record in safe_records:
        title = _text(record.get("activity_title"))
        activity_id = _text(record.get("activity_id"))
        if title is None or activity_id is None:
            raise ValueError("publication-safe record must have an activity_id and activity_title")
        lines.extend([f"## {title}", ""])
        description = _text(record.get("description"))
        if description is not None:
            lines.extend([description, ""])

        facts = [
            ("日期", _joined_text(record.get("dates"), "date_text")),
            ("時間", _text(record.get("time"))),
            ("地點", _text(record.get("venue"))),
            ("對象", _text(record.get("target_participants"))),
            ("費用", _fees(record.get("fee"))),
            ("名額", _text(record.get("quota"))),
            ("報名方法", _text(record.get("registration_method"))),
            ("報名日期", _text(record.get("registration_period"))),
            ("備註", _text(record.get("notes"))),
        ]
        lines.extend(f"- {label}：{value}" for label, value in facts if value is not None)
        lines.extend(["", f"<!-- activity_id: {activity_id} -->", ""])

    return "\n".join(lines).rstrip() + "\n"


def load_records(path: Path):
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_deterministic(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(content)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate a deterministic fictional Markdown newsletter from approved records."
    )
    parser.add_argument("input_json", type=Path)
    parser.add_argument("output_markdown", type=Path)
    args = parser.parse_args(argv)
    try:
        records = load_records(args.input_json)
        write_deterministic(args.output_markdown, render_newsletter(records))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
