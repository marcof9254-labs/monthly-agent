import json
from pathlib import Path

from tools.generate_newsletter import (
    main,
    meets_temporary_record_guard,
    partition_records_by_temporary_guard,
    render_newsletter,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "fictional-approved-newsletter-input.json"


def load_fixture():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_mixed_batch_is_explicitly_partitioned_in_input_order():
    records = load_fixture()
    qualifying, excluded = partition_records_by_temporary_guard(records)

    assert [record["activity_id"] for record in qualifying] == [
        "sample-2026-04-001",
        "sample-2026-04-002",
        "sample-2026-04-003",
        "sample-2026-04-005",
    ]
    assert excluded == [
        (
            "sample-2026-04-004",
            ("qa_status is not 'approved'", "uncertain_fields is not []"),
        )
    ]


def test_direct_render_of_mixed_batch_reports_exclusion(capsys):
    output = render_newsletter(load_fixture())

    assert "## 春日茶聚同樂日" not in output
    assert "暫定$25" not in output
    assert "通訊未列明報名日期" not in output
    assert "> 注意：本次輸入有 1 項活動未獲納入。" in output
    error = capsys.readouterr().err
    assert "WITHHELD: sample-2026-04-004" in error
    assert "qa_status is not 'approved'" in error
    assert "uncertain_fields is not []" in error


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


def test_missing_fields_are_omitted_after_explicit_partition():
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

    qualifying, excluded = partition_records_by_temporary_guard([minimal, unsafe])
    output = render_newsletter(qualifying)

    assert excluded == [("fictional-unsafe", ("uncertain_fields is not []",))]
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


def test_all_records_qualify_without_exclusions():
    qualifying = [
        record for record in load_fixture() if meets_temporary_record_guard(record)
    ]

    admitted, excluded = partition_records_by_temporary_guard(qualifying)

    assert admitted == qualifying
    assert excluded == []


def test_partition_rejects_empty_and_non_array_inputs():
    for invalid in ([], {"records": load_fixture()}):
        try:
            partition_records_by_temporary_guard(invalid)
        except ValueError as exc:
            assert str(exc)
        else:
            raise AssertionError("inadmissible CLI batch was accepted")


def test_cli_mixed_batch_succeeds_reports_and_writes_withheld_notice(tmp_path, capsys):
    input_path = tmp_path / "mixed.json"
    output_path = tmp_path / "newsletter.md"
    input_path.write_text(json.dumps(load_fixture()), encoding="utf-8")

    assert main([str(input_path), str(output_path)]) == 0
    output = output_path.read_text(encoding="utf-8")
    assert "> 注意：本次輸入有 1 項活動未獲納入。" in output
    assert "## 春日茶聚同樂日" not in output
    error = capsys.readouterr().err
    assert "WITHHELD: sample-2026-04-004" in error
    assert "qa_status is not 'approved'" in error
    assert "uncertain_fields is not []" in error


def test_cli_total_exclusion_reports_stable_labels_and_does_not_write(tmp_path, capsys):
    input_path = tmp_path / "withheld.json"
    output_path = tmp_path / "newsletter.md"
    input_path.write_text(
        json.dumps(
            [
                {"activity_id": " ", "qa_status": "needs_review", "uncertain_fields": []},
                {"activity_id": "blocked-id", "qa_status": "approved", "uncertain_fields": ["fee"]},
            ]
        ),
        encoding="utf-8",
    )

    assert main([str(input_path), str(output_path)]) == 1
    assert not output_path.exists()
    error = capsys.readouterr().err
    assert "WITHHELD: record[0]: qa_status is not 'approved'" in error
    assert "WITHHELD: blocked-id: uncertain_fields is not []" in error
    assert "nothing publishable" in error


def test_cli_malformed_json_does_not_overwrite_output(tmp_path, capsys):
    input_path = tmp_path / "malformed.json"
    output_path = tmp_path / "newsletter.md"
    input_path.write_text("[", encoding="utf-8")
    output_path.write_text("existing approved artifact\n", encoding="utf-8")

    assert main([str(input_path), str(output_path)]) == 1
    assert output_path.read_text(encoding="utf-8") == "existing approved artifact\n"
    assert "ERROR:" in capsys.readouterr().err


def test_cli_render_failure_does_not_overwrite_output(tmp_path, capsys):
    input_path = tmp_path / "approved-but-unrenderable.json"
    output_path = tmp_path / "newsletter.md"
    input_path.write_text(
        json.dumps([{"qa_status": "approved", "uncertain_fields": []}]),
        encoding="utf-8",
    )
    output_path.write_text("existing approved artifact\n", encoding="utf-8")

    assert main([str(input_path), str(output_path)]) == 1
    assert output_path.read_text(encoding="utf-8") == "existing approved artifact\n"
    assert "publication-safe record must have" in capsys.readouterr().err


def test_cli_writes_output_after_safe_batch_passes_guard(tmp_path):
    safe_records = [
        record for record in load_fixture() if meets_temporary_record_guard(record)
    ]
    input_path = tmp_path / "approved.json"
    output_path = tmp_path / "newsletter.md"
    input_path.write_text(json.dumps(safe_records), encoding="utf-8")

    assert main([str(input_path), str(output_path)]) == 0
    assert output_path.read_text(encoding="utf-8").startswith("# 虛構活動通訊草稿\n")


def test_committed_artifact_matches_rendered_frozen_fixture(capsys):
    expected = ROOT / "data" / "output" / "prototype" / "fictional-newsletter.md"

    rendered = render_newsletter(load_fixture())

    assert rendered.encode("utf-8") == expected.read_bytes()
    assert "WITHHELD: sample-2026-04-004" in capsys.readouterr().err
