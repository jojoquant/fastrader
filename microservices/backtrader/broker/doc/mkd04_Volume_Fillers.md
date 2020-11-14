- [Fillers](#fillers)
  - [The fillers signature](#the-fillers-signature)
  - [Adding a Filler to the broker](#adding-a-filler-to-the-broker)
  - [The sample](#the-sample)
  - [Reference](#reference)
    - [class backtrader.fillers.FixedSize()](#class-backtraderfillersfixedsize)
    - [class backtrader.fillers.FixedBarPerc()](#class-backtraderfillersfixedbarperc)
    - [class backtrader.fillers.BarPointPerc()](#class-backtraderfillersbarpointperc)

---------------------------------------------------------------------
# Fillers
在 order 执行时使用 volume, backtrader broker 模拟有一个默认策略:
* 忽略 volume

这是基于2个前提:

* 市场上的交易流动性足以一次性完全吸收买入/卖出指令

* 真实 volume 要求匹配现实世界  
    一个简单的例子是 `Fill or Kill` 订单。即使下降到 tick 分辨率, 也有足够填充 volume，在backtrader broker 不知道有多少额外的 actors 碰巧在市场中可以鉴别这样的 order, 能否匹配到 `Fill` 部分 或者 `order` 应该是 `Kill`

但是 broker 可以接受交易量填充器(`Volume Fillers`)，交易量填充器确定在给定的时间点用多少 volume 进行订单匹配。

## The fillers signature
```
callable(order, price, ago)
```
* `order` 将要被执行的订单
    
    该对象可访问 data 对象作为操作目标，创建 sizes/prices，执行prices/sizes/remaining sizes 以及其他详细信息

* `price` 订单执行的价格

* `ago` data在订单中寻找量价元素的索引 

    在几乎所有情况下，这都将是0（当前时间点），但是在涉及 Close 订单的特殊情况下，这可能是-1

    例如，要访问 bar volume，请执行以下操作：
    ```
    barvolume = order.data.volume[ago]
    ```

可调用对象可以是函数或例如支持该__call__方法的类的实例，例如：
```
class MyFiller(object):
    def __call__(self, order, price, ago):
        pass
```

## Adding a Filler to the broker
最直观的方法是使用 set_filler:
```
import backtrader as bt

cerebro = Cerebro()
cerebro.broker.set_filler(bt.broker.fillers.FixedSize())
```

另一个选择是完整替换 broker, 尽管这可能仅适用于BrokerBack已重写部分功能的子类：
```
import backtrader as bt

cerebro = Cerebro()
filler = bt.broker.fillers.FixedSize()
newbroker = bt.broker.BrokerBack(filler=filler)
cerebro.broker = newbroker
```

## The sample
backtrader 源码包含名为 `volumefilling` 的例子，其允许测试一些集成的 fillers（最初全部）

## Reference

### class backtrader.fillers.FixedSize()
```
class backtrader.fillers.FixedSize()
```
使用 bar 中 volume 的百分比返回给定订单的执行 size

百分比用参数 `perc` 设置

Params:
* `size` (default: `None`)      
    要执行的最大size 。如果执行时 bar 的实际 volume 小于该 size，则也是一个限制

    如果此参数的值评估为False，则将使用 bar 的全部 volume 来匹配订单

### class backtrader.fillers.FixedBarPerc()
```
class backtrader.fillers.FixedBarPerc()
```
使用 bar 的百分比返回给定订单的执行大小。

该百分比由参数设置 `perc`

Params:
* `perc` (default: 100.0) (valied values: 0.0 - 100.0)      
    用于执行订单的 volume bar 的百分比

### class backtrader.fillers.BarPointPerc()
```
class backtrader.fillers.BarPointPerc()
```
返回给定订单的执行size。volume 将在使用 `minmov` 分区 high-low 范围内均匀分布。

从给定价格的分配数量， 将使用百分比 `perc`

Params:

* `minmov` (default: 0.01)      
    最小价格变动。用于划分范围 high-low 按比例分配 volume 在可能的价格间

* `perc` (default: 100.0) (valied values: 0.0 - 100.0)      
    分配给订单执行价格以用于匹配的交易量的百分比
