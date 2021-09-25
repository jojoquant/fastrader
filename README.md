# 项目企划
micro-fastrader = nameko + fastapi + backtrader

```
正在施工中...
```

**施工进度**
- nameko
  - [x] docker及docker-compose使用
  - [x] nameko基本使用
  - [ ] 微服务 Websocket 通信
- fastapi
  - [x] User Guide
  - [ ] Advanced Using
- backtrader
  - [x] Quick Guide
  - [ ] Advanced Using

# 架构说明

## docker-compose
.env 文件存放容器外port

***.env 文件存放相应容器的环境变量

### image 更新
单独docker镜像
```
docker images   // 查看本地镜像
docker pull  镜像名字  // 更新镜像到最新, 残留的旧镜像可以删除
```
docker-compose镜像
```
docker-compose stop
docker-compose pull
docker-compose up -d --build
```
