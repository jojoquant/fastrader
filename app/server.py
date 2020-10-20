# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Datetime : 2020/10/3 2:26
# @Author   : Fangyang
# @Software : PyCharm

import json
import asyncio
import os

import uvicorn
from fastapi import FastAPI, Depends, Cookie, Header
from fastapi import Request
from fastapi import WebSocket
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse, Response
from starlette.status import WS_1008_POLICY_VIOLATION

from nameko.standalone.rpc import ClusterRpcProxy

nameko_username = os.environ.get('NAMEKO_USER')
nameko_password = os.environ.get('NAMEKO_PASS')
nameko_host = os.environ.get('NAMEKO_HOST', "rabbitmq")

CONFIG = {
    'AMQP_URI': f"amqp://{nameko_username}:{nameko_password}@{nameko_host}"
}

app = FastAPI()
# templates = Jinja2Templates(directory="templates")

with open('./templates/measurements.json', 'r') as file:
    measurements = iter(json.loads(file.read()))


@app.get("/")
async def index(request: Request):
    with ClusterRpcProxy(CONFIG) as rpc:
        user_data = rpc.index.index()
    return {'msg': user_data}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        await asyncio.sleep(1)
        payload = next(measurements)
        await websocket.send_json(payload)


if __name__ == '__main__':
    uvicorn.run("server:app", host='0.0.0.0', port=8089, debug=True)
