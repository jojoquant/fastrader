- [Using Indicators](#using-indicators)
  - [Indicators in action](#indicators-in-action)
  - [__init__ vs next](#init-vs-next)
    - [During __init__](#during-init)
    - [During next](#during-next)
    - [The __init__ vs next why](#the-init-vs-next-why)
  - [Some notes](#some-notes)
  - [Indicator Plotting](#indicator-plotting)
    - [Controlling plotting](#controlling-plotting)
- [Indicators - Development](#indicators---development)
- [Indicators - Timeframe Mixing](#indicators---timeframe-mixing)
- [Indicators - Reference](#indicators---reference)
- [Indicators - ta-lib](#indicators---ta-lib)
- [Indicators - ta-lib - Reference](#indicators---ta-lib---reference)


----------------------------------------
# Using Indicators
指标在平台中的两个地方使用
* Inside Strategies
* Inside other Indicators

## Indicators in action
1. 指标在策略的`__init__`中被实例化
2. 指标值(或其派生值)将在 `next` 期间使用/检查

有一个重要的点需要考虑:
* 在调用 `next` 之前，将预先计算在初始化期间声明的任何 `Indicator`（或其派生的值）

我们一起来操作下不同的模式

## __init__ vs next
* 在 __init__ 期间，任何设计操作 `lines` 对象都会生成另一个 `lines` 对象
* 在 `next` 中，操作涉及的任何 `lines` 对象，都会生成常规的 Python 类型，比如 float 和 bools

### During __init__
一个在 __init__ 期间的操作的示例:
```
hilo_diff = self.data.high - self.data.low
```
变量 hilo_diff 持有一个对 lines 对象的引用，该对象在调用next之前被预先计算过，可以使用标准数组符号[]对其进行访问

它显然包含了 data feed 的每一个 bar 的 high 和 low 之差。

这也适用于混合简单的 lines (如 self.data 的 data feed)和指标等复杂数据:
```
sma = bt.SimpleMovingAverage(self.data.close)
close_sma_diff = self.data.close - sma
```
现在 `close_sma_diff` 又包含了一个 line 对象

使用逻辑运算符:
```
close_over_sma = self.data.close > sma
```
现在生成的 lines 对象将包含一个 booleans 数组

### During next
一个操作(逻辑运算符)的例子:
```
close_over_sma = self.data.close > self.sma
```
使用等效数组(基于索引0的符号):
```
close_over_sma = self.data.close[0] > self.sma[0]
```
在这种情况下，`close_over_sma` 生成一个boolean，这是比较两个浮点值的结果，[0]运算符返回的值应用于self.data.close以及self.sma

### The __init__ vs next why
逻辑简化(以及易于使用)是关键。计算和大部分相关的逻辑可以在__init__期间声明，在 `next` 期间保持实际的操作逻辑最简化。

实际上还有一个好处:速度(由于在开始时解释了预先计算)

一个完整的例子，在 `__init__` 产生买入信号:
```
class MyStrategy(bt.Strategy):

    def __init__(self):

        sma1 = btind.SimpleMovingAverage(self.data)
        ema1 = btind.ExponentialMovingAverage()

        close_over_sma = self.data.close > sma1
        close_over_ema = self.data.close > ema1
        sma_ema_diff = sma1 - ema1

        buy_sig = bt.And(close_over_sma, close_over_ema, sma_ema_diff > 0)

    def next(self):

        if buy_sig:
            self.buy()
```
> 注意  
> Python 的 `and` 操作符不能被重写，这迫使平台定义自己的 `And`。同样的道理也适用于其他结构，比如 `Or` 和 `If` 

很明显，在 __init__ 期间的“声明性”方法将 `next` 的代码长度（实际的策略工作发生的地方）保持在最小程度。

（别忘了还有加速因素）

> 当逻辑变得非常复杂并涉及多个操作时，通常最好将其封装在一个 `Indicator` 中。

## Some notes
在上面的例子中，与其他平台相比，backtrader简化了两个方面:

  * 声明的指标既没有父参数(就像创建它们的策略一样)，也没有调用任何的“注册”方法/函数。
    
    尽管如此，由于操作(如sma - ema)，策略还是会驱动指标的计算和任何 lines 对象的生成。

  * `ExponentialMovingAverage` 实例化时不需要 `self.data`

    这是故意的。如果没有传递数据，父节点的第一个数据(在本例中是创建的策略也就是self.data)将自动在后台传递

## Indicator Plotting
首先:
* 声明的指标将自动绘制（如果cerebro.plot被调用）

* 不打印来自操作的 lines 对象(比如 close_over_sma = self.data.close > self.sma ), 有一个辅助的 `LinePlotterIndicator` ，可根据需要使用以下方法绘制这些操作：
    ```
    close_over_sma = self.data.close > self.sma
    LinePlotterIndicator(close_over_sma, name='Close_over_SMA')
    ```
    name 参数为该 indicator 保留的 单个line 的命名

### Controlling plotting
在指示器的开发过程中，可以添加 `plotinfo` 声明。它可以是元组（2个元素）、dict或OrderedDict。它看起来像：
```
class MyIndicator(bt.Indicator):

    ....
    plotinfo = dict(subplot=False)
    ....
```

之后可以按如下方式访问（和设置）该值（如果需要）
```
myind = MyIndicator(self.data, someparam=value)
myind.plotinfo.subplot = True
```

该值甚至可以在实例化的时候设置
```
myind = MyIndicator(self.data, someparams=value, subplot=True)
```
`subblot=True` 将被传递给指标的（幕后）指定成员变量`plotinfo`。

`plotinfo` 提供以下参数来控制打印行为：

* `plot` (default: `True`)  
    是否标绘指标

* `subplot` (default: `True`)   
    是否在其他窗口中绘制指示器。对于移动平均数这样的指标，默认值改为False

* `plotname` (default: '')  
    设置要在打印上显示的打印名称。空值表示将使用 indicator 的规范名称（class.__name__）。这有一些限制，因为Python标识符不能使用例如算术运算符之类。

    像DI+这样的指标将声明如下：
    ```
    class DIPlus(bt.Indicator):
    plotinfo=dict(plotname='DI+')
    ```

* `plotabove` (default: `False`)    
    指标（`subplot=True`的指标）通常标绘在它们所操作的数据下方。将此设置为 True 将使指示器绘制在数据上方。

* `plotlinelabels` (default: `False`)   
    指“指标”上的“指标”。如果计算 `RSI` 的 `SimpleMovingAverage`，则绘图通常会显示相应绘制线的名称`“SimpleMovingAverage”`。这是“指标”的名称，而不是实际绘制的line。

    这种默认行为是有意义的，因为用户通常希望看到使用RSI创建了一个SimpleMovingAverage。

    如果该值设置为`True`，则将使用 SimpleMovingAverage 中的 line 的实际名称(RSI???)。

* `plotymargin` (default: 0.0)  
    在指示器顶部和底部保留的余量（0.15->15%）。有时，matplotlib绘图到轴的顶部/底部太远，可能希望有一个边距

* `plotyticks` (default: [])    
    用于控制绘制的y比例刻度

    如果传递了一个空列表，“y tick”将自动计算。对于类似随机的情况，将其设置为众所周知的行业标准可能是有意义的，比如：[20.0，50.0，80.0]

    有些指示器提供了参数，如 `upperband` 和 `lowerband` ，这些参数实际上用于操纵 y ticks

* `plothlines` (default: [])    
    用于控制沿指示器轴的水平线的绘制。

    如果传递了一个空列表，则不会绘制水平线。

    对于诸如随机指标之类的东西，可能会为众所周知的工业标准画线，例如： [20.0, 80.0]

    一些指标提供了和等参数upperband，lowerband这些参数实际上用于操纵水平线

* `plotyhlines` (default: [])   
    使用单个参数用于同时控制 `plotyticks` 和 `plothlines`。

* `plotforce` (default: False)  
    如果出于某种原因，您认为某个指标应该有绘图，而它却没有绘图…请将此设置为True作为最后的手段


-----------------------------------------
# [Indicators - Development](./mkd02_Development.md)
# [Indicators - Timeframe Mixing](./mkd03_Timeframe_Mixing.md)
# [Indicators - Reference](./mkd04_Reference.md)
# [Indicators - ta-lib](./mkd05_talib.md)
# [Indicators - ta-lib - Reference](./mkd06_talib_Reference.md)