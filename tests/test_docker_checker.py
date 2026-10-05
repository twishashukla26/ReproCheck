from reprocheck.docker_checker import check_docker_files


def test_docker_files():

    project = "benchmark_projects/project_docker"

    results = check_docker_files(project)

    assert results["Dockerfile"] is True
    assert results["Docker Compose"] is True