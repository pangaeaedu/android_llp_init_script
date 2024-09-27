import os
import re
import logging
import subprocess


def run(target_path):
    try:
        local_properties_path = os.path.join(target_path, 'local.properties')

        # 检查文件是否存在
        if not os.path.exists(local_properties_path):
            logging.warning(f"local.properties 文件不存在于 {target_path}")
            return False

        # 读取文件内容
        with open(local_properties_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # 使用正则表达式查找 targetSdkVersion 行
        pattern = r'^targetSdkVersion\s*=\s*\d+\s*$'
        match = re.search(pattern, content, re.MULTILINE)

        if not match:
            logging.info("未找到 targetSdkVersion 行，任务结束")
            return True  # 任务成功完成，但没有进行修改

        # 替换找到的行
        new_content = re.sub(pattern, 'targetSdkVersion=34',
                             content, flags=re.MULTILINE)

        # 写入修改后的内容
        with open(local_properties_path, 'w', encoding='utf-8') as file:
            file.write(new_content)

        logging.info("已将 targetSdkVersion 更新为 34")

        # 创建 Git commit
        try:
            subprocess.run(["git", "add", "local.properties"],
                           check=True, cwd=target_path)
            subprocess.run(
                ["git", "commit", "-m", "Update targetSdkVersion to 34 in local.properties"], check=True, cwd=target_path)
            logging.info("已创建 Git commit 以记录对 local.properties 的修改")
        except subprocess.CalledProcessError as e:
            logging.error(f"创建 Git commit 时发生错误: {e}")
            return False

        return True

    except Exception as e:
        logging.error(f"更新 local.properties 时发生错误: {e}")
        return False
