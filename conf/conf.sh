#!/bin/sh

ACTION=$1
EVN=$2


start() {
    apt-get update
    apt-get -y install supervisor
    echo "\033[31m supervisor安装成功 \033[0m"
    apt-get -y install nginx
    echo "nginx安装成功"
    apt-get -y install python3-pip
    echo "python3-pip安装成功"
    pip3 install uwsgi
    echo "uwsgi安装成功"
    echo "开始配置"
    pip3 install -r /home/sfpt/conf/requirements.txt
    echo "python第三方插件安装完成"

    if [ "$EVN" = "debug" ]; then
        mv -f /home/sfpt/conf/nginx_debug.conf /etc/nginx/conf.d/sfpt.conf
        mv /home/sfpt/conf/supervisor_debug.conf /etc/supervisor/conf.d/sfpt.conf
    fi


    if [ "$EVN" = "debug" ]; then
        apt-get -y install redis-server
        echo "安装redis server"
    fi




    python3 /home/sfpt/manage.py migrate
    echo "初始化数据库"


    sudo killall -9 uwsgi
    echo "结束uwsgi进程"

    supervisorctl reread
    supervisorctl update


    supervisorctl restart sfpt


#    nohup uwsgi --ini /home/ksht/uwsgi.ini
#    echo "启动uwsgi进程"
    /etc/init.d/nginx reload
    echo "重启nginx"
    exit 0



}

stop(){
    exit 0
}

case "$ACTION" in
    start)
        start
    ;;
    stop)
        stop
    ;;
esac