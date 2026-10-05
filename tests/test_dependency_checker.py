from reprocheck.dependency_checker import check_dependency_mismatches


def test_dependency_mismatch():
    project = "benchmark_projects/project_missing_dependency"

    mismatches = check_dependency_mismatches(project)

    assert "matplotlib" in mismatches