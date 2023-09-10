import os
import re


def is_valid_github_url(repo_url: str) -> bool:
    """Check if the given URL is a valid GitHub repository URL.

    Parameters:
        repo_url (str): The URL of the GitHub repository to check.

    Returns:
        bool: True if the URL is valid, False otherwise.
    """
    github_url_pattern = r'^https:\/\/github\.com\/[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+$'
    return re.match(github_url_pattern, repo_url) is not None


def fetch_github_repo_contents(repo_url: str, temp_dir: str) -> None:
    """Clone a GitHub repository to a temporary directory.

    Parameters:
        repo_url (str): The URL of the GitHub repository to clone.
        temp_dir (str): The path of the temporary directory where the repository will be cloned.

    Raises:
        ValueError: If the GitHub repository URL is invalid.
    """
    if not is_valid_github_url(repo_url):
        raise ValueError("Invalid GitHub repository URL")

    os.system(f'git clone {repo_url} {temp_dir}')
