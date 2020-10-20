
[已解决]

dockerfile更新后, 重新build, 加 --build
> docker-compose up -d --build


[未解决]

> docker-compose up grafana

发现报错，对'/var/lib/grafana/plugins'没有权限创建目录，那么就赋予权限：
chmod 777 /usr/local/grafana/