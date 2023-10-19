
# **进阶应用**

logging库提供了模块化的方法和几个组件，下列列出了模块定义的基础类和函数

- Loggers ：记录器公开应用程序代码直接使用的接口。
- Handlers ：处理程序将日志记录（由记录器创建）发送到相应的目标。
- Filters ：过滤器提供了更细粒度的工具，用于确定要输出哪些日志记录。
- Formatters： 格式化程序指定最终输出中日志记录的布局。

```python
logger = logging.getLogger(__name__)
```

1）logger对象方法

Logger.setLevel(level)：设置Logger对象日志消息级别

Logger.addHandler(hdlr)：为Logger对象添加handler对象

Logger.removeHandler(hdlr)：为Logger对象移除handler对象

Logger.hasHandlers()：判断是否有处理器

Logger.addFilter(filter)：为Logger对象添加filter对象

Logger.removeFilter(filter)：为Logger对象移除filter对象