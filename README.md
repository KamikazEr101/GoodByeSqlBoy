# GoodbyeSqlBoy
GoodbyeSqlBoy是一个基于AutoGen与FastApi搭建的根据自然语言生成sql语句的框架

以下是它的特点：

- 对外暴露端口，支持不同语言框架的调用
- 内部不集成任何ORM框架，考虑到框架的跨语言性，防止与其他事务管理框架冲突，于是采用轻量化的设计理念，不与数据库进行任何交互
- 生成的sql语句的准确性与查询效率是可以被调整的，根据参数去决定是否开启optimize agent进行sql准确性的提升与慢sql的优化
- 基于redis进行sql语句的缓存，减少响应耗时(可选, 根据参数调整是否开启)

**note**：关于第四点的实现，是基于框架的设计理念的，框架的实际运行是结合其他框架对本框架的端口发送post请求，postbody内容属于硬编码，故本框架内部采用sha256对自然语言进行加密存入redis，而不再使用多余的agent进行键的匹配


# v0.1
## QuickStart:
### 0. 初始化配置
在项目根目录下创建.env文件, 
按照.example_env文件中的配置项进行配置, 并将想要生成SQL语句的表的DDL建表SQL文件放在指定目录下(如果没有, 就直接照着.example_env文件的SQL_FILE_PATH设定, 
将最后一层路径设置为项目中的resource文件夹, 注意前面的路径要改成自己电脑中的绝对路径. resource文件中已放了两个建表SQL, 是经典的员工+部门多对一关系表)
启动main.py
#### 人话:  将.example_env文件名改成.env, 将SQL_FILE_PATH除了resource的最后一层目录以外全改为自己电脑放这个项目的地址, 然后运行main.py

### 1. 通过HTTP请求对外暴露的接口进行交互(若用不到, 则转2)
在启动main.py后, 对  http://localhost:8000/api/v1/nl2sql  发送post请求, 请求体规定为json格式, 属性只有一个 -> "query"(自然语言), 可进入schemas模块查看具体定义
### 2. 通过控制台标准输入输出流进行交互
在.env文件中, 将CONSOLE_INPUT配置设为True(和.example_env文件写法一样), 输入想要进行的查询的自然语言(人话), 看到控制台中输出agent的执行流程, 等待最后结果即可

## 没有redis / 用不到redis 怎么办:

和.example_env文件写法一样, 将自己在项目根目录下的.env文件中, 将`ENABLE_REDIS`参数设为False