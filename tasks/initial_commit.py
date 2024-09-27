import subprocess
import logging


def run(target_path):
    try:
        # 检查是否有需要提交的更改
        status_output = subprocess.run(['git', 'status', '--porcelain'],
                                       check=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       cwd=target_path,
                                       text=True).stdout.strip()

        if not status_output:
            logging.info("没有需要提交的更改，跳过初始提交")
            return True

        logging.info("检测到需要提交的更改，正在进行初始提交...")

        # 添加所有文件
        subprocess.run(['git', 'add', '.'],
                       check=True,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE,
                       cwd=target_path)

        # 提交
        subprocess.run(['git', 'commit', '-m', "Initial commit"],
                       check=True,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE,
                       cwd=target_path,
                       text=True).stdout.strip()

        logging.info(f"初始提交完成")
        return True
    except Exception as e:
        logging.error(f"进行初始提交时发生错误: {e}")
        return False
