[更多docker说明](https://hub.docker.com/_/mongo)
#环境变量   

启动mongo映像时，可以通过在docker run命令行上传递一个或多个环境变量来调整MongoDB实例的初始化。请注意，如果使用已包含数据库的数据目录启动容器，则以下任何变量都将无效：容器启动时，任何现有数据库都将保持不变。

**MONGO_INITDB_ROOT_USERNAME, MONGO_INITDB_ROOT_PASSWORD**  
这些变量一起使用，可以创建一个新用户并设置该用户的密码。该用户在admin 身份验证数据库中创建，并具有的角色root，这是“超级用户”角色。

以下是使用这两个变量创建MongoDB实例，然后使用mongocli连接到admin身份验证数据库的示例。

```
$ docker run -d --network some-network --name some-mongo \
    -e MONGO_INITDB_ROOT_USERNAME=mongoadmin \
    -e MONGO_INITDB_ROOT_PASSWORD=secret \
    mongo

$ docker run -it --rm --network some-network mongo \
    mongo --host some-mongo \
        -u mongoadmin \
        -p secret \
        --authenticationDatabase admin \
        some-db
> db.getName();
some-db
```

这两个变量都是创建用户所必需的。如果两者都存在，则MongoDB将以启用身份验证（mongod --auth）开始。

MongoDB中的身份验证相当复杂，因此，更复杂的用户设置将通过以下方式明确地留给用户/docker-entrypoint-initdb.d/（有关更多详细信息，请参见下面的初始化新实例和身份验证部分）。

**MONGO_INITDB_DATABASE**
此变量允许您指定用于创建脚本的数据库的名称/docker-entrypoint-initdb.d/*.js（请参阅下面的初始化新实例）。MongoDB从根本上设计为“首次使用时创建”，因此，如果您不随JavaScript文件一起插入数据，则不会创建数据库。