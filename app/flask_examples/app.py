#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# http://www.mingjiao.org:8088/

import os
from flask import Flask, render_template
from nameko.standalone.rpc import ClusterRpcProxy

nameko_username = os.environ.get('nameko_username')
nameko_password = os.environ.get('nameko_password')
nameko_host = os.environ.get('nameko_host', "rabbitmq")

template_dir = os.path.abspath('./templates')

app = Flask(__name__, template_folder=template_dir)

CONFIG = {'AMQP_URI': f"amqp://{nameko_username}:{nameko_password}@{nameko_host}"}


@app.route('/', methods=['GET'])
def index():
    with ClusterRpcProxy(CONFIG) as rpc:
        user_data = rpc.index.index()
    return render_template('index.html', template=user_data.get('welcome_info'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
