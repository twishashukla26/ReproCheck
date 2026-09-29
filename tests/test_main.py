from reprocheck.main import generate_report


def test_generate_report(capsys):

    project = "benchmark_projects/project_clean"

    generate_report(project)

    captured = capsys.readouterr()

    assert "README found" in captured.out
    assert "LICENSE found" in captured.out
    assert "pandas" in captured.out