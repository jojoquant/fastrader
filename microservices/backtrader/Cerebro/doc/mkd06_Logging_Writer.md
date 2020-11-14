# Writer
向流中写出以下内容：

* 带有数据源，策略，指标和观察者的CSV流

    哪些对象实际上进入CSV流可以与控制 csv每个对象的（默认为True属性data feeds和 observers/假的indicators）

* 属性摘要

    * Data Feeds
    * Strategies (lines and parameters)
    * Indicators/Observers: (lines and parameters)
    * Analyzers: (parameters and analysis outcome)

仅定义了一个叫做 WriterFile 的 Writer，可以将其添加到系统中：

* 通过将 cerebro 的参数 `writer` 设置为 `True`

    一个标准 `WriterFile` 将被实例化

* 通过调用 `Cerebro.addwriter(writerclass, **kwargs)`

    `writerclass` 将在使用给定的 `kwargs`参数, 在回测执行过程中进行实例化

    由于标准 `WriterFile` 默认不输出 csv，下面的 addwriter 调用会设置它：
    ```
    cerebro.addwriter(bt.WriterFile, csv=True)
    ```

# Reference
```
class backtrader.WriterFile()
```
系统级的 writer 类

它可以设置的参数如下:
* `out` (default: `sys.stdout`): 写输出流到哪里     
    如果传入一个字符串, 应该是 filename
If a string is passed a filename with the content of the parameter will be used

* `close_out` (default: `False`)  
    如果out是一个流，是否必须由编写者显式关闭它

* `csv` (default: `False`)      
    是否为csv流，执行时将datafeeds, 策略，观察者和指标写入流中

    可以使用csv每个对象的属性控制哪些对象实际进入csv流（默认值为True, data feeds和observers; False 为 indicators）

* `csv_filternan` (default: `True`)     
    是否将nan值从csv流中剔除(替换为一个空的字段)

* `csv_counter` (default: `True`)   
    writer是否保留和打印输出的行数

* `indent` (default: `2`)       
    每级的缩进空格数

* `separators` (default: `['=', '-', '+', '*', '.', '~', '"', '^', '#']`)       
    用于分 节/子（sub）节的行分隔符的字符

* `seplen` (default: 79)        
    包括缩进的行分隔符的总长度

* `rounding` (default: `None`)      
    四舍五入到小数点后的位数。None表示没有进行舍入
