import os
import re
from config import CONFIG


def run(script_root_path, target_project_path):
    print("开始执行取消本地集成Task")

    # 1 & 2. 替换 settings.gradle 文件内容
    settings_gradle_path = os.path.join(target_project_path, 'settings.gradle')
    settings_remote_gradle_path = os.path.join(
        script_root_path, 'templates', 'local_integrate', 'settings_remote.gradle')

    if os.path.exists(settings_gradle_path) and os.path.exists(settings_remote_gradle_path):
        with open(settings_remote_gradle_path, 'r') as f:
            new_content = f.read()
        with open(settings_gradle_path, 'w') as f:
            f.write(new_content)
        print("已更新 settings.gradle 文件")
    else:
        print("未找到 settings.gradle 或 settings_remote.gradle 文件")

    # 3 & 4. 更新 gradle.properties 文件
    gradle_properties_path = os.path.join(
        target_project_path, 'gradle.properties')
    if os.path.exists(gradle_properties_path):
        with open(gradle_properties_path, 'r') as f:
            lines = f.readlines()
        new_lines = [
            line for line in lines if not line.strip().startswith('build_in_shell')]
        if len(new_lines) != len(lines):
            with open(gradle_properties_path, 'w') as f:
                f.writelines(new_lines)
            print("已从 gradle.properties 中移除 build_in_shell 行")
        else:
            print("gradle.properties 中没有找到 build_in_shell 行")
    else:
        print("未找到 gradle.properties 文件")

    # 5, 6, 7, 8 & 9. 更新 app-factory-component.gradle 文件
    app_factory_component_path = os.path.join(
        target_project_path, 'app', 'app-factory-component.gradle')
    if os.path.exists(app_factory_component_path):
        with open(app_factory_component_path, 'r') as f:
            content = f.read()

        # 取消注释指定的依赖库
        local_integrate_lib = CONFIG.get('local_integrate_lib', [])
        for lib in local_integrate_lib:
            content = re.sub(
                r'//\s*(.*' + re.escape(lib) + '.*)', r'\1', content)
            print(f"已取消注释依赖库: {lib}")

        # 移除 lib_local.txt 内容
        lib_local_path = os.path.join(
            script_root_path, 'templates', 'local_integrate', 'lib_local.txt')
        if os.path.exists(lib_local_path):
            with open(lib_local_path, 'r') as f:
                lib_local_content = f.read().strip()

            content = content.replace(lib_local_content, '')
            print("已移除 lib_local.txt 内容")

        # 写回文件
        with open(app_factory_component_path, 'w') as f:
            f.write(content)
        print("已更新 app-factory-component.gradle 文件")
    else:
        print("未找到 app-factory-component.gradle 文件")

    print("取消本地集成Task执行完成")
    return True


if __name__ == "__main__":
    # 这里假设脚本在脚本工程的根目录运行
    script_root_path = os.path.dirname(os.path.abspath(__file__))
    target_project_path = CONFIG['target_project_path']
    run(script_root_path, target_project_path)
