import os
import re
import logging
import subprocess


def run(target_path):
    try:
        gradle_file_path = os.path.join(target_path, 'build.gradle')

        # 检查文件是否存在
        if not os.path.exists(gradle_file_path):
            logging.warning(f"build.gradle 文件不存在于 {target_path}")
            return False

        # 读取文件内容
        with open(gradle_file_path, 'r') as file:
            content = file.read()

        # 使用正则表达式查找并替换版本号
        pattern = r'(gradle_plugin_version\s*=\s*["\'])([^"\']*)(["\']\s*)'
        new_content, count = re.subn(pattern, r'\g<1>7.1.2\g<3>', content)

        if count == 0:
            logging.warning("未找到 gradle_plugin_version 行")
            return False

        # 写入修改后的内容
        with open(gradle_file_path, 'w') as file:
            file.write(new_content)

        logging.info("已将 gradle_plugin_version 更新为 7.1.2")

        # 创建 Git commit
        try:
            subprocess.run(["git", "add", "build.gradle"],
                           check=True, cwd=target_path)
            subprocess.run(
                ["git", "commit", "-m", "Update gradle_plugin_version to 7.1.2"], check=True, cwd=target_path)
            logging.info("已创建 Git commit 以记录对 build.gradle 的修改")
        except subprocess.CalledProcessError as e:
            logging.error(f"创建 Git commit 时发生错误: {e}")
            return False

        return True

    except Exception as e:
        logging.error(f"更新 build.gradle 时发生错误: {e}")
        return False
