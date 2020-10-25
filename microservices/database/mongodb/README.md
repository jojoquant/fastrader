
进入容器的 bash
> docker exec -it fastrader_mongo_1 bash

进入容器的 mongo shell
> docker exec -it fastrader_mongo_1 mongo

退出
> \>exit


由于MongoDB内datetime采用UTC, 所以pandas在IO过程中需要对datetime进行时区转换
```
df['report_date'] = pd.to_datetime(df['report_date'], format='%Y%m%d', utc=False)
df['report_date'] = df['report_date'].dt.tz_localize('Asia/Shanghai')  # 设置当前时间为东八区
df['report_date'] = df['report_date'].dt.tz_convert('UTC')   # 转成utc时间
```