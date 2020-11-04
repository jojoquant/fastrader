- [Analyzers - PyFolio](#analyzers---pyfolio)
  - [Usage](#usage)
  - [Sample Code](#sample-code)
  - [Reference](#reference)

-------------------------------------------------------------------
# Analyzers - PyFolio
>截至（至少）2017-07-25，`pyfolio` API已经发生了变化， `create_full_tear_sheet` 不再以 `gross_lev` 作为命名参数。因此，用于集成的示例不起作用

引用 `pyfolio` 主页面 http://quantopian.github.io/pyfolio/:
```
pyfolio is a Python library for performance and risk analysis of financial
portfolios developed by Quantopian Inc. It works well with the Zipline open
source backtesting library
```
pyfolio是一个Python库，用于财务性能和风险分析，由Quantopian公司开发的投资组合。它与Zipline open配合良好源代码回溯测试库

现在它也很好地与backtrader合作。需要什么：
* 很明显是pyfolio
* 以及它的依附关系(things like pandas, seaborn …)

>在与版本0.5.1的集成过程中，需要对依赖项的最新包进行更新，比如seaborn从以前安装的0.7.0-dev升级到0.7.1，这显然是因为缺少swarmplot方法

## Usage
1. 将PyFolio分析仪添加到 cerebro 中：
    ```
    cerebro.addanalyzer(bt.analyzers.PyFolio)
    ```
2. 运行并检索第一个策略:
    ```
    strats = cerebro.run()
    strat0 = strats[0]
    ```
3. 检索分析器, 使用您为其指定的名称 或 其默认名称：pyfolio。例如：
    ```
    pyfolio = strats.analyzers.getbyname('pyfolio')
    ```
4. 使用 analyzer 的方法 `get_pf_items` 去获取 pyfolio 稍后需要的4个组件 
    ```
    returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()
    ```
    > 注意!!    
    > 通过对“pyfolio”可用的测试样本进行集成，复制了相同的头文件(或者没有)
5. 与pyfolio合作（这已经超出了backtrader生态系统）  
    
    一些与backtrader没有直接关系的使用说明:
    
    * `pyfolio` 自动绘图功能可以在Jupyter Notebook外部工作，但在内部效果最好
    * `pyfolio` 数据表的输出在Jupyter Notebook之外似乎几乎不起作用。它在Notebook内工作
    
    如果希望使用pyfolio，那么结论很简单：在Jupyter Notebook中工作

## Sample Code
```
...
cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')
...
results = cerebro.run()
strat = results[0]
pyfoliozer = strat.analyzers.getbyname('pyfolio')
returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()
...
...
# pyfolio showtime
import pyfolio as pf
pf.create_full_tear_sheet(
    returns,
    positions=positions,
    transactions=transactions,
    gross_lev=gross_lev,
    live_start_date='2005-05-01',  # This date is sample specific
    round_trips=True)

# At this point tables and chart will show up
```

## Reference
查看 PyFolio 分析器的 Analyzers 参考，以及它在内部使用哪些分析器