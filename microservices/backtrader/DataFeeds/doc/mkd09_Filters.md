- [Data Feeds - Filters](#data-feeds---filters)
  - [Purpose](#purpose)
  - [Filters at work](#filters-at-work)
  - [Filter Interface](#filter-interface)
  - [A Sample Filter](#a-sample-filter)
  - [Data Pseudo-API for Filters](#data-pseudo-api-for-filters)
  - [Another example: Pinkfish Filter](#another-example-pinkfish-filter)
---------------------------------------
# Data Feeds - Filters 
此功能是 `backtrader` 添加的相对较晚的功能，已经安装到存在的内部组件中。这使得它不像所希望的那样灵活，并且具有100%完整的功能，但是在许多情况下仍然可以达到目的。

尽管该实现尝试允许即插即用过滤器链接，但由于预先存在的内部结构，很难确保始终能够实现这一点。因此，一些过滤器可能是连锁的，而另一些则不是。

## Purpose

* 转换 data Feed 的值, 以提供一个不同的 data Feed

开始实现是为了简化 cerebro API 直接使用的两个明显的过滤器。他们是：

* `Resampling`（`cerebro.resampledata`）    
  在这里，过滤器变换输入 data feed 的 `timeframe` 和 `compression` 。例如：

    > (Seconds, 1) -> (Days, 1)

    这意味着原始 data feed 是分辨率为1秒的 bars。该重采样滤波器截取数据并对其进行缓冲，直到它可以提供一个1 Day bar。这将发生在第二天的1秒条出现时。

* `Replaying` （`cerebro.replaydata`）  
  对于与上述相同的时间范围，过滤器将使用1秒分辨率重建 1 day bar。
  
  这意味着 1 day bar 的发送次数与 1 second bar 的发送次数一样多，并已更新为包含最新信息。
  
  例如，这模拟了实际交易日的发展方式。
  
  > 注意    
  > len(data)只要日期不改变，数据的长度以及策略的长度就保持不变。

## Filters at work
给定一个现有的数据源/源，您可以使用数据源的addfilter方法：
```
data = MyDataFeed(dataname=myname)
data.addfilter(filter, *args, **kwargs)
cerebro.addata(data)
```
甚至它可以兼容 resample/replay 过滤，以下可以这么操作:
```
data = MyDataFeed(dataname=myname)
data.addfilter(filter, *args, **kwargs)
cerebro.replaydata(data)
```

## Filter Interface
filter必须符合以下接口定义

* 一个可调用对象，它接受该签名
  > callable(data, *args, **kwargs)

或者

* 一个类能被实例，实例能被调用

    * 实例化的 `__init__` 方法必须支持如下签名:
    ```
    def __init__(self, data, *args, **kwargs)
    ```

    * `__call__` 方法签名如下:
    ```
    def __call__(self, data, *args, **kwargs)
    ```
    从 data feed 传进来的每一个新的值都将调用实例。`*args` 和 `*kwargs` 与 `__init__` 方法中一致

    返回值:
    

## A Sample Filter
## Data Pseudo-API for Filters
## Another example: Pinkfish Filter