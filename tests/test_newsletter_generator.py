import json
from pathlib import Path

from tools.generate_newsletter import publication_safe, render_newsletter


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "fictional-approved-newsletter-input.json"


def load_fixture():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_includes_only_approved_records_without_uncertainty():
    records = load_fixture()
    output = render_newsletter(records)

    assert [record["activity_id"] for record in records if publication_safe(record)] == [
        "sample-2026-04-001",
        "sample-2026-04-002",
        "sample-2026-04-003",
        "sample-2026-04-005",
    ]
    assert "## 春日茶聚同樂日" not in output
    assert "暫定$25" not in output
    assert "通訊未列明報名日期" not in output


def test_preserves_participant_facing_facts_exactly():
    output = render_newsletter(load_fixture())

    expected_lines = {
        "## 護心有法健康講座",
        "- 日期：2026年4月8日（三）",
        "- 時間：上午10:30至11:30",
        "- 地點：中心活動室一",
        "- 對象：中心會員及區內長者",
        "- 費用：免費",
        "- 名額：30人",
        "- 報名方法：親臨中心櫃位報名",
        "- 報名日期：2026年3月25日起，額滿即止",
        "- 費用：會員$60（已包括材料）；非會員$90（已包括材料）",
        "- 備註：每位參加者可完成一份鮮花作品。請攜帶會員證。活動如有更改，以中心公布為準。",
    }
    assert expected_lines <= set(output.splitlines())


def test_missing_fields_are_omitted_and_uncertain_approved_record_is_excluded():
    minimal = {
        "activity_id": "fictional-minimal",
        "activity_title": "只有標題的虛構活動",
        "qa_status": "approved",
        "uncertain_fields": [],
    }
    unsafe = {
        "activity_id": "fictional-unsafe",
        "activity_title": "不應刊登",
        "qa_status": "approved",
        "uncertain_fields": ["fee"],
        "fee": [{"amount_text": "待定"}],
    }

    output = render_newsletter([minimal, unsafe])

    assert "## 只有標題的虛構活動" in output
    assert "不應刊登" not in output
    assert "待定" not in output
    assert "- 日期：" not in output
    assert "- 費用：" not in output


def test_rendering_is_deterministic_readable_and_non_empty():
    records = load_fixture()
    first = render_newsletter(records)
    second = render_newsletter(records)

    assert first.encode("utf-8") == second.encode("utf-8")
    assert first.startswith("# 虛構活動通訊草稿\n")
    assert len(first.splitlines()) > 20
