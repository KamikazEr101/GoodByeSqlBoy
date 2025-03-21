import os
from config import settings

# 读取sql建表语句的tool
def read_sql_file() -> str:
    path_ = settings.SQL_FILE_PATH
    sql_contents=''

    # 如果传入的是文件路径
    if os.path.isfile(path_) and path.endswith('.sql'):
        # 读取单个 SQL 文件
        with open(path_, 'r', encoding='utf-8') as file:
            sql_contents+=file.read()

    # 如果传入的是目录路径
    elif os.path.isdir(path_):
        # 遍历目录中的所有 SQL 文件
        for file_name in os.listdir(path_):
            if file_name.endswith('.sql'):
                file_path = os.path.join(path_, file_name)
                # 读取 SQL 文件
                with open(file_path, 'r', encoding='utf-8') as file:
                    sql_contents+=file.read()

    return "数据库的表结构如下, 请根据此结构生成或优化SQL: \n" + sql_contents
