from reprocheck.main import main


def test_generate_report(capsys):

    project = "benchmark_projects/project_clean"

    import sys

    original_argv = sys.argv

    sys.argv = [
        "reprocheck",
        project
    ]

    try:
        main()
    finally:
        sys.argv = original_argv

    captured = capsys.readouterr()

    assert "README found" in captured.out
    assert "LICENSE found" in captured.out
    assert "pandas" in captured.out


def test_json_report_generation(capsys, tmp_path, monkeypatch):

    project = "benchmark_projects/project_docker"

    import sys
    import os

    original_argv = sys.argv
    original_directory = os.getcwd()

    monkeypatch.chdir(tmp_path)

    sys.argv = [
        "reprocheck",
        project,
        "--json"
    ]

    try:
        main()
    finally:
        sys.argv = original_argv
        monkeypatch.chdir(original_directory)

    captured = capsys.readouterr()

    assert "JSON report saved to report.json" in captured.out

    report_file = tmp_path / "report.json"

    assert report_file.exists()