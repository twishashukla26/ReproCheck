from pathlib import Path


def check_file_exists(project_path, file_path):
    """Check whether a referenced file exists in the project."""

    project = Path(project_path)
    target_file = project / file_path

    return target_file.exists()

def check_absolute_paths(project_path):
    """Find hard-coded absolute paths in Python files."""

    project = Path(project_path)
    absolute_paths = []

    for python_file in project.rglob("*.py"):
        with open(python_file, "r") as file:
            for line_number, line in enumerate(file, start=1):

                if "C:\\" in line or "D:\\" in line or "/" in line:
                    absolute_paths.append(
                        (str(python_file), line_number, line.strip())
                    )

    return absolute_paths