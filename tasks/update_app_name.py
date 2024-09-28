import os
import re
import xml.etree.ElementTree as ET
import logging
import subprocess


def run(target_path):
    logging.info("开始执行更新应用名称任务")
    modified = False

    # 1. 寻找 app/res 文件夹
    res_path = os.path.join(target_path, "app", "res")
    if not os.path.exists(res_path):
        logging.warning(f"未找到 app/res 文件夹，路径：{res_path}")
        return False

    # 2. 查找所有 strings.xml 文件
    strings_files = []
    for root, dirs, files in os.walk(res_path):
        if "values" in root.split(os.path.sep)[-1]:
            for file in files:
                if file == "strings.xml":
                    strings_files.append(os.path.join(root, file))

    # 3. 检查并更新 strings.xml 文件
    for file_path in strings_files:
        tree = ET.parse(file_path)
        root = tree.getroot()
        for string_elem in root.findall(".//string[@name='app_name_appfactory']"):
            if string_elem.text != "aom-ai":
                string_elem.text = "aom-ai"
                tree.write(file_path, encoding="utf-8", xml_declaration=True)
                logging.info(f"已更新 {file_path} 中的应用名称为 aom-ai")
                modified = True

    # 4 & 5. 检查并更新 local.properties 文件
    local_properties_path = os.path.join(target_path, "local.properties")
    package_name_line = "want.reset.package.name=com.aom_ai.app"

    if os.path.exists(local_properties_path):
        with open(local_properties_path, 'r') as file:
            content = file.read()

        if package_name_line not in content:
            with open(local_properties_path, 'a') as file:
                file.write(f"\n{package_name_line}\n")
            logging.info(f"已在 local.properties 文件中添加 {package_name_line}")
            modified = True
    else:
        with open(local_properties_path, 'w') as file:
            file.write(f"{package_name_line}\n")
        logging.info(f"已创建 local.properties 文件并添加 {package_name_line}")
        modified = True

    # 6. 如果有修改，创建 Git commit
    if modified:
        try:
            subprocess.run(["git", "add", "."], check=True, cwd=target_path)
            subprocess.run(["git", "commit", "-m", "更新应用名称和包名配置"],
                           check=True, cwd=target_path)
            logging.info("已创建 Git commit，记录应用名称和包名配置的更新")
        except subprocess.CalledProcessError as e:
            logging.error(f"创建 Git commit 时发生错误：{str(e)}")
            return False

    return True
