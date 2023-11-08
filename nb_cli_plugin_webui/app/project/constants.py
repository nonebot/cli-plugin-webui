class ErrorCode:
    PROJECT_NOT_FOUND = "NoneBot 实例不存在"
    PROJECT_DIR_NOT_DIR = "NoneBot 实例目录不存在"
    PROJECT_DELETE_FAILED = "NoneBot 实例删除失败"
    PROJECT_WRITE_PROFILE_FAILED = "NoneBot 实例信息写入失败"
    PROJECT_TOML_NOT_FOUND = "实例 pyproject.toml 文件不存在"

    TOML_PROJECT_NAME_NOT_FOUND = "未找到项目名称"
    TOML_ADAPTERS_NOT_FOUND = "未找到适配器"
    TOML_PLUGINS_NOT_FOUND = "未找到插件"
    TOML_PLUGIN_DIRS_NOT_FOUND = "未找到插件目录"
    TOML_BUILTIN_PLUGINS_NOT_FOUND = "未找到内置插件"


class Constants:
    TOML_CHECK_SUCCESS = "检查通过"
