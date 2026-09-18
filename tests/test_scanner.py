from reprocheck.scanner import scan_project


def test_scan_project():
    project = "benchmark_projects/project_clean"

    files = scan_project(project)

    file_names = [file.name for file in files]

    assert "README.md" in file_names
    assert "main.py" in file_names
    assert "requirements.txt" in file_names
    assert "sample.csv" in file_names