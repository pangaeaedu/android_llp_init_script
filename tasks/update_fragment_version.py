import os
import re
import logging
import subprocess
from config import CONFIG


def run(target_path):
    logging.info("Starting update_fragment_version task")

    files_to_update = [
        os.path.join(target_path, "app/assets/app-factory-component.gradle"),
        os.path.join(target_path, "app/app-factory-component.gradle")
    ]

    updated_files = []
    for file_path in files_to_update:
        if os.path.exists(file_path):
            if update_fragment_version(file_path, "1.4.0"):
                updated_files.append(file_path)
        else:
            logging.warning(f"File not found: {file_path}")

    if updated_files:
        create_git_commit(updated_files, target_path)
        return True
    else:
        logging.info("No files were updated")
        return False


def update_fragment_version(file_path, new_version):
    with open(file_path, 'r') as file:
        content = file.read()

    pattern = r'force "androidx\.fragment:fragment:(\d+\.\d+\.\d+)"'
    new_line = f'force "androidx.fragment:fragment:{new_version}"'

    updated_content, count = re.subn(pattern, new_line, content)

    if count > 0:
        with open(file_path, 'w') as file:
            file.write(updated_content)
        logging.info(f"Updated fragment version in {file_path}")
        return True
    else:
        logging.info(f"No changes needed in {file_path}")
        return False


def create_git_commit(files, target_path):
    try:
        subprocess.run(["git", "add"] + files, check=True, cwd=target_path)
        subprocess.run(
            ["git", "commit", "-m", "Update androidx.fragment version to 1.4.0"], check=True, cwd=target_path)
        logging.info("Created Git commit for fragment version updates")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error creating Git commit: {str(e)}")
