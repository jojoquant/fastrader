- [Cerebro - Optimization - Improvements](#cerebro---optimization---improvements)
  - [Data Feed Management](#data-feed-management)
  - [Results management](#results-management)
  - [Some test runs](#some-test-runs)
    - [Single Core Run](#single-core-run)
    - [Multiple Core Runs](#multiple-core-runs)
  - [Concluding](#concluding)
  - [Sample Usage](#sample-usage)

-------------------------------------------------------------
# Cerebro - Optimization - Improvements
version 1.8.12.99 backtrader 囊括了一个在多进程下 data feeds 和 结果管理的提升

通过 Cerebro 两个新的参数来控制:
* `optdatas` (default: `True`)    
    如果为 `True`, 优化(系统预预加载并使用 runonce), 数据只做一次预先加载到主进程中, 省时间和系统开销

* `optreturn` (default: `True`)   
    如果为 True, 优化结果将不是 Strategy 对象(全部datas, indicators, observers, ...), 而是带有以下属性的对象(和Strategy中一样):

    * `params` (or `p`) , 已经执行的策略的

    * `analyzers` , 已经执行的策略的

    大多数情况下, 只有 analyzers 和 需要去评估策略表现的参数. 如果需要(比如)indicators 生成值的详细分析, 把该参数设置为 `False`

## Data Feed Management
在优化场景下, 这可能是一个与 Cerebro 参数的组合:

* `preload=True` (default)    
  Data feeds 在运行回测前被预加载

* `runonce=True` (default)
  Indicators 将在 batch mode下(紧密的循环)被计算, 而不是 step by step

如果以上都为`True`, 同时 `optdatas=True`, 之后:
* data feeds 将在主进程中进行预加载, 在 spawn 新的子进程之前(子进程负责执行回测)

## Results management
在优化场景下, 当评估策略使用不同参数时, 有个两个东西非常重要:

* `strategy.params` (or `strategy.p`)   
  回测使用的参数值

* `strategy.analyzers`    
  该对象负责提供对策略表现的评估. 比如: `SharpeRatio_A` (年化的 SharpeRatio)

当 `optreturn=True`, 将创建占位符对象，而不是返回完整的策略实例，该占位符对象带有上述两个属性以进行评估。

这避免了回传大量(例如在由指示符生成的值)生成的数据的回测

如果需要完整的策略对象，只需 `optreturn=False` 在`Cerebro`实例化过程中或执行时设置`cerebro.run` 即可

## Some test runs
backtrader源中的优化示例可以通过添加和控制`optdatas` 和 `optreturn` （实际上是禁用它们）进行扩展

### Single Core Run
cpu数量限制为1且未使用多处理模块时发生了什么, 实例如下:
```
$ ./optimization.py --maxcpus 1
==================================================
**************************************************
--------------------------------------------------
OrderedDict([(u'smaperiod', 10), (u'macdperiod1', 12), (u'macdperiod2', 26), (u'macdperiod3', 9)])
**************************************************
--------------------------------------------------
OrderedDict([(u'smaperiod', 10), (u'macdperiod1', 13), (u'macdperiod2', 26), (u'macdperiod3', 9)])
...
...
OrderedDict([(u'smaperiod', 29), (u'macdperiod1', 19), (u'macdperiod2', 29), (u'macdperiod3', 14)])
==================================================
Time used: 184.922727833
```

### Multiple Core Runs
在不限制CPU数量的情况下，`Python multiprocessing` 模块将尝试使用所有CPU 。optdatas 和 optreturn 将被禁用

optdata 和 optreturn 都为True
```
$ ./optimization.py
...
...
...
==================================================
Time used: 56.5889185394
```
通过 多核 和 datafeed 以及结果的全面改进, 意味着从 184.92秒 缩短1到了 56.58秒。

考虑到样本使用的是252个bars，并且指标仅生成​​带有252个点的长度。这只是一个例子。

实际问题是新行为提升了多少

只把 `optreturn` 禁用

让我们把所有策略再运行一次
```
$ ./optimization.py --no-optreturn
...
...
...
==================================================
Time used: 67.056914007
```
执行时间增加了 18.50%

只把 `optdatas ` 禁用, 每个子进程强制加载各自的datafeeds:
```
$ ./optimization.py --no-optdatas
...
...
...
==================================================
Time used: 72.7238112637
```
执行时间增加了 28.52%

`optreturn` 和 `optdatas ` 都禁用

只使用多核, 不使用新的提升改进行为:
```
$ ./optimization.py --no-optdatas --no-optreturn
...
...
...
==================================================
Time used: 83.6246643786
```
执行时间增加了 47.79%

这表明使用多核是提高时间的主要原因
> 这些执行都是在一台i7-4710HQ(4核/ 8逻辑)、16 g字节RAM、Windows 10 64位的笔记本电脑上完成的。在其他条件下，行驶里程可能有所不同


## Concluding
* 优化过程中减少时间的最大因素是使用多核

* 该示例运行时，`optdatas` 和 `optreturn` 显示了大约 22.19% 和 15.62% 每个（32.34%在测试中一起）的加速

## Sample Usage
```
$ ./optimization.py --help
usage: optimization.py [-h] [--data DATA] [--fromdate FROMDATE]
                       [--todate TODATE] [--maxcpus MAXCPUS] [--no-runonce]
                       [--exactbars EXACTBARS] [--no-optdatas]
                       [--no-optreturn] [--ma_low MA_LOW] [--ma_high MA_HIGH]
                       [--m1_low M1_LOW] [--m1_high M1_HIGH] [--m2_low M2_LOW]
                       [--m2_high M2_HIGH] [--m3_low M3_LOW]
                       [--m3_high M3_HIGH]

Optimization

optional arguments:
  -h, --help            show this help message and exit
  --data DATA, -d DATA  data to add to the system
  --fromdate FROMDATE, -f FROMDATE
                        Starting date in YYYY-MM-DD format
  --todate TODATE, -t TODATE
                        Starting date in YYYY-MM-DD format
  --maxcpus MAXCPUS, -m MAXCPUS
                        Number of CPUs to use in the optimization
                          - 0 (default): use all available CPUs
                          - 1 -> n: use as many as specified
  --no-runonce          Run in next mode
  --exactbars EXACTBARS
                        Use the specified exactbars still compatible with preload
                          0 No memory savings
                          -1 Moderate memory savings
                          -2 Less moderate memory savings
  --no-optdatas         Do not optimize data preloading in optimization
  --no-optreturn        Do not optimize the returned values to save time
  --ma_low MA_LOW       SMA range low to optimize
  --ma_high MA_HIGH     SMA range high to optimize
  --m1_low M1_LOW       MACD Fast MA range low to optimize
  --m1_high M1_HIGH     MACD Fast MA range high to optimize
  --m2_low M2_LOW       MACD Slow MA range low to optimize
  --m2_high M2_HIGH     MACD Slow MA range high to optimize
  --m3_low M3_LOW       MACD Signal range low to optimize
  --m3_high M3_HIGH     MACD Signal range high to optimize
```