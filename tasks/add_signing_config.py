import os
import logging
import shutil
import re
import subprocess


def run(target_path):
    logging.info("开始执行添加签名配置任务")

    # 1. 找到 app/build.gradle 文件
    build_gradle_path = os.path.join(target_path, "app", "build.gradle")
    if not os.path.exists(build_gradle_path):
        logging.warning(f"未找到 app/build.gradle 文件，路径：{build_gradle_path}")
        return False

    # 2. 读取签名配置
    keyconfig_path = os.path.join(os.path.dirname(
        __file__), "..", "templates", "key", "keyconfig.txt")
    with open(keyconfig_path, 'r') as file:
        signing_config = file.read().strip()

    # 3. 检查并添加签名配置
    with open(build_gradle_path, 'r') as file:
        content = file.read()

    # 删除现有的 signingConfigs { } 块
    pattern = re.compile(r'signingConfigs\s*\{\s*\}', re.DOTALL)
    if pattern.search(content):
        content = pattern.sub('', content)
        logging.info("已删除现有的空 signingConfigs 块")
        modified = True
    else:
        modified = False

    if signing_config not in content:
        logging.info("signingConfigs 块不在build.gradle文件中")
        content = re.sub(r'(defaultConfig \{)', f'{
                         signing_config}\n\n\\1', content)
        modified = True

    # 4. 检查并添加 debug 签名配置
    if 'signingConfig signingConfigs.debugConfig' not in content:
        content = content.replace(
            'println("-------buildTypes-------debug-------------debuggable =true-------")',
            'println("-------buildTypes-------debug-------------debuggable =true-------")\n            signingConfig signingConfigs.debugConfig'
        )
        modified = True

    # 5. 检查并添加 release 签名配置
    if 'signingConfig signingConfigs.releaseConfig' not in content:
        content = content.replace(
            'println("--------buildTypes------release--------------------isApfDebuggable " + isApfDebuggable)',
            'println("--------buildTypes------release--------------------isApfDebuggable " + isApfDebuggable)\n            signingConfig signingConfigs.releaseConfig'
        )
        modified = True

    if modified:
        with open(build_gradle_path, 'w') as file:
            file.write(content)
        logging.info("已更新 app/build.gradle 文件，添加了签名配置")

    # 6. 复制签名文件
    for key_file in ['sign_key.jks', 'upload_key.jks']:
        target_key_path = os.path.join(target_path, key_file)
        if not os.path.exists(target_key_path):
            source_key_path = os.path.join(os.path.dirname(
                __file__), "..", "templates", "key", key_file)
            shutil.copy(source_key_path, target_key_path)
            logging.info(f"已将 {key_file} 复制到项目根目录")
            modified = True

    # 7. 创建 Git commit
    if modified:
        try:
            subprocess.run(["git", "add", "app/build.gradle", "sign_key.jks",
                           "upload_key.jks"], check=True, cwd=target_path)
            subprocess.run(["git", "commit", "-m", "添加签名配置和密钥文件"],
                           check=True, cwd=target_path)
            logging.info("已创建 Git commit，记录签名配置和密钥文件的添加")
        except subprocess.CalledProcessError as e:
            logging.error(f"创建 Git commit 时发生错误：{str(e)}")
            return False

    return True
