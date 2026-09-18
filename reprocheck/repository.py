from pathlib import Path


def check_readme(project_path):
    """Check whether the project contains a README file."""

    project = Path(project_path)

    readme_files = [
        project / "README.md",
        project / "README.txt",
        project / "README"
    ]

    for readme in readme_files:
        if readme.exists():
            return True

    return False


def check_license(project_path):
    """Check whether the project contains a license file."""

    project = Path(project_path)

    license_files = [
        project / "LICENSE",
        project / "LICENSE.txt",
        project / "LICENSE.md"
    ]

    for license_file in license_files:
        if license_file.exists():
            return True

    return False

def check_dependencies(project_path):
    """Check whether the project contains a dependency file."""

    project = Path(project_path)

    dependency_files = [
        project / "requirements.txt",
        project / "pyproject.toml"
    ]

    for dependency_file in dependency_files:
        if dependency_file.exists():
            return True

    return False