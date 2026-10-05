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


def check_dockerfile_structure(project_path):
    """Check whether the Dockerfile contains basic Docker instructions."""

    project = Path(project_path)
    dockerfile = project / "Dockerfile"

    if not dockerfile.exists():
        return {
            "valid": False,
            "missing": ["Dockerfile"]
        }

    with open(dockerfile, "r") as file:
        content = file.read()

    required_instructions = [
        "FROM",
        "WORKDIR",
        "COPY",
        "RUN",
        "CMD"
    ]

    missing = []

    for instruction in required_instructions:
        if instruction not in content:
            missing.append(instruction)

    return {
        "valid": len(missing) == 0,
        "missing": missing
    }