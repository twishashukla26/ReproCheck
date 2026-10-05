from reprocheck.docker_checker import (
    check_docker_files,
    check_dockerfile_structure
)


def test_docker_files():

    project = "benchmark_projects/project_docker"

    results = check_docker_files(project)

    assert results["Dockerfile"] is True
    assert results["Docker Compose"] is True


def test_dockerfile_structure():

    project = "benchmark_projects/project_docker"

    results = check_dockerfile_structure(project)

    assert results["valid"] is True
    assert results["missing"] == []