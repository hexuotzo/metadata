# 基于的基础镜像
FROM python:3.7

# 维护者信息
MAINTAINER hesaiyue  hesaiyue10508@navinfo.com

# 代码添加到code文件夹
COPY ./ /data/www/alakir/

# 设置命令行无交互
ARG DEBIAN_FRONTEND=noninteractive


# 修改pip源
RUN mkdir ~/.pip/

RUN  echo '[global]\nindex-url=https://pypi.tuna.tsinghua.edu.cn/simple/\n[install]\ntrusted-host=pypi.tuna.tsinghua.edu.cn' > ~/.pip/pip.conf

# 更新pip
RUN python -m pip install --user --upgrade pip

# 安装扩展库
RUN pip install -r /data/www/alakir/requirements.txt

EXPOSE 8088

WORKDIR /data/www/alakir/
# 启动后执行的命令
CMD ["gunicorn","--worker-class=gevent","-w","2","alakir.wsgi:application","-b","0.0.0.0:8088"]
