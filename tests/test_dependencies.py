from reprocheck.dependencies import read_dependencies


def test_read_dependencies():

    project = "benchmark_projects/project_clean"

    dependencies = read_dependencies(project)

    assert "pandas" in dependencies
    assert "numpy" in dependencies