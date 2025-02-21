
### 部署说明
项目采用容器化部署，实际部署需要分别UI、API、Crawler、Pusher，具体启动方式可参考对应的docker-compose配置文件，同时项目也支持github workflows部署，提供了deploy脚本(部署前请提前安装好docker及docker-compose).

先完成DB服务部署，后再部署其他服务。

#### DB部署
clone项目后，修改`backend/.envs/prod.db.env`的配置，进入deploy目录，给deploy.sh添加执行权限`chmod +x deploy.sh`，然后直接执行
```
./deploy.sh -s db -e prod -t 目标目录 --clean
```
注：添加`--clean`参数会先对目标目录进行清空处理
也可以独立部署，无需复制整个项目：
* 修改`prod.db.env` 中的配置并复制到部署目录下，重命名为.env
* 复制`docker-compose.db.yml`及`pgsql.conf`到部署目录
* 执行`docker-compose -f docker-compose.db.yml up -d` 即可完成启动

#### UI部署
UI为前后端分离，可通过`deploy.sh`部署，也可分别独立部署，以下为使用`deploy.sh`部署方式
* 修改`.env/prod.env` 配置(这里默认`prod.db.env`配置已配置，如未修改，则一并要配置)
* 进入`frontend`目录，执行以下命令`npm install;npm run build`进行构建(生成`dist`文件夹)
* 将`deploy`、`backend`、`frontend/dist`上传到目标服务器任意目录
* 进入`deploy`目录，执行`chmod +x deploy.sh;sh deploy.sh -s ui -t 目标目录 -e prod --clean` 完成服务启动(可通过`docker ps -a`是否启动了名为`sec_cafe_backend`的容器)
* 修改`nginx/ui_nginx.conf`配置，并include到nginx配置中，重启nginx即可

#### API部署
API部署同理backend部署
* 修改`.env/prod.env` 配置(这里默认`prod.db.env`配置已配置，如未修改，则一并要配置)
* 将`deploy`、`backend`上传到目标服务器任意目录
* 进入`deploy`目录，执行`chmod +x deploy.sh;sh deploy.sh -s api -t 目标目录 -e prod --clean` 完成服务启动(可通过`docker ps -a`是否启动了名为`sec_cafe_api`的容器)
* 修改`nginx/ui_nginx.conf`配置，并include到nginx配置中，重启nginx即可

#### crawler及pusher 部署
* 修改`.env/prod.crawler.env` 配置
* 将`deploy`、`backend`上传到目标服务器任意目录
* 进入`deploy`目录，执行`chmod +x deploy.sh;sh deploy.sh -s 项目名 -t 目标目录 -e prod --clean` 完成服务启动
* crawler的项目名为`crawler`;pusher项目名为`pusher`


### 如何使用github workflows部署
* 在对应github项目Settings-Secrets and Variables-Actions 添加以下Secrets，如果部署在不同服务器，可配置多个key并修改修改`.github/workflows`中yml文件
  * DEPLOY_HOST
  * DEPLOY_HOST_PORT
  * DEPLOY_PRIVATE_KEY
  * DEPLOY_HOST_USER
* 项目Actions即可手动触发进行部署(如果部署在同一天服务，请等待其他任务执行完成再进行下一个任务)


### 导入links.sql
如果使用导航功能，针对src和vuldb，也提供了db文件，需要手动导入


### 针对github登录失败问题
由于网络问题，如果UI服务部署在国内站点，有一定概率会导致失败
可以通过配置`environment`为后台服务配置代理，定向配置`.github.com`经过代理服务