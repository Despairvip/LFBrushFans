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
    pip3 install -r /home/sfpt-server/conf/requirements.txt
    echo "python第三方插件安装完成"

    if [ "$EVN" = "debug" ]; then
        mv -f /home/sfpt-server/conf/nginx_debug.conf /etc/nginx/conf.d/sfpt.conf
        mv /home/sfpt-server/conf/supervisor_debug.conf /etc/supervisor/conf.d/sfpt.conf
    elif [ "$EVN" = "prerelease" ]; then
        mv -f /home/sfpt-server/conf/nginx_prerelease.conf /etc/nginx/conf.d/sfpt.conf
        mv /home/sfpt-server/conf/supervisor_prerelease.conf /etc/supervisor/conf.d/sfpt.conf
    else
        mv -f /home/sfpt-server/conf/nginx_release.conf /etc/nginx/conf.d/sfpt.conf
        mv /home/sfpt-server/conf/supervisor_release.conf /etc/supervisor/conf.d/sfpt.conf
    fi



    mv -f /home/sfpt-server/sfpt/settings_"$EVN".py /home/sfpt-server/sfpt/settings.py
    apt-get -y install redis-server
    echo "安装redis server"




    python3 /home/sfpt-server/manage.py migrate
    echo "初始化数据库"


    sudo killall -9 uwsgi

    echo "结束uwsgi进程"

    supervisorctl reread
    supervisorctl update


    supervisorctl restart sfpt


#    nohup uwsgi --ini /home/ksht/uwsgi.ini
#    echo "启动uwsgi进程"
    killall -9 nginx
    /etc/init.d/nginx start
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