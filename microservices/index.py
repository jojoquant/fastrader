#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# http://www.mingjiao.org:8088/

import random
from nameko.rpc import rpc, RpcProxy


class Index(object):
    name = "index"
    register_rpc = RpcProxy("index")

    @rpc
    def index(self):
        return {'welcome_info': "欢迎使用Python微服务"}
