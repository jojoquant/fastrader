# Data Feeds - Yahoo
2017年5月，Yahoo停止了以csv格式下载历史数据的现有API 。

新的API（此处称为v7）已迅速标准化并已实现。

这也改变了实际的CSV下载格式。

## Using the v7 API/format
从版本开始，`1.9.49.116`这是默认行为。简单选择

* `YahooFinanceData` 用于在线下载

* `YahooFinanceCSVData` 用于离线下载的文件

## Using the legacy API/format
使用旧的 API/format

* 实例化在线Yahoo数据供稿为：
```
data = bt.feeds.YahooFinanceData(
    ...
    version='',
    ...
)
```
* 离线Yahoo data Feed的形式为：
```
data = bt.feeds.YahooFinanceCSVData(
    ...
    version='',
    ...
)
```
可能是在线服务又回来了（该服务在没有任何通知的情况下终止了……它很可能又回来了）

要么

* 仅对于更改发生之前下载的脱机文件，还可以执行以下操作：
```
 data = bt.feeds.YahooLegacyCSV(
    ...
    ...
)
```
新的 `YahooLegacyCSV` 只是使用 version=''