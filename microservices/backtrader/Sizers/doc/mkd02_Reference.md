- [Sizers Reference](#sizers-reference)
  - [Sizer](#sizer)
  - [FixedSize](#fixedsize)
  - [FixedReverser](#fixedreverser)
  - [PercentSizer](#percentsizer)
  - [AllInSizer](#allinsizer)
  - [PercentSizerInt](#percentsizerint)
  - [AllInSizerInt](#allinsizerint)

------------------------------------------------
# Sizers Reference
## Sizer
```
class backtrader.Sizer()
```
Sizers 的基类, 所有 sizer 都必须是该类的子类, 需要重构 `_getsizing` 方法

**成员属性**:
* `strategy`:     
    任意一个sizer工作的策略都可以设置
    
    提供对策略的整个api的访问权限，例如，如果需要实际的数据仓位就可以通过 `_getsizing` 方法
    ```
    position = self.strategy.getposition(data)
    ```
* `broker`      
    任意一个sizer工作的策略都可以设置

    提供对一些复杂 sizers 可能需要的信息的访问，如投资组合价值。

    Params:     
    * `comminfo`: `CommissionInfo`的实例, 包含data佣金信息, 可以进行 position value, operation cost, commission 的计算

    * `cash`: current available cash in the *broker*

    * `data`: target of the operation

    * `isbuy`: will be `True` for *buy* operations and `False` for *sell* operations

**成员方法**:
* `_getsizing(comminfo, cash, data, isbuy)`     
    该方法必须返回要执行的实际 size（int）。如果返回的是0，则不执行任何操作。

    将使用返回值的绝对值

## FixedSize
```
class backtrader.sizers.FixedSize()
```
此 `sizer` 只返回任何操作的固定 size。size 可以通过 `tranches` 参数指定，由系统希望用来扩展到交易中的份额数量来控制。

Params:
* `stake` (default: `1`)
* `tranches` (default: `1`)

## FixedReverser
```
class backtrader.sizers.FixedReverser()
```
这个 `sizer` 返回需要的固定 size 来反转 open position，或者固定的 size 来开仓

* To open a position: return the param stake
* To reverse a position: return 2 * stake

Params:
* `stake` (default: `1`)
```
params = (('stake', 1),)
 
    def _getsizing(self, comminfo, cash, data, isbuy):
        position = self.strategy.getposition(data)
        size = self.p.stake * (1 + (position.size != 0))
        return size
```

## PercentSizer
```
class backtrader.sizers.PercentSizer()
```
这个sizer将返回现金可用百分比

Params:
* `percents` (default: `20`)
```
    params = (
        ('percents', 20),
        ('retint', False),  # return an int size or rather the float value
    )
    
    def __init__(self):
        pass
    
    def _getsizing(self, comminfo, cash, data, isbuy):
        position = self.broker.getposition(data)
        if not position:
            size = cash / data.close[0] * (self.params.percents / 100)
        else:
            size = position.size
    
        if self.p.retint:
            size = int(size)
    
        return size
```

## AllInSizer
```
class backtrader.sizers.AllInSizer()
```
这个sizer返回 broker 全部的可用cash

Params:
* `percents` (default: `100`)
```
class AllInSizer(PercentSizer):
    '''This sizer return all available cash of broker
 
     Params:
       - ``percents`` (default: ``100``)
     '''
    params = (
        ('percents', 100),
    )
```

## PercentSizerInt
```
class backtrader.sizers.PercentSizerInt()
```
这个sizer返回可用现金的取整百分比

Params:
* `percents` (default: `20`)
```
class PercentSizerInt(PercentSizer):
    '''This sizer return percents of available cash in form of size truncated
    to an int
 
    Params:
      - ``percents`` (default: ``20``)
    '''
 
    params = (
        ('retint', True),  # return an int size or rather the float value
    )
```

## AllInSizerInt
```
class backtrader.sizers.AllInSizerInt()
```
这个sizer返回 broker 可用现金的 size 取整

Params:

* `percents` (default: `100`)
```
class AllInSizerInt(PercentSizerInt):
    '''This sizer return all available cash of broker with the
    size truncated to an int
 
     Params:
       - ``percents`` (default: ``100``)
     '''
    params = (
        ('percents', 100),
    )
```