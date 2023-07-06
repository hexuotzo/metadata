# 基于的基础镜像

FROM centos:centos7.8.2003

# 维护者信息

MAINTAINER hesaiyue  hesaiyue@aerozhonghuan.com

# 代码添加到code文件夹

COPY ./install_package/Python-3.6.6.tgz /code/
COPY ./install_package/libressl-2.9.0.tar.gz /code/
COPY ./install_package/openssl-1.0.2a.tar.gz /code/

# 设置code文件夹是工作目录

WORKDIR /code

# 安装支持
#  配置yum源(由于本身CentOs安装上之后 yum源默认为清华  所以跳过这步)
#RUN yum install wget -y &&  cp /etc/yum.repos.d/CentOS-Base.repo  /etc/yum.repos.d/CentOS-Base.repo.bak && wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo && yum clean all && yum makecache


# 设置命令行无交互
ARG DEBIAN_FRONTEND=noninteractive

# 安装gcc等基础组件
RUN yum install gcc gcc-c++ make ssh vim wget cmake unzip build-essential zlib-devel  bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel  git libgl1-mesa-glx mesa-libGL.x86_64 -y && yum makecache

# 安装openssl组件
RUN  tar -xzf openssl-1.0.2a.tar.gz && cd /code/openssl-1.0.2a && ./config --prefix=/usr/local/openssl-1.0.2a  && make && make install && echo "/usr/local/openssl-1.0.2a/lib/" >/etc/ld.so.conf.d/openssl.conf && ldconfig


# 安装编译python需要的组件
RUN  tar -xzf libressl-2.9.0.tar.gz && cd /code/libressl-2.9.0 && ./configure && make && make install

# 安装python3.6
RUN tar -zxvf  /code/Python-3.6.6.tgz
RUN  cd /code/Python-3.6.6  && ./configure --prefix=/usr/local/python3.6 --with-openssl=/usr/local/openssl-1.0.2a --enable-optimizations && make -j8 build_all && make -j8 install
RUN ln -sf /usr/local/python3.6/bin/python3.6 /usr/bin/python && ln -sf /usr/local/python3.6/bin/python3.6 /usr/bin/python3 && ln -sf /usr/local/python3.6/bin/pip3 /usr/bin/pip  && ln -sf /usr/local/python3.6/bin/pip3 /usr/bin/pip3

## 开启ssh -i "10s/https:\/\/www.baidu.com/https:\/\/www.google.cn/"
##RUN sed -i "34s/\#PermitRootLogin prohibit-password/PermitRootLogin yes" && service ssh start


# 修改pip源
RUN mkdir ~/.pip/

RUN  echo -e '[global]\nindex-url=http://mirrors.aliyun.com/pypi/simple/\n[install]\ntrusted-host=mirrors.aliyun.com' > ~/.pip/pip.conf
# 更新pip
RUN rm -rf /usr/bin/lsb_release

RUN python -m pip install --user --upgrade pip

# 在编译dlib之前安装cmake
RUN pip install cmake -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

# 安装pymysql
COPY ./pip_package/PyMySQL-0.9.2-py2.py3-none-any.whl /code/
RUN pip install /code/PyMySQL-0.9.2-py2.py3-none-any.whl

# 安装扩展库
COPY ./pip_package/requirements.txt /code/
RUN pip install -r /code/requirements.txt


# 切换工作路径
WORKDIR /code/alakir/

# 启动后执行的命令
#EXPOSE 8888 9999
#CMD ["python", "./manage.py", "runserver","0.0.0.0:8888"]
#CMD ["/usr/local/python3.6/bin/gunicorn","--worker-class=gevent","-w","2","hippo.wsgi:application","-b","0.0.0.0:8888"]


CMD top