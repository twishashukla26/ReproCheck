from reprocheck.import_checker import find_imports


def test_find_imports():

    project = "benchmark_projects/project_clean"

    imports = find_imports(project)

    assert "pandas" in imports
    assert "numpy" in imports