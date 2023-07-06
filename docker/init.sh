#!/bin/bash
source ./config
docker --version &>/dev/null
if [ $? -ne 0 ]; then
  echo -e "未安装 Docker！"
  exit 1
fi
images_name=${images_repository}":"${images_tag}
# echo $docker_name
now_dir=$(pwd)

# 删除镜像
delete_images() {
  local docker_img_id=$(docker images --filter=reference=${images_repository}:${images_tag} | grep $images_tag | awk '{print $3}')

  if [ "$docker_img_id" ]; then
    # 删除镜像前删除容器
    delete_container "当前存在使用该镜像的容器${container_name},是否删除?(y or n):"
    read -p "是否删除镜像:${images_name}?(y or n):" arg
    if [[ "$arg" == "y" ]]; then
      # 删除镜像
      docker rmi "$docker_img_id"
      currency_message "删除镜像"
    elif [[ "$arg" == "n" ]]; then
      exit 1
    else
      delete_images
    fi
  fi
}

# 删除容器
delete_container() {
  # 判断容器是否存在
  local docker_con_id=$(docker ps -a --filter "name=$container_name" | grep $container_name | awk '{print $1}')

  if [ "$docker_con_id" ]; then
    if [ $# -gt 0 ]; then
      read -p "$1" arg
    else
      read -p "是否删除容器:${container_name}?(y or n):" arg
    fi

    if [[ "$arg" == "y" ]]; then
      # 当前存在使用该镜像的容器 选择删除该容器  删除前必须停止容器
      stop_container
      docker rm "${docker_con_id}"
      currency_message "删除容器"

    elif [[ "$arg" == "n" ]]; then
      exit 1
    else
      delete_container "$1" if [ $# -gt 0 ] then delete_container

    fi
  fi
}

# 通用提示语
currency_message(){
  if [ $# -gt 0 ];then
    if [ $? -eq 0 ];then
      echo "$1成功"
    else
      echo "$1失败"
      exit 1
    fi
  fi
}

# 打包
build_images() {
  # 判断镜像以及容器是否存在
  delete_images
  # 不存在  打包
  docker build $now_dir/../docker -t $images_name
  if [ $? -ne 0 ];then
      exit 1
  fi
  currency_message "打包镜像"
}

# 创建容器
create_container() {
  # 判断是否存在镜像
  docker_img=$(docker images --filter=reference=${images_repository}:${images_tag} | grep $images_tag)
  if [ $? -eq 0 ]; then
    # 存在镜像
    if [[ ${port_number} == 1 ]];then
      # 启动端口的数量
      docker run -it -p ${local_port_one}:${container_port_one} --name ${container_name} --privileged=true  -v ${local_code_dir}:${container_code_dir}  -d ${images_repository}:${images_tag}
    else
         docker run -it -p ${local_port_one}:${container_port_one} -p ${local_port_two}:${container_port_two} --name ${container_name} --privileged=true  -v ${local_code_dir}:${container_code_dir}  -d ${images_repository}:${images_tag}
    fi
  else
    build_images
    create_container
    currency_message "创建容器"

  fi
}

# 启动服务
start_service(){

  if [[ ${port_number} == 1 ]];then
    docker exec -d ${container_name} /usr/local/python3.6/bin/gunicorn --worker-class=gevent -w ${threads_number} ${container_name}.wsgi:application -b 0.0.0.0:${container_port_one} ; docker exec -d ${container_name} /usr/local/python3.6/bin/gunicorn --worker-class=gevent -w ${threads_number} ${container_name}.wsgi:application -b 0.0.0.0:${container_port_two}
  else
    docker exec -d ${container_name} /usr/local/python3.6/bin/gunicorn --worker-class=gevent -w ${threads_number} ${container_name}.wsgi:application -b 0.0.0.0:${container_port_one}
  fi

  currency_message "启动服务"
}


# 启动容器
start_container(){
  docker start ${container_name}
  currency_message "启动容器"
  start_service

}

# 停止容器
stop_container(){
    docker stop ${container_name}
    currency_message "停止容器"

}

# 重启容器
restart_container(){
  docker restart ${container_name}
  currency_message "重启容器"
  start_service

}

# 完整安装
init() {
  build_images
  create_container
  start_container
}

# 加载压缩文件镜像
load_tar() {
  if [ $# -gt 0 ]; then
    if [ ! -e $1 ]; then
      echo "文件不存在"
      exit 1
    elif [ ! -r $1 ]; then
      echo "文件不可读"
      exit 1
    fi
    echo "正在导入......"
    delete_images
    docker load <$1
  else
    echo "命令必须包含docker压缩包"
    exit 1
  fi
}

# 导出压缩文件镜像
export_tar() {
  if [ $# -gt 0 ]; then
    local docker_img_id=$(docker images --filter=reference=${images_repository}:${images_tag} | grep $images_tag | awk '{print $3}')
    if [ $? -eq 0 ]; then
      echo "正在导出......"
      docker save -o $1 "$images_name"
      if [ $? -ne 0 ]; then
        echo "导出失败"
        exit 1
      fi
      echo "导出成功:$1"
    else
      echo "镜像${images_name}不存在"
    fi
  else
    echo "缺少文件路径"
    exit 1
  fi
}
####################################
if [ $# -gt 0 ]; then
  if [[ "$1" == "start_container" ]]; then
    start_container
  elif [[ "$1" == "restart_container" ]]; then
    restart_container
  elif [[ "$1" == "stop_container" ]]; then
    stop_container
  elif [[ "$1" == "init" ]]; then
    init
  elif [[ "$1" == "build_images" ]]; then
    build_images
  elif [[ "$1" == "delete_images" ]]; then
    delete_images
  elif [[ "$1" == "delete_container" ]]; then
    delete_container
  elif [[ "$1" == "create_container" ]]; then
    create_container
  elif [[ "$1" == "load" ]] && [ $# -gt 1 ]; then
    load_tar $2
  elif [[ "$1" == "export" ]] && [ $# -gt 1 ]; then
    export_tar $2
  fi
fi
