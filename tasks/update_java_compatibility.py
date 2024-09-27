import os
import re
import logging
import subprocess


def update_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    pattern = r'(sourceCompatibility|targetCompatibility)\s+(\S+)'
    new_content, count = re.subn(
        pattern, r'\1 JavaVersion.VERSION_11', content)

    if count == 0:
        logging.warning(
            f"在 {file_path} 中未找到 sourceCompatibility 或 targetCompatibility")
        return False

    with open(file_path, 'w') as file:
        file.write(new_content)

    logging.info(f"已更新 {file_path} 中的 Java 兼容性设置")
    return True


def run(target_path):
    try:
        files_to_update = [
            os.path.join(target_path, 'app', 'app-factory-component.gradle'),
            os.path.join(target_path, 'app', 'assets',
                         'app-factory-component.gradle')
        ]

        updated_files = []

        for file_path in files_to_update:
            if not os.path.exists(file_path):
                logging.warning(f"{file_path} 文件不存在")
                continue

            if update_file(file_path):
                updated_files.append(file_path)

        if not updated_files:
            logging.warning("没有文件被更新")
            return False

        # 创建 Git commit
        try:
            for file_path in updated_files:
                relative_path = os.path.relpath(file_path, target_path)
                subprocess.run(["git", "add", relative_path],
                               check=True, cwd=target_path)

            commit_message = "Update Java compatibility to VERSION_11 in app-factory-component.gradle files"
            subprocess.run(["git", "commit", "-m", commit_message],
                           check=True, cwd=target_path)
            logging.info(
                "已创建 Git commit 以记录对 app-factory-component.gradle 文件的修改")
        except subprocess.CalledProcessError as e:
            logging.error(f"创建 Git commit 时发生错误: {e}")
            return False

        return True

    except Exception as e:
        logging.error(f"更新 Java 兼容性设置时发生错误: {e}")
        return False
