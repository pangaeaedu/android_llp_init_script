import subprocess
import os
import logging


def run(target_path):
    try:
        if os.path.exists(os.path.join(target_path, '.git')):
            logging.info("目标目录已经是一个Git仓库，不需要初始化.")
            return True

        logging.info("正在初始化Git仓库...")
        subprocess.run(['git', 'init'], check=True, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, cwd=target_path)
        logging.info("Git仓库已成功初始化.")
        return True
    except Exception as e:
        logging.error(f"初始化Git仓库时发生错误: {e}")
        return False
