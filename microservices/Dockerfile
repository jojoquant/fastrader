FROM ubuntu
WORKDIR /code
RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN apt clean
RUN apt update -y
RUN apt upgrade -y
RUN apt install -y python3 python3-pip
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple nameko
ENV RABBITMQ_HOST=rabbitmq
COPY ./index.py ./index.py
CMD sh -c "nameko run index --broker amqp://$NAMEKO_USER:$NAMEKO_PASS@$RABBITMQ_HOST"