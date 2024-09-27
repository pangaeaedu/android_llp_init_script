import os
import logging
import subprocess


def run(target_path):
    try:
        properties_path = os.path.join(target_path, 'local.properties')

        # 检查文件是否存在
        if not os.path.exists(properties_path):
            logging.warning(f"local.properties 文件不存在于 {target_path}")
            return False

        # 读取文件内容
        with open(properties_path, 'r') as file:
            lines = file.readlines()

        # 检查是否存在目标行
        target_line = "allowInsecureProtocol=true\n"
        if any(line.strip() == target_line.strip() for line in lines):
            logging.info("allowInsecureProtocol=true 已存在于 local.properties")
            return True

        # 如果不存在，添加目标行
        with open(properties_path, 'a') as file:
            if lines and not lines[-1].endswith('\n'):
                file.write('\n')  # 确保在新的一行添加
            file.write(target_line)

        logging.info("已向 local.properties 添加 allowInsecureProtocol=true")

        # 创建 Git commit
        try:
            subprocess.run(["git", "add", "local.properties"],
                           check=True, cwd=target_path)
            subprocess.run(
                ["git", "commit", "-m", "Add allowInsecureProtocol=true to local.properties"], check=True, cwd=target_path)
            logging.info("已创建 Git commit 以记录对 local.properties 的修改")
        except subprocess.CalledProcessError as e:
            logging.error(f"创建 Git commit 时发生错误: {e}")
            return False

        return True

    except Exception as e:
        logging.error(f"更新 local.properties 时发生错误: {e}")
        return False
