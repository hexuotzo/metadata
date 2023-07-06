## Hippo项目搭建Docker环境
### 安装命令
```commandline
    bash init.sh init
```
### 目录详解
```
    docker目录:hippo/docker
        |---install_package->存放linux环境的安装包
        |---pip_package->存放python第三方扩展包
        |---config->init.sh配置文件
        |---Dockerfile->Docker打包文件
        |---init.sh->环境搭建的shell脚本名
        |---ReadMe.md->文档
```

### 文件详解
#### config文件配置规范
 ```
    # local  物理机配置
    local_port_one=8888   物理机端口1
    local_port_two=9999   物理机端口2
    local_code_dir=/mnt/d/Pycode/hippo/  物理机存放代码目录
    local_log_dir=/data/hippo/   物理机存放log的目录
    # container  虚拟机配置
    container_port_one=8888   虚拟机端口1
    container_port_two=9999   虚拟机端口2
    container_code_dir=/code/hippo/   虚拟机存放代码目录
    container_log_dir=/data/hippo/    虚拟机存放log的目录
    # name  镜像和容器名称配置
    images_repository=ubuntu  镜像名称
    images_tag=hippo   镜像tag
    container_name=hippo   容器名称
    # kafka host配置
    kafka1~kafka6  配置ip
    # threads_num  
    threads_number=2 启动服务的线程数
 ```

#### init.sh使用方法

```
    bash init.sh <option> <param>
    option:
        start_container  启动容器
        restart_container 重启容器
        stop_container 停止容器
        init 初始化安装(完全删除重装)
        build_images 创建镜像
        delete_images 删除镜像
        create_container 创建容器
        delete_container 删除容器
    option param:
        load ./hippo_docker.tar  导入镜像
        export ./hippo_docker.tar 导出镜像
```

### Docker的命令操作
```
    打包:docker build ./h_docker/ -t ubuntu:hippo
        命令解释:./h_docker/  DockerFile文件存放的文件夹
                -t  生成镜像的名称:tag
    启动:
        生成容器命令: docker run -p 8888:8888 --name hippo --privileged=true  -v /data/hippo/:/data/hippo/ -v /mnt/d/PyCode/hippo/:/code/hippo/ -d ubuntu:hippo
        命令解释: -p 本地端口号:容器端口号
              -name 生成的容器名称
              --privileged=true  关闭安全模式映射文件夹
              -v 本地目录或文件:容器目录或文件
              -d 后台执行
              ubuntu:hippo 镜像名称:tag
    
        容器启动命令: docker start hippo
        容器重启命令: docker restart hippo
    
    导出和导入:
        导出命令:docker save -o ./hippo_docker.tar ubuntu:hippo
        命令解释:-o ./hippo_docker.tar 导出的文件路径
                ubuntu:hippo  镜像名称:tag
        导入命令:docker load < ./hippo_docker.tar
        命令解释:./hippo_docker.tar  镜像压缩包存放路径
    
    常用:
        docker ps -a  查看当前容器列表
        docker rm 容器id或容器名称     删除容器
        docker images 查看当前镜像列表
        docker rmi 镜像id    删除镜像(删除镜像之前必须删除当前镜像所启动的容器)
```