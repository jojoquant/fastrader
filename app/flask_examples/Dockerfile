FROM centos:8
WORKDIR /code
RUN yum install -y python3
RUN pip3 install -i https://pypi.douban.com/simple/ flask
RUN pip3 install -i https://pypi.douban.com/simple/ nameko
ENV nameko_username=rabbitmq_admin nameko_password=Cisc0123 rabbitmq_host=rabbitmq
EXPOSE 5000
COPY . .
CMD ["python3", "app.py"]