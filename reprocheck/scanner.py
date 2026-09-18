from pathlib import Path


def scan_project(project_path):
    """Return all files inside a project directory."""

    project = Path(project_path)

    if not project.exists():
        raise FileNotFoundError(f"Project not found: {project_path}")

    if not project.is_dir():
        raise NotADirectoryError(f"Not a directory: {project_path}")

    files = []

    for item in project.rglob("*"):
        if item.is_file():
            files.append(item)

    return files