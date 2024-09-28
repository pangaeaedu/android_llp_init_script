import os
import shutil
import re
from config import CONFIG


def run(script_root_path, target_project_path):
    print("开始执行本地集成Task")

    # 1 & 2. 替换 settings.gradle 文件内容
    settings_gradle_path = os.path.join(target_project_path, 'settings.gradle')
    settings_local_gradle_path = os.path.join(
        script_root_path, 'templates', 'local_integrate', 'settings_local.gradle')

    if os.path.exists(settings_gradle_path) and os.path.exists(settings_local_gradle_path):
        with open(settings_local_gradle_path, 'r') as f:
            new_content = f.read()
        with open(settings_gradle_path, 'w') as f:
            f.write(new_content)
        print("已更新 settings.gradle 文件")
    else:
        print("未找到 settings.gradle 或 settings_local.gradle 文件")

    # 3 & 4. 更新 gradle.properties 文件
    gradle_properties_path = os.path.join(
        target_project_path, 'gradle.properties')
    if os.path.exists(gradle_properties_path):
        with open(gradle_properties_path, 'r') as f:
            content = f.read()
        if 'build_in_shell' not in content:
            with open(gradle_properties_path, 'a') as f:
                f.write('\nbuild_in_shell=true\n')
            print("已在 gradle.properties 中添加 build_in_shell 行")
    else:
        print("未找到 gradle.properties 文件")

    # 5 & 6. 复制 buildSrc 文件夹
    buildsrc_target = os.path.join(target_project_path, 'buildSrc')
    buildsrc_source = os.path.join(script_root_path, 'templates', 'buildSrc')
    if not os.path.exists(buildsrc_target):
        shutil.copytree(buildsrc_source, buildsrc_target)
        print("已复制 buildSrc 文件夹到项目根目录")
    else:
        print("buildSrc 文件夹已存在")

    # 7, 8, 9, 10 & 11. 更新 app-factory-component.gradle 文件
    app_factory_component_path = os.path.join(
        target_project_path, 'app', 'app-factory-component.gradle')
    if os.path.exists(app_factory_component_path):
        with open(app_factory_component_path, 'r') as f:
            content = f.readlines()

        # 注释掉指定的依赖库
        local_integrate_lib = CONFIG.get('local_integrate_lib', [])
        for i, line in enumerate(content):
            for lib in local_integrate_lib:
                if lib in line and not line.strip().startswith('//'):
                    content[i] = '//' + line
                    print(f"已注释依赖库: {lib}")

        # 插入 lib_local.txt 内容
        lib_local_path = os.path.join(
            script_root_path, 'templates', 'local_integrate', 'lib_local.txt')
        if os.path.exists(lib_local_path):
            with open(lib_local_path, 'r') as f:
                lib_local_content = f.read()

            if lib_local_content not in ''.join(content):
                content.insert(2, lib_local_content + '\n')
                print("已插入 lib_local.txt 内容")

        # 写回文件
        with open(app_factory_component_path, 'w') as f:
            f.writelines(content)
        print("已更新 app-factory-component.gradle 文件")
    else:
        print("未找到 app-factory-component.gradle 文件")

    print("本地集成Task执行完成")
    return True


if __name__ == "__main__":
    # 这里假设脚本在脚本工程的根目录运行
    script_root_path = os.path.dirname(os.path.abspath(__file__))
    target_project_path = CONFIG['target_project_path']
    run(script_root_path, target_project_path)
