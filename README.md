# 通用资源爬虫框架
- 爬取垂直类网站资源框架
- 作者：tieqiang Xu
- Email: 805349916@qq.com
- 创建时间:2018.01.26
- 欢迎fork，请给star，O(∩_∩)O~

# TODO Plan
- 继承Parser编写相应的函数的开发机制
- use_agent、proxy、cookie、header可配置
- 将25分钟前state=doing的task，置为ready状态（25分钟非固定，可配置时间）
- 1小时没有新任务，则认为所有task执行完成（1小时非固定，可配置时间）
- 支持PhantomJS浏览器解析js、302跳转
- mongo连接失败友好提示给用户
- 运行InitUtils不能自动结束进程（LogUtils中的线程队列死循环导致）
- 常见网站登录的插件化（微博等）
- 验证码识别插件（深度学习）

# 安装运行环境
- Anaconda3(python3.6.3)
- Mongodb3数据
- pip install pymongo
- 不需要初始化mongodb库，首次运行项目时会自动检测并初始化数据库

# 主要特性
- 业务流程：Main入口 -> SchedulerX任务调度器模块 -> DownloaderX下载器模块 -> ParserX页面解析器模块 -> PipellineX资源存储管道模块
- 多进程访问网络、多线程日志
- 推荐使用 lml.xpath 与 regexp 配合做网页解析（万能组合）
- 支持断点续爬（task级）

# 源码结构说明
|文件/文件夹 |功能 |
|--------   | :----- |
|[configs] |配置集|
|....config.ini |运行时可变的配置 |
|....Setting.py |运行时不可变的配置 |
|[modules] |模块集 |
|....SchedulerX.py |任务调度器模块 |
|....DownloaderX.py |下载器模块 |
|....ParserX.py |页面解析器模块 |
|....PipelineX.py |资源存储管道模块 |
|[utils] |工具集 |
|....ConfigUtil.py |读写configs/config.ini的工具类 |
|....HttpUtil.py |访问http/https的工具类 |
|....InitUtil.py |任务初始化工具类(调试用) |
|....LogUtil.py |日志处理工具类 |
|....MongoUtil.py |Mongo连接和增删改查工具类 |
|....RegexpUtil.py |正则表达式工具类 |
|....TaskUtil.py |Task任务操作工具类 |
|....XpathUtil.py |Xpath工具类 |
|Main.py |项目入口（从这里开始运行/调试） |
|README.md |安装、使用、开发详细说明 |

- 更详细的说明见源码内注释

# 数据结构(MongoDB)
#### 1. tasks集合
```
[{
    "_id" : ObjectId("5a6af4a957215754f04e66d4"),
    "state" : "ready",
    "parser" : "demo",
    "request" : "http://news.baidu.com",
    "table" : "demo_info"
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
|table |string |存储解析结果的表名 |
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

- 注1：第1个task在SchedulerX模块调用TaskUtils的构造方法时创建（根据Settings.py的配置），之后的task由Parser模块创建；
- 注2：task从SchedulerX模块中读取，在SchedulerX模块、DownloaderX模块、ParserX模块、PipelineX模块中按顺序传递，每个模块都把自己执行的结果写入task，以供下一个模块使用；
- 注3：SchedulerX模块负责写入第1个task、读取ready的task，并将取出的task的state置为doing状态；
- 注4：DownloaderX模块负责读取task的paser和request，并将结果写入response；
- 注5：ParserX模块负责读取task的paser和response，并将结果写入task的results，同时也应该生成下一次task的paser和request,将下一次任务写入task的next_tasks；
- 注6：PiplineX模块负责读取task的paser、results、next_tasks，并将results解析结果及next_tasks下次任务集写入mongodb，同时将本次task的state置为done状态；

#### 2. logs集合
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
- 规划每种信息的[parser-解析器名称]，[request-请求url]， [result-结果格式], [table-存储的表名] 四要素
- 使用chrome的F12神器，编写、检验各种元素定位的xpath及regexp
#### 第2步：修改初始配置configs
- 修改configs/conifg.ini，手动配置"任务间隔秒数"、"日志显示级别"等
- 修改configs/Setting.py, 手动配置"Mongodb连接参数"、"初始task的解析器、url、table"等

#### 第3步：编写DownloaderX代码逻辑
- 如果是标准的http/https get请求，则不需要编写DownloaderX的逻辑，保持现状即可自动调用download_default()函数下载访问http资源，直接跳到第4步
- 如果有特殊的http/https访问需求,则创建download_<parser名>()函数，在该函数内使用HttpUtil访问self.task[request]字段值，将结果写入self.task[response]内

### 第4步：编写ParserX代码逻辑
- 本模块一般不可省略，需要自行创建函数，完成解析网页的过程，函数完成两项任务：一是解析出本期的结果列表存入self.task[results]，二是解析出下次的任务列表存入self.task[next_tasks]
- 创建各parse_<parser名>()函数，在函数内使用xpath和regexp解析self.task[response]字段值，将解析结果写入self.task[results]内; 同时解析出下一次task的parser、request、table、parent，存入task的next_tasks列表中

### 第5步：编写PiplineX代码逻辑
- 如果是标准的mongodb写入，则不需要编写本模块的逻辑，保持现状即可自动调用pipline_default(),自动保存task的results到mongodb，自动保存next_tasks到mongodb,自动将最终的task更新到mongodb，自动将本次任务的状态置为done
- 如果有特殊的存储要求，则创建pipline_<parser名>()函数，在该函数内访问self.task[result]字段值写入MongoDB内、其它有关task的存储任务是自动完成的，不需要自己处理

### 第6步：循环3-5步完成开发
- 调试单个parser的下载/解析/存储时，建议从DownloaderX开始运行DEBUG模式，不必从Main.py开始执行，因为SchedulerX内的死循环和多进程，会增加调试难度
- 访问http/https时需要特殊proxy、user-agent、cookie时，请修改HttpUtils中的get_proxy()、get_useragent()、get_cookie()及DownloaderX中的代码
- 控制台输出日志时尽量不要使用系统内置的print()，请使用LogUtil.Log的d()、i()、w()、e()，它提供了更详尽的输出信息，并且日志也会被记录到mongodb的logs集合中，便于追溯
- 执行过程中如果中途断掉，会产生state=doing的task，请在task全部执行完毕后将它们置为ready状态
- 调试过程中需要经常初始化数据库，运行utils/InitUtil可以快速初始化，或者直接调用InitUtil的init()方法

# xpath经验集
- 【教程】 W3的xpath英文规范：https://www.w3.org/standards/techs/xpath#w3c_all
- 【教程】 W3cschool的中文教程： http://www.w3school.com.cn/xpath/index.asp
- 【教程】 微软的xpath中文示例： https://msdn.microsoft.com/zh-cn/library/ms256086(v=vs.120).aspx
- 【经验】 chrome的F12神器测试xpath命令：$x('xpath路径规则')

# regexp经验集
- 【教程】 菜鸟教程之正则表达式 http://www.runoob.com/regexp/regexp-syntax.html
- 【教程】 正则表达实验室教程  http://www.regexlab.com/zh/regref.htm
- 【教程】 正则表达式在线测试 http://tool.oschina.net/regex/
- 【经验】 使用正则表达式解析出赞的数量，注意要转换所有的&nbsp为标准空格，并去掉前后的空格
```
ptext='<p>本资源被赞了 35&nbsp;&nbsp; 次</p>'
m = re.findall(r"赞了(.+?)次", ptext)
cnt=m[0].replace('\xc2\xa0',' ').strip()
```
