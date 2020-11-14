# Exceptions
设计目标之一是尽早退出，让用户完全了解发生错误的情况。目的是强迫自己拥有将在异常情况下中断并强制重新访问受影响部分的代码。

但是时间到了，某些异常可能会慢慢出现在平台中。

# Hierarchy
所有异常的基类是 `BacktraderError` (它是Exception的一个直接子类)

# Location
1. 在 errors 模块内, 可以直接使用:
    ```
    import backtrader as bt

    class Strategy(bt.Strategy):

        def __init__(self):
            if something_goes_wrong():
                raise bt.errors.StrategySkipError
    ```
2. 直接从 backtrader 中使用
    ```
    import backtrader as bt

    class Strategy(bt.Strategy):

        def __init__(self):
            if something_goes_wrong():
                raise bt.StrategySkipError
    ```
# Exceptions
## StrategySkipError
请求平台跳过此策略进行回测。在实例的初始化(__init__)阶段引发
