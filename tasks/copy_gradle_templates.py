import os
import shutil
import logging
import subprocess


def run(target_path):
    try:
        # 获取脚本项目的templates/gradle目录路径
        script_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__)))
        source_gradle_dir = os.path.join(script_dir, 'templates', 'gradle')

        # 获取目标项目的gradle目录路径
        target_gradle_dir = os.path.join(target_path, 'gradle')

        # 检查目标项目是否已经有gradle目录
        if os.path.exists(target_gradle_dir):
            logging.info(f"目标项目已存在gradle目录: {target_gradle_dir}")
            return True  # 任务成功完成，但没有进行复制

        # 复制gradle目录及其内容
        shutil.copytree(source_gradle_dir, target_gradle_dir)
        logging.info(f"已将gradle模板复制到: {target_gradle_dir}")

        # 创建Git commit
        try:
            subprocess.run(["git", "add", "gradle"],
                           check=True, cwd=target_path)
            subprocess.run(
                ["git", "commit", "-m", "Add gradle directory from templates"], check=True, cwd=target_path)
            logging.info("已创建Git commit以记录gradle目录的添加")
        except subprocess.CalledProcessError as e:
            logging.error(f"创建Git commit时发生错误: {e}")
            return False

        return True

    except Exception as e:
        logging.error(f"复制gradle模板时发生错误: {e}")
        return False
