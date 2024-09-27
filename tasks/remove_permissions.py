import os
import re
import logging
import subprocess
from config import CONFIG


def run(target_path):
    logging.info("Starting remove_permissions task")

    manifest_path = os.path.join(target_path, "app/AndroidManifest.xml")

    if not os.path.exists(manifest_path):
        logging.warning(f"AndroidManifest.xml not found at {manifest_path}")
        return False

    with open(manifest_path, 'r') as file:
        content = file.read()

    if "<!-- Remove Permission -->" in content:
        logging.info(
            "Remove Permission comment already exists. No changes needed.")
        return True

    permissions_to_remove = """
    <!-- Remove Permission -->
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" tools:node="remove" />
    <uses-permission android:name="android.permission.RECORD_AUDIO" tools:node="remove" />
    <uses-permission android:name="android.permission.REQUEST_INSTALL_PACKAGES" tools:node="remove" />
    <uses-permission android:name="android.permission.WRITE_SETTINGS" tools:node="remove" />
    <uses-permission android:name="android.permission.QUERY_ALL_PACKAGES" tools:node="remove" />
    
"""

    # Find the first <uses-permission line
    match = re.search(r'^\s*<uses-permission', content, re.MULTILINE)
    if match:
        insert_position = match.start()
        updated_content = content[:insert_position] + \
            permissions_to_remove + content[insert_position:]

        with open(manifest_path, 'w') as file:
            file.write(updated_content)

        logging.info(f"Updated AndroidManifest.xml with removed permissions")

        # Create git commit
        try:
            subprocess.run(["git", "add", manifest_path],
                           check=True, cwd=target_path)
            subprocess.run(
                ["git", "commit", "-m", "Remove unnecessary permissions from AndroidManifest.xml"], check=True, cwd=target_path)
            logging.info("Created Git commit for removed permissions")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error creating Git commit: {str(e)}")
            return False

        return True
    else:
        logging.warning(
            "No <uses-permission line found in AndroidManifest.xml")
        return False
