import shutil
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import urlparse


def validate_github_url(repo_url):
    """Validate that the supplied URL is a GitHub repository URL."""

    repo_url = repo_url.strip()

    parsed = urlparse(repo_url)

    if parsed.scheme not in ("http", "https"):
        raise ValueError("Repository URL must start with http:// or https://")

    if parsed.netloc.lower() not in ("github.com", "www.github.com"):
        raise ValueError("Please provide a GitHub repository URL.")

    if not parsed.path.strip("/"):
        raise ValueError("Please provide a complete GitHub repository URL.")

    return repo_url


def clone_repository(repo_url):
    """
    Clone a public GitHub repository into a temporary directory.

    Returns:
        Path: local path of the cloned repository.
    """

    repo_url = validate_github_url(repo_url)

    temp_directory = Path(
        tempfile.mkdtemp(prefix="reprocheck_")
    )

    repository_directory = temp_directory / "repository"

    try:
        subprocess.run(
            [
                "git",
                "clone",
                "--depth",
                "1",
                repo_url,
                str(repository_directory),
            ],
            check=True,
            capture_output=True,
            text=True,
        )

    except FileNotFoundError:
        shutil.rmtree(temp_directory, ignore_errors=True)
        raise RuntimeError(
            "Git was not found on this computer. "
            "Please make sure Git is installed."
        )

    except subprocess.CalledProcessError as error:
        shutil.rmtree(temp_directory, ignore_errors=True)

        message = error.stderr.strip()

        if message:
            raise RuntimeError(
                f"Could not clone the repository:\n{message}"
            )

        raise RuntimeError(
            "Could not clone the repository. "
            "Please check that the URL is correct and the repository is public."
        )

    return repository_directory


def cleanup_repository(repository_path):
    """Delete the temporary cloned repository."""

    repository_path = Path(repository_path)

    # The repository is inside a temporary directory created by us.
    temporary_directory = repository_path.parent

    shutil.rmtree(temporary_directory, ignore_errors=True)