import os
import subprocess
import platform
import logging


def run(target_path):
    try:
        system = platform.system()
        shebang_fixed = False

        if system == "Windows":
            script_path = os.path.join(target_path, "workSpaceCanRun.bat")
            if os.path.exists(script_path):
                logging.info("在 Windows 系统上运行 workSpaceCanRun.bat")
                subprocess.run([script_path], check=True, cwd=target_path)
            else:
                logging.warning("workSpaceCanRun.bat 不存在")
                return False

        elif system in ["Darwin", "Linux"]:  # Darwin 是 Mac OS 的系统名
            script_path = os.path.join(target_path, "workSpaceCanRun.sh")
            if os.path.exists(script_path):
                logging.info("在 Unix-like 系统上运行 workSpaceCanRun.sh")

                # 检查文件内容
                with open(script_path, 'r') as file:
                    first_line = file.readline().strip()
                    if not first_line.startswith("#!"):
                        # 尝试修复 shebang 行
                        if first_line.replace(" ", "").startswith("#!"):
                            logging.warning(
                                f"workSpaceCanRun.sh 的 shebang 行格式不正确。尝试修复...")
                            with open(script_path, 'r') as original_file:
                                content = original_file.read()
                            with open(script_path, 'w') as fixed_file:
                                fixed_file.write(
                                    "#!/bin/sh\n" + content[len(first_line):])
                            logging.info("shebang 行已修复")
                            shebang_fixed = True
                        else:
                            logging.error(
                                f"workSpaceCanRun.sh 缺少 shebang 行。文件开头: {first_line}")
                            return False

                # 先赋予执行权限
                subprocess.run(["chmod", "+x", script_path], check=True)

                # 然后运行脚本，使用完整路径
                try:
                    result = subprocess.run(
                        [script_path], check=True, cwd=target_path, capture_output=True, text=True)
                    logging.info(f"脚本输出: {result.stdout}")
                except subprocess.CalledProcessError as e:
                    logging.error(f"脚本执行失败。返回码: {e.returncode}")
                    logging.error(f"错误输出: {e.stderr}")
                    return False
            else:
                logging.warning("workSpaceCanRun.sh 不存在")
                return False

        else:
            logging.error(f"不支持的操作系统: {system}")
            return False

        # 如果修复了 shebang 行，创建一个 Git commit
        if shebang_fixed:
            try:
                subprocess.run(["git", "add", "workSpaceCanRun.sh"],
                               check=True, cwd=target_path)
                subprocess.run(
                    ["git", "commit", "-m", "Fix shebang line in workSpaceCanRun.sh"], check=True, cwd=target_path)
                logging.info("已创建 Git commit 以记录对 workSpaceCanRun.sh 的修改")
            except subprocess.CalledProcessError as e:
                logging.error(f"创建 Git commit 时发生错误: {e}")
                # 注意：我们不在这里返回 False，因为主要任务已经完成

        logging.info("工作空间脚本执行完成")
        return True

    except subprocess.CalledProcessError as e:
        logging.error(f"执行工作空间脚本时发生错误: {e}")
        logging.error(f"错误输出: {e.stderr}")
        return False
    except Exception as e:
        logging.error(f"运行工作空间脚本时发生未知错误: {e}")
        return False
