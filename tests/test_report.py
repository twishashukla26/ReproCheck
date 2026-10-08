from reprocheck.result import CheckResult
from reprocheck.report import format_report


def test_check_result_status_methods():
    passed = CheckResult("README", "PASS", "README file found")
    warning = CheckResult("Docker", "WARNING", "Dockerfile found")
    failed = CheckResult("Dependencies", "FAIL", "requirements.txt missing")

    assert passed.is_passed()
    assert not passed.is_warning()
    assert not passed.is_failed()

    assert warning.is_warning()
    assert not warning.is_passed()
    assert not warning.is_failed()

    assert failed.is_failed()
    assert not failed.is_passed()
    assert not failed.is_warning()


def test_format_report_contains_project_and_summary():
    results = [
        CheckResult("README", "PASS", "README file found"),
        CheckResult("License", "WARNING", "License file missing"),
        CheckResult("Dependencies", "FAIL", "requirements.txt missing"),
    ]

    report = format_report("sample_project", results)

    assert "REPROCHECK REPORT" in report
    assert "Project: sample_project" in report

    assert "README: README file found" in report
    assert "License: License file missing" in report
    assert "Dependencies: requirements.txt missing" in report

    assert "Passed:   1" in report
    assert "Warnings: 1" in report
    assert "Failed:   1" in report