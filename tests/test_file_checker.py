from reprocheck.file_checker import check_file_exists, check_absolute_paths


def test_check_file_exists():
    project = "benchmark_projects/project_clean"

    assert check_file_exists(project, "data/sample.csv") is True
    assert check_file_exists(project, "data/missing.csv") is False


def test_check_absolute_paths():
    project = "benchmark_projects/project_hardcoded_path"

    paths = check_absolute_paths(project)

    assert len(paths) > 0
    assert "Users" in paths[0][2]
    assert "Desktop" in paths[0][2]
    assert "data.csv" in paths[0][2]