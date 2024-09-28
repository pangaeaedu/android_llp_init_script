import os
import re
import logging
import subprocess
from config import CONFIG


def run(target_path):
    logging.info("开始执行更新服务URL任务")
    modified = False
    service_file_list = CONFIG["service_file_list"]
    env = CONFIG["env"]

    if not service_file_list:
        logging.warning("service_file_list 为空")
        return False

    # 根据环境选择正确的替换URL
    if env == "staging":
        old_domain = r"beta\.101\.com"
        new_domain = "th2-staging.apse1.ndpg.xyz"
    elif env == "pre":
        old_domain = r"pre\.101\.com"
        new_domain = "th2-pre.apse1.ndpg.xyz"
    else:
        logging.error(f"未知的环境配置: {env}")
        return False

    # 遍历服务配置文件并进行修改
    for relative_path in service_file_list:
        file_path = os.path.join(target_path, relative_path)
        if not os.path.exists(file_path):
            logging.warning(f"文件不存在: {file_path}")
            continue

        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # 使用正则表达式替换URL
        updated_content = re.sub(
            r'(https?://[^/]*?)' + old_domain, r'\1' + new_domain, content)

        if content != updated_content:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(updated_content)
            logging.info(f"已更新文件: {file_path}")
            modified = True

    # 如果有修改，创建 Git commit
    if modified:
        try:
            subprocess.run(["git", "add"] + [os.path.join(target_path, path)
                           for path in service_file_list], check=True, cwd=target_path)
            subprocess.run(
                ["git", "commit", "-m", f"更新服务URL配置到 {env} 环境"], check=True, cwd=target_path)
            logging.info(f"已创建 Git commit，记录服务URL配置的更新到 {env} 环境")
        except subprocess.CalledProcessError as e:
            logging.error(f"创建 Git commit 时发生错误：{str(e)}")
            return False

    return True


if __name__ == "__main__":
    run()
