- [Extending a Datafeed](#extending-a-datafeed)
  - [Plotting that extra P/E line](#plotting-that-extra-pe-line)

------------------------------------------------
# Extending a Datafeed
让我们以CSV数据Feed开发和GenericCSVData示例示例为基础。

步骤：

* 假设在解析的CSV数据中设置了`P/E`信息
* 使用`GenericCSVData`作为基类
* 扩展存在的行（open/high/low/close/volumen/openinterest） `pe`
* 添加参数，以使调用者确定`P/E`信息的列位置

结果：
```
from backtrader.feeds import GenericCSVData

class GenericCSV_PE(GenericCSVData):

    # Add a 'pe' line to the inherited ones from the base class
    lines = ('pe',)

    # openinterest in GenericCSVData has index 7 ... add 1
    # add the parameter to the parameters inherited from the base class
    params = (('pe', 8),)
```

之后在策略中使用这个data feed
```
import backtrader as bt

....

class MyStrategy(bt.Strategy):

    ...

    def next(self):

        if self.data.close > 2000 and self.data.pe < 12:
            # TORA TORA TORA --- Get off this market
            self.sell(stake=1000000, price=0.01, exectype=Order.Limit)
    ...
```

## Plotting that extra P/E line
显然，数据提要中没有多余的自动绘图功能。

最好的选择是在该行上执行 `SimpleMovingAverage` 并将其绘制在单独的轴上：
```
import backtrader as bt
import backtrader.indicators as btind

....

class MyStrategy(bt.Strategy):

    def __init__(self):

        # The indicator autoregisters and will plot even if no obvious
        # reference is kept to it in the class
        btind.SMA(self.data.pe, period=1, subplot=False)

    ...

    def next(self):

        if self.data.close > 2000 and self.data.pe < 12:
            # TORA TORA TORA --- Get off this market
            self.sell(stake=1000000, price=0.01, exectype=Order.Limit)
    ...
```