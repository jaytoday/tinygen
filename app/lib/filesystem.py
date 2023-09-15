import hashlib
import logging
import os
import shutil
from typing import List, Dict

BASE_CODE_PATH = '/tmp/repo'


def generate_hash_for_repo_and_prompt(repo_url: str, prompt: str) -> str:
    """Generate a unique hash for a given repository URL and prompt.

    Parameters:
        repo_url (str): The URL of the repository.
        prompt (str): The code generation prompt.

    Returns:
        str: The generated hash.
    """
    combined_string = f"{repo_url}::{prompt}"
    sha256 = hashlib.sha256()
    sha256.update(combined_string.encode())
    return sha256.hexdigest()


def fetch_files(root: str, paths: List[str]) -> str:
    """Fetch the contents of specified files.

    Parameters:
        root (str): The root directory where the files are located.
        paths (List[str]): The paths of the files to fetch.

    Returns:
        str: The concatenated content of all files.
    """
    contents_list = []
    for item_path in paths:
        full_item_path = os.path.join(root, item_path)
        contents_list.append(f"\n--- File: {item_path} ---\n")
        try:
            with open(full_item_path, 'r', encoding='utf-8', errors='ignore') as file:
                contents_list.append(file.read())
        except FileNotFoundError:
            logging.info(f"File not found: {full_item_path}. This is likely a new file to be added in the code diff.")
    return "".join(contents_list)


def fetch_file_map(root: str, path: str = "") -> Dict:
    """Fetch a file map of the specified directory.

    Parameters:
        root (str): The root directory to start from.
        path (str, optional): The relative path to start from. Defaults to an empty string.

    Returns:
        Dict: A map of filenames to their full paths.
    """
    file_map = {}
    for item in os.listdir(os.path.join(root, path)):
        item_path = os.path.join(path, item) if path else item
        full_item_path = os.path.join(root, item_path)
        if os.path.isdir(full_item_path):
            file_map[item] = fetch_file_map(root, item_path)
        else:
            file_map[item] = full_item_path  # type: ignore
    return file_map


def prepare_temp_dir(hash: str) -> str:
    """Prepare a temporary directory for the code.

    Parameters:
        hash (str): A unique hash to identify the temporary directory.

    Returns:
        str: The path to the prepared directory.
    """
    temp_dir = f'{BASE_CODE_PATH}/{hash}'
    if not os.path.exists(BASE_CODE_PATH):
        os.makedirs(BASE_CODE_PATH)
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    return temp_dir


def remove_temp_dir(temp_dir: str):
    """Remove a temporary directory.

    Parameters:
        temp_dir (str): The path to the temporary directory to remove.
    """
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
