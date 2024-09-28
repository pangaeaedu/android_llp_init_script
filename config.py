import os

# 配置参数
CONFIG = {
    # 替换为实际的目标项目路径
    "target_project_path": os.path.expanduser("/Users/wurf/Code/llp/llp_9_27"),
    # 在这里可以添加更多的配置参数

    # 环境，可以是 staging 或 pre
    "env": "staging",
    "pre_app_id": "9f45cb97-6499-45a5-8149-0bfc905b8ac0",
    "staging_app_id": "52dee6da-4350-4ff9-a9e5-309ce2880721",

    # 服务配置文件
    "service_file_list": [
        "app/assets/app_factory/app/service.json",
        "app/src/main/java/com/nd/smartcan/appfactory/generate/G_app_service.java",
        "app/src/main/java/com/nd/sdp/conf/impl/ServiceConfigImpl.java",
        # 可以根据需要添加更多文件路径
    ],

    "local_integrate_lib": [
        "com.nd.xst:llp-userinfo:",
        "com.nd.sdp.android:llp-x-user-android:",
        "com.nd.sdp.android:llp-x-cloud-assemble-android:",
        "com.nd.sdp.android:xst-coursehour:",
        "com.nd.sdp.android:llp-xst-course:",
    ]
}
