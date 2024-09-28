import logging
import importlib
import os
from config import CONFIG

# 设置日志
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# 任务列表
tasks = [
    'init_git',
    'create_gitignore',
    'initial_commit',
    'run_workspace_script',
    'add_allow_insecure_protocol',
    'update_gradle_plugin_version',
    'update_java_compatibility',
    'update_target_sdk_version',
    'copy_gradle_templates',
    'update_mod_app_id',
    'update_fragment_version',
    'remove_permissions',
    'add_signing_config'
]


def run_task(task_name):
    try:
        module = importlib.import_module(f'tasks.{task_name}')
        return module.run(CONFIG["target_project_path"])
    except ImportError:
        logging.error(f"无法导入任务模块: {task_name}")
        return False
    except AttributeError:
        logging.error(f"任务模块 {task_name} 没有 run() 函数")
        return False


def main():
    successful_tasks = []
    failed_tasks = []

    for task in tasks:
        logging.info(f"执行任务: {task}")
        if run_task(task):
            logging.info(f"任务 {task} 完成\n")
            successful_tasks.append(task)
        else:
            logging.warning(f"任务 {task} 失败\n")
            failed_tasks.append(task)

    # 打印总结
    logging.info("任务执行总结:")
    if successful_tasks:
        logging.info(f"成功的任务: {', '.join(successful_tasks)}")
    if failed_tasks:
        logging.warning(f"失败的任务: {', '.join(failed_tasks)}")


if __name__ == "__main__":
    main()
