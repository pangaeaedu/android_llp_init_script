import os
import json
import logging
from config import CONFIG


def run(target_path):
    env = CONFIG.get("env")
    pre_app_id = CONFIG.get("pre_app_id")
    staging_app_id = CONFIG.get("staging_app_id")

    app_id = pre_app_id if env == "pre" else staging_app_id if env == "staging" else None
    if not app_id:
        logging.error(f"Invalid env: {env}")
        return False

    file_paths = [
        'app/assets/app_factory/th/components/build.json',
        'app/assets/app_factory/zh-CN/components/build.json',
        'app/assets/app_factory/en/components/build.json'
    ]

    for file_path in file_paths:
        full_path = os.path.join(target_path, file_path)
        if not os.path.exists(full_path):
            logging.warning(f"File not found: {full_path}")
            continue

        try:
            with open(full_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            if isinstance(data, list):
                updated = False
                for item in data:
                    if isinstance(item, dict) and 'properties' in item and 'modAppId' in item['properties']:
                        item['properties']['modAppId'] = app_id
                        updated = True

                if updated:
                    with open(full_path, 'w', encoding='utf-8') as file:
                        json.dump(data, file, indent=4, ensure_ascii=False)
                    logging.info(f"Updated modAppId in {
                                 file_path} to {app_id}")
                else:
                    logging.warning(
                        f"No modAppId found in properties of any item in {file_path}")
            else:
                logging.warning(f"Invalid structure in {file_path}")

        except Exception as e:
            logging.error(f"Error updating {file_path}: {str(e)}")
            return False

    # 创建 Git commit
    try:
        import subprocess
        subprocess.run(["git", "add"] + file_paths,
                       check=True, cwd=target_path)
        subprocess.run(["git", "commit", "-m", f"Update modAppId for {
                       env} environment"], check=True, cwd=target_path)
        logging.info("Created Git commit for modAppId updates")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error creating Git commit: {str(e)}")
        return False

    return True
