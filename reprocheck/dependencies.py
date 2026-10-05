from pathlib import Path


def read_dependencies(project_path):
    """Read declared dependencies from requirements.txt."""

    project = Path(project_path)
    requirements_file = project / "requirements.txt"

    if not requirements_file.exists():
        return []

    dependencies = []

    with open(requirements_file, "r") as file:
        for line in file:
            line = line.strip()

            if line and not line.startswith("#"):
                dependencies.append(line)

    return dependencies