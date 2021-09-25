[已解决]

dockerfile更新后, 重新build, 加 --build
> docker-compose up -d --build

[已解决]

ImportError: cannot import name 'warnings' from 'matplotlib.dates'

> pip uninstall matplotlib # or conda
> pip install matplotlib==3.2.2


[未解决]

> docker-compose up grafana

发现报错，对'/var/lib/grafana/plugins'没有权限创建目录，那么就赋予权限： chmod 777 /usr/local/grafana/