# 通用资源爬虫框架
- 爬取垂直类网站资源框架
- 作者：tieqiang Xu
- 创建时间:2018.01.26
- 欢迎fork，请给star，O(∩_∩)O~

# TODO Plan
- 将25分钟前state=doing的task，置为ready状态（25分钟非固定，可配置时间）
- 1小时没有新任务，则认为所有task执行完成（1小时非固定，可配置时间）
- 支持PhantomJS浏览器

# 安装运行环境
- Anaconda3(python3.6.3)
- Mongodb3数据
- pip install pymongo

# 主要特性
- 业务流程：Main入口 -> Scheduler任务调度器模块 -> Downloader下载器模块 -> Parser页面解析器模块 -> Pipelline资源存储管道模块
- 多进程访问网络、多线程日志
- 推荐使用 lml.xpath 与 regexp 配合做网页解析（万能组合）
- 支持断点续爬（task级）

# 源码结构说明
|文件/文件夹 |功能 |
|--------   | :----- |
|[configs] |配置集|
|....configs.ini |运行时可变的配置 |
|....Settings.py |运行时不可变的配置 |
|[utils] |工具集 |
|....ConfigUtils.py |读写configs/configs.ini的工具类 |
|....HttpUtils.py |访问http/https的工具类 |
|....InitUtils.py |任务初始化工具类(调试用) |
|....LogUtils.py |日志处理工具类 |
|....MongoUtils.py |Mongo连接和增删改查工具类 |
|....TaskUtils.py |Task任务操作工具类 |
|Main.py |项目入口 |
|Scheduler.py |任务调度器模块 |
|Downloader.py |下载器模块 |
|Parser.py |页面解析器模块 |
|Pipeline.py |资源存储管道模块 |

- 更详细的说明见源码内注释

# 数据结构(Mongodb)
#### 1. tasks
```
[{
    "_id" : ObjectId("5a6af4a957215754f04e66d4"),
    "state" : "ready",
    "parser" : "demo",
    "request" : "http://news.baidu.com",
    "response" : "<html>...</html>",
    "result" : [{
        "id":"...",
        "name":"...",
        "...":"..."
    }]
    "parent" : {
        "parent_id" : "http://www.baidu.com",
        "parent_name" : "百度首页"
    },
    "uptime" : "2018-01-26 17:28:09.071",
    "uptimestamp" : NumberLong("1516958889071")
}]
```
|字段名 |类型 |含义 |
|--------------   | :----- | :----- |
|_id |number|主键（由Mongodb自动生成）|
|state |string |任务状态。ready-随时待命,doing-正在爬取,done-爬取完成 |
|parser |string |解析器名称。根据不同的网站自己定义，例如：category-分类，list-列表，details-详情，page-分页，等 |
|request |string |要爬取的url地址 |
|[response] |string |返回的html |
|[result] |list<map> |解析的资源结果 |
|...id |string |资源id |
|...name |string |资源名称 |
|...<...> |string |资源的其它属性 |
|[parent] |map |父结点信息（用于表数据关联） |
|....parent_id |string |父结点id |
|....parent_name |string |父结点名称 |
|[uptime] |string |更新时间（插入时自动构建，用于历史追溯） |
|[uptimestamp] |number |更新时间戳（插入时自动构建，用于历史追溯筛选条件、排序） |

- 注1：第1个task在Scheduler模块调用TaskUtils构建方法时创建（根据Settings.py的配置）；之后的task由Parser模块创建
- 注2：task从Scheduler模块中读取，在Scheduler模块、Downloader模块、Parser模块、Pipeline模块中按顺序传递，每个模块都把自己执行的结果写入task，以供下一个模块使用
- 注3：Scheduler模块负责写入第1个task、读取ready的task，并将取出的task的state置为doing状态；
- 注4：Downloader模块负责读取task的paser和request，并将结果写入response；
- 注5：Parser模块负责读取task的paser和response，并将结果写入result，同时也应该生成下一次task的paser和request,将下一次任务写入mongodb；
- 注6：Pipline模块负责读取task的paser和result，并将结果写入mongodb，同时将本次task的state置为done状态

#### 2. logs
```
{
    "_id" : ObjectId("5a6af48157215754ec49e02e"),
    "timestring" : "2018-01-26 17:27:29.745",
    "timestamp" : NumberLong("1516958849745"),
    "level" : "DEBUG",
    "pid" : 21740,
    "source" : "insert(),MongoUtils.py:124",
    "text" : "insert success!"
}
```
|字段名 |类型 |含义 |
|--------------   | :----- | :----- |
|_id |number|主键（由Mongodb自动生成）|
|timestring |string |日志时间 |
|timestamp |number |日志时间戳 |
|level |string |日志级别，DEBUG、INFO、WARN、ERROR |
|pid |number |进程id |
|source |string |源码定位。格式：函数,文件名:行号 |
|text |string |日志内容 |

# 开发步骤与过程指导
#### 第1步：目标网站分析
- 分析待爬取网站的分类信息、列表信息、详情信息、分页信息等资源
- 规划每种信息的[parser-解析器名称]，[request-请求url]， [result-结果格式] 三要素
- 使用chrome的F12神器，编写、检验各种元素定位的xpath及regexp
#### 第2步：修改初始配置configs
- 修改configs/conifgs.ini，手动配置"任务间隔秒数"、"日志显示级别"等
- 修改configs/Settings.py, 手动配置"Mongodb连接参数"、"初始task的解析器、url"等

#### 第3步：编写Downloader代码逻辑
- 修改Downloader.run()代码，按self.task[parser]值做分发调用本类函数
- 创建各parser对应的函数，在函数内使用HttpUtil访问self.task[request]字段值，将结果写入self.task[response]内

### 第4步：编写Parser代码逻辑
- 修改Parser.run()代码，按self.task[parser]值做分发调用本类函数
- 创建各parser对应的函数，在函数内使用xpath和regexp解析self.task[response]字段值，将解析结果写入self.task[result]内;同时解析出下一次task的parser和request，写入mongodb的tasks集合中

### 第5步：编写Pipline代码逻辑
- 修改Downloader.run()代码，按self.task[parser]值做分发调用本类函数
- 创建各parser对应的函数，在函数内访问self.task[result]字段值写入MongoDB内

### 第6步：循环3-5步完成开发
- 调试单个parser的下载/解析/存储时，建议从Downloader开始运行DEBUG模式，不必从Main.py开始执行，因为Scheduler内的死循环和多进程，会增加调试难度
- 访问http/https时需要特殊proxy、user-agent、cookie时，请修改HttpUtils中的get_proxy()、get_useragent()、get_cookie()及Downloader中的代码
- 控制台输出日志时尽量不要使用系统内置的print()，请使用LogUtils.log的d()、i()、w()、e()，它提供了更详尽的输出信息，并且日志也会被记录到mongodb的logs集合中，便于追溯
- 执行过程中如果中途断掉，会产生state=doing的task，请在task全部执行完毕后将它们置为ready状态

# xpath经验集
- chrome的F12神器测试xpath命令：$x('xpath路径规则')

# regexp经验集

