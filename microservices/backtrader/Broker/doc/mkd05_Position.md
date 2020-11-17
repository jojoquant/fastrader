# Position
通常通过以下方法从策略中检查资产头寸：

* `position` （财产）或 `getposition(data=None, broker=None)`   
    它将返回 cerebro 提供的默认 broker 中策略的 datas[0] 的位置

`position` 只是表明：

* 持有资产的 `size`
* 平均价格是 `price`

它表示一种状态，例如可用于确定是否必须发出订单（例如：仅在未开仓的情况下才开仓多头头寸）

# Reference: Position
```
class backtrader.position.Position(size=0, price=0.0)
```
保存和更新仓位的 size 和 price. 该对象和asset没有关系, 值保留 size 和 price

成员属性:

* size (int): current size of the position

* price (float): current price of the position

可以使用 `len(Position)` 测试 `Position` 实例，看看大小是否为 null