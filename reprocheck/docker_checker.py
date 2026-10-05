from pathlib import Path


def check_docker_files(project_path):
    """Check whether Docker configuration files exist."""

    project = Path(project_path)

    dockerfile = project / "Dockerfile"
    compose_yml = project / "docker-compose.yml"
    compose_yaml = project / "docker-compose.yaml"

    return {
        "Dockerfile": dockerfile.exists(),
        "Docker Compose": compose_yml.exists() or compose_yaml.exists()
    }