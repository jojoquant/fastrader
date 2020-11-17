# Trade
一个trade的定义:
* 当标的头寸从 0 到 X size 多头/空头头寸position, 可能为正/负）时，trade is open
* 当头寸从 X 变为 0 时, trade is closed

以下是两个动作：
* 正 到 负
* 负 到 正

实际上看到：
1. 一个 trade 已平仓（头寸从X转到0）
2. 一个新的交易已经 open（头寸从0到Y）

交易仅提供信息，没有用户可调用的方法。

# Reference: Trade
```
class backtrader.trade.Trade(data=None, tradeid=0, historyon=False, size=0, price=0.0, value=0.0, commission=0.0)
```
跟踪交易的生命周期：size, price, commission (and value?)

0 可以被看作交易的开始, 可以增加和减少，如果回到 0，则可以视为已平仓。

交易可以做多（正 size）或做空（负 size）

交易不应该是 reversed（逻辑上不支持）

成员属性：
* `ref`: 唯一的 trade identifier

* `status` (`int`): one of Created, Open, Closed

* `tradeid`: grouping tradeid passed to orders during creation The default in orders is 0

* `size` (`int`): current size of the trade

* `price` (`float`): current price of the trade

* `value` (`float`): current value of the trade

* `commission` (`float`): current accumulated commission

* `pnl` (`float`): current profit and loss of the trade (gross pnl)

* `pnlcomm` (`float`): current profit and loss of the trade minus commission (net pnl)

* `isclosed` (`bool`): records if the last update closed (set size to null the trade

* `isopen` (`bool`): records if any update has opened the trade

* `justopened` (`bool`): if the trade was just opened

* `baropen` (`int`): bar in which this trade was opened

* `dtopen` (`float`): float coded datetime in which the trade was opened

Use method open_datetime to get a Python datetime.datetime or use the platform provided num2date method

* `barclose` (`int`): bar in which this trade was closed

* `dtclose` (`float`): float coded datetime in which the trade was closed

Use method close_datetime to get a Python datetime.datetime or use the platform provided num2date method
barlen (int): number of bars this trade was open

* `historyon` (`bool`): whether history has to be recorded

* `history` (`list`): holds a list updated with each “update” event containing the resulting status and parameters used in the update

The first entry in the history is the Opening Event The last entry in the history is the Closing Event