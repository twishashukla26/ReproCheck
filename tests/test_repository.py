from reprocheck.repository import check_readme, check_license, check_dependencies


def test_check_readme():
    project = "benchmark_projects/project_clean"

    assert check_readme(project) is True


def test_check_license():
    project = "benchmark_projects/project_clean"

    assert check_license(project) is True


def test_check_dependencies():
    project = "benchmark_projects/project_clean"

    assert check_dependencies(project) is True