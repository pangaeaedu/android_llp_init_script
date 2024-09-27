import os
import logging
import shutil


def run(target_path):
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_path = os.path.join(
        script_dir, 'templates', 'gitignore_template.txt')

    try:
        # 创建 .gitignore 文件
        if not os.path.exists(template_path):
            logging.error(f"gitignore 模板文件不存在: {template_path}")
            return False

        with open(template_path, 'r') as template_file:
            gitignore_content = template_file.read()

        with open(os.path.join(target_path, '.gitignore'), 'w') as gitignore_file:
            gitignore_file.write(gitignore_content)

        logging.info(".gitignore 文件已创建，使用外部模板文件")

        # 处理 flutter 目录
        flutter_dir = os.path.join(target_path, 'flutter')
        if os.path.exists(flutter_dir):
            git_dir = os.path.join(flutter_dir, '.git')
            gitignore_file = os.path.join(flutter_dir, '.gitignore')

            # 删除 .git 目录
            if os.path.exists(git_dir):
                shutil.rmtree(git_dir)
                logging.info(f"已删除 {git_dir}")

            # 删除 .gitignore 文件
            if os.path.exists(gitignore_file):
                os.remove(gitignore_file)
                logging.info(f"已删除 {gitignore_file}")

            logging.info("flutter 目录下的 .git 和 .gitignore 已被删除")
        else:
            logging.info("flutter 目录不存在，跳过删除操作")

        return True
    except Exception as e:
        logging.error(f"在处理 .gitignore 或 flutter 目录时发生错误: {e}")
        return False
