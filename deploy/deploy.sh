#!/bin/bash

usage(){
    echo $"Usage: $0 [-s|--start] {db|ui|api|pusher|crawler|browser} [-e|--env] {test/prod} [-t|--target_dir] {deploy_dir} [-n|--num] {brwoser_num} [-c|--clean]" 1>&2
    echo $"example:" 1>&2
    echo $"deploy.sh -s db -e prod -t /data/" 1>&2
    echo $"deploy.sh -s brwoser -e prod -t /data/ -n 5" 1>&2
    echo $"" 1>&2
    echo $"-s|--start  require, deploy app" 1>&2
    echo $"-e|--env  start require, environment, pro or test" 1>&2
    echo $"-t|--target_dir  require, deploy target directory" 1>&2
    echo $"-n|--brwoser_num  require when app is brwoser, start brwoser num, max 20" 1>&2
    echo $"-c|--clean  option, files in the target directory will forcibly deleted" 1>&2
    exit 1
}

ARGS=`getopt -o s:e:t:d:n:c -l start:,env:,target_dir:,dbs:,brwoser_num:,clean -- "$@"`
eval set -- "$ARGS"


while true ; do
    case "$1" in
        -s|--start)
            case "$2" in
                "db"|"ui"|"api"|"pusher"|"crawler"|"browser") START=$2 ; shift 2 ;;
                                                            *) echo '1';usage ; exit 1 ;;
            esac ;;
        -e|--env)
            case "$2" in
                "test"|"prod") ENV=$2 ; shift 2 ;;
                            *) usage ; exit 1 ;;
            esac ;;
        -t|--target_dir)
            TARGET_DIR=$2 ; shift 2;;
        -n|--brwoser_num)
            BROWSER_NUM=$2 ;shift 2 ;;
        -c|--clean)
            CLEAN=1 ;shift ;;
        --) shift ; break ;;
        *) usage ; exit 1 ;;
    esac
done


if [[ '$TARGET_DIR' == *'/' ]] ; then
    TARGET_DIR=${TARGET_DIR:0:0-1}
fi

if [ "$ENV" == "prod" ] ; then
    if [ "$START" = "pusher" ] || [ "$START" = "crawler" ]; then
        ENV_FILE='prod.crawler.env'
    elif [ "$START" = "db" ]; then
        ENV_FILE='prod.db.env'
    else
        ENV_FILE='prod.env prod.db.env'
    fi
else
    ENV_FILE='test.env'
fi


crawler_deploy(){
    build
    init "docker-compose.crawler.yml"
    cp docker-compose.crawler.yml $TARGET_DIR/docker-compose.crawler.yml
    cp ../backend/.envs/$ENV_FILE $TARGET_DIR/.env
    cp -r ../backend/* $TARGET_DIR/
    cd $TARGET_DIR
    docker-compose -f docker-compose.crawler.yml up -d crawler-scheduler crawler-worker
    
}

pusher_deploy(){
    build
    init "docker-compose.pusher.yml"
    cp docker-compose.pusher.yml $TARGET_DIR/docker-compose.pusher.yml
    cp ../backend/.envs/$ENV_FILE $TARGET_DIR/.env
    cp -r ../backend/* $TARGET_DIR/
    cd $TARGET_DIR
    docker-compose -f docker-compose.pusher.yml up -d pusher-scheduler pusher-worker
    
}

browser_deploy(){
    init "docker-compose.browser.yml"
    cp ../backend/.envs/$ENV_FILE $TARGET_DIR/.env
    if [ ! "$BROWSER_NUM" == "" ];then
        cp docker-compose.browser.yml $TARGET_DIR/docker-compose.browser.yml
        cd $TARGET_DIR
        docker-compose -f docker-compose.browser.yml up -d --scale chrome=$BROWSER_NUM
    else
        usage
    fi

}


db_deploy(){
    init "docker-compose.db.yml"
    cp ../backend/.envs/$ENV_FILE $TARGET_DIR/.env
    cp -r pgsql.conf $TARGET_DIR/
    cp -r docker-compose.db.yml $TARGET_DIR/
    cd $TARGET_DIR
    echo "Deploy db..."
    docker-compose -f docker-compose.db.yml up -d

}

ui_deploy(){
    build
    init "docker-compose.ui.yml"
    cp -r docker-compose.ui.yml $TARGET_DIR/docker-compose.ui.yml
    if [ ! -d $TARGET_DIR/html ]; then
        mkdir $TARGET_DIR/html
    fi
    if [ ! -d $TARGET_DIR/nginx ]; then
        mkdir -p $TARGET_DIR/nginx
    fi
    
    if [ ! -d $TARGET_DIR/backend ]; then
        mkdir $TARGET_DIR/backend
        mkdir $TARGET_DIR/backend/.envs
    fi
    cp -r ../backend/src $TARGET_DIR/backend/
    cp -r ../backend/main.py $TARGET_DIR/backend/

    for item in $ENV_FILE; do
        cp -r ../backend/.envs/$item $TARGET_DIR/backend/.envs/
    done

    cp -r ../dist/* $TARGET_DIR/html/
    cp -r nginx/ui_nginx.conf $TARGET_DIR/nginx/nginx.conf

    if [ "$ENV" == "prod" ] ; then
        echo 'APP_ENV=prod' > $TARGET_DIR/backend/.envs/.env
    else
        echo 'APP_ENV=test' > $TARGET_DIR/backend/.envs/.env
    fi

    cd $TARGET_DIR
    docker-compose -f docker-compose.ui.yml up -d
    cd /data/nginx/conf.d
    rm -rf sec.cafe.conf
    ln /data/www/sec.cafe/nginx/nginx.conf sec.cafe.conf
    docker exec -it nginx nginx -s reload
}

api_deploy(){
    build
    init "docker-compose.api.yml"
    cp -r docker-compose.api.yml $TARGET_DIR/docker-compose.api.yml

    if [ ! -d $TARGET_DIR/nginx ]; then
        mkdir -p $TARGET_DIR/nginx/log
    fi
    
    if [ ! -d $TARGET_DIR/src ]; then
        mkdir $TARGET_DIR/src
        mkdir $TARGET_DIR/src/.envs
    fi
    cp -r ../backend/src $TARGET_DIR/src/
    cp -r ../backend/run_api.py $TARGET_DIR/src/
    for item in $ENV_FILE; do
        cp -r ../backend/.envs/$item $TARGET_DIR/backend/.envs/
    done
    cp -r nginx/api_nginx.conf $TARGET_DIR/nginx/nginx.conf
    if [ "$ENV" == "prod" ] ; then
        echo 'APP_ENV=prod' > $TARGET_DIR/src/.envs/.env
    else
        echo 'APP_ENV=test' > $TARGET_DIR/src/.envs/.env
    fi

    cd $TARGET_DIR
    docker-compose -f docker-compose.api.yml up -d
    docker exec -it nginx nginx -s reload
}

build(){
    cd ../backend
    export VERSION=1.0
    docker build . -t sec_cafe_backend:${VERSION}
    cd ../deploy
}

init(){
    PWD_DIR=`pwd`
    echo "init..."
    if [ ! -d $TARGET_DIR ];then
        mkdir -p $TARGET_DIR
    fi
    if [ "$1" ];then
        echo $1
        echo "Down server..."
        cd $TARGET_DIR
        docker-compose -f $1 down
    fi
    if [ "$CLEAN" ];then
        echo "Clean target directory..."
        rm -rf $TARGET_DIR/*
    fi
    cd $PWD_DIR
}

echo  "Start deploy $START ..."
echo  "DIR: $TARGET_DIR, ENV: $ENV, CLEAN: $CLEAN"

case "$START" in
    db) db_deploy ;;
    ui) ui_deploy ;;
    api) api_deploy ;;
    pusher) pusher_deploy ;;
    crawler) crawler_deploy ;;
    browser) browser_deploy ;;
    *) usage ;;
esac

exit 0