from reprocheck.dependencies import read_dependencies
from reprocheck.import_checker import find_imports


def check_dependency_mismatches(project_path):
    """Find imported packages that are not declared as dependencies."""

    declared = read_dependencies(project_path)
    imported = find_imports(project_path)

    declared_names = set()

    for dependency in declared:
        name = dependency.split("==")[0]
        name = name.split(">=")[0]
        name = name.split("<=")[0]
        name = name.split(">")[0]
        name = name.split("<")[0]
        name = name.strip()

        declared_names.add(name)

    mismatches = []

    for package in imported:
        if package not in declared_names:
            mismatches.append(package)

    return mismatches