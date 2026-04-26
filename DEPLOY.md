
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
* 修改`backend/.envs/prod.env` 配置(这里默认`prod.db.env`配置已配置，如未修改，则一并要配置)
* 修改 `frontend/.env.production`（站点标题、备案、导航外链、广告/赞助模块开关、联系方式等）
* 如需调整页面文案内容，更新：
  * `frontend/src/config/about.config.js`
  * `frontend/src/config/sponsor.config.js`
* 进入`frontend`目录，执行以下命令`npm install;npm run build`进行构建(生成`dist`文件夹)
* 将`deploy`、`backend`、`frontend/dist`上传到目标服务器任意目录
* 进入`deploy`目录，执行`chmod +x deploy.sh;sh deploy.sh -s ui -t 目标目录 -e prod --clean` 完成服务启动(可通过`docker ps -a`是否启动了名为`sec_cafe_backend`的容器)
* 如需脚本自动挂载并重载nginx，请在执行前设置环境变量：
  * `NGINX_CONF_DIR`（如`/data/nginx/conf.d`）
  * `NGINX_SITE_CONF_NAME`（可选，默认`sec.cafe.conf`）
  * `NGINX_RELOAD_CONTAINER`（可选，默认`nginx`）
* 若未设置 `NGINX_CONF_DIR`，脚本仅部署容器，不会自动修改宿主机nginx配置

#### API部署
API部署同理backend部署
* 修改`backend/.envs/prod.env` 配置(这里默认`prod.db.env`配置已配置，如未修改，则一并要配置)
* 将`deploy`、`backend`上传到目标服务器任意目录
* 进入`deploy`目录，执行`chmod +x deploy.sh;sh deploy.sh -s api -t 目标目录 -e prod --clean` 完成服务启动(可通过`docker ps -a`是否启动了名为`sec_cafe_api`的容器)
* 可复用 UI 部署中的 `NGINX_CONF_DIR` / `NGINX_SITE_CONF_NAME` / `NGINX_RELOAD_CONTAINER` 配置实现自动重载

#### crawler及pusher 部署
* 修改`backend/.envs/prod.crawler.env` 配置
  * 爬虫UA：`REQ_UA`
  * AI判重：`OPENAPI_KEY`、`OPENAPI_BASE_URL`、`OPENAPI_MODEL`
  * AI判重阈值与提示词：`VUL_SIMILARITY_*`
* 将`deploy`、`backend`上传到目标服务器任意目录
* 进入`deploy`目录，执行`chmod +x deploy.sh;sh deploy.sh -s 项目名 -t 目标目录 -e prod --clean` 完成服务启动
* crawler的项目名为`crawler`;pusher项目名为`pusher`

#### browser与代理（可选）
如果需要为爬虫启用远程浏览器与代理，可使用以下部署文件：
* `deploy/docker-compose.browser.yml`
* `deploy/docker-compose.proxy.yml`
* `deploy/v2_config.example.json`（复制为本地 `deploy/v2_config.json` 并填入真实配置）


### 如何使用github workflows部署
* 在对应github项目 Settings -> Secrets and Variables -> Actions 添加以下 Secrets（可按 UI/API 与 crawler/pusher 分开）：
  * UI_DEPLOY_HOST
  * UI_DEPLOY_PORT
  * UI_DEPLOY_USER
  * CRAWLER_DEPLOY_HOST
  * CRAWLER_DEPLOY_PORT
  * CRAWLER_DEPLOY_USER
  * DEPLOY_PRIVATE_KEY
* 项目Actions即可手动触发进行部署(如果部署在同一天服务，请等待其他任务执行完成再进行下一个任务)

### 前端配置建议
为了避免每次都改代码，建议以“环境变量 + 配置文件”方式维护页面内容：
* 环境变量文件：`frontend/.env.production`
* 关于我们内容：`frontend/src/config/about.config.js`
* 赞助页内容：`frontend/src/config/sponsor.config.js`
* 推荐流程：先更新配置，再 `npm run build`，最后走 UI 部署流程。

### 可配置项速查
#### 前端环境变量（`frontend/.env.production`）
* 站点信息：`VITE_APP_TITLE`、`VITE_APP_DESCRIPT`、`VITE_APP_KEYWORDS`
* 备案与版权：`VITE_APP_ICP_NUM`、`VITE_APP_GA_NUM`、`VITE_APP_GA_CODE`、`VITE_APP_COPYRIGHT_TEXT`
* 统计与广告：`VITE_APP_UMAMI_WEBSITE_ID`、`VITE_APP_BAIDU_HM_ID`、`VITE_APP_GOOGLE_ADS_*`
* 页脚文案：`VITE_APP_FOOTER_SLOGAN`、`VITE_APP_FOOTER_PROJECT_*`
* 模块开关：`VITE_APP_SHOW_SPONSOR_PAGE`、`VITE_APP_SHOW_UPDATE_WIDGET`、`VITE_APP_SHOW_BOOK_RECOMMEND`、`VITE_APP_SHOW_AD_BLOCK`、`VITE_APP_SHOW_YEARLY_SPONSORS`
* 导航外链：`VITE_APP_NAV_EXTERNAL_LINKS`（JSON数组，可配置任意数量；`position=main/help`）
* 联系方式与友情链接：`VITE_APP_CONTACT_*`、`VITE_APP_FRIEND_LINKS`
* 爬虫说明页UA展示：`VITE_APP_SPIDER_UA`

#### 前端内容配置文件
* 关于我们：`frontend/src/config/about.config.js`
* 赞助页/年度赞助商：`frontend/src/config/sponsor.config.js`
* 更新公告：`frontend/src/config/update.config.js`

#### 后端爬虫配置（`backend/.envs/prod.crawler.env`）
* 请求配置：`REQ_UA`、`REQ_VERIFY_SSL`
* AI判重模型：`OPENAPI_KEY`、`OPENAPI_BASE_URL`、`OPENAPI_MODEL`
* AI判重策略：`VUL_SIMILARITY_*`

#### 私有部署配置（本地保留）
* `deploy/v2_config.json`：真实代理配置（不提交，已在 `.gitignore`）
* `deploy/v2_config.example.json`：模板配置（可提交）


### 导入links.sql
如果使用导航功能，针对src和vuldb，也提供了db文件，需要手动导入


### 针对github登录失败问题
由于网络问题，如果UI服务部署在国内站点，有一定概率会导致失败
可以通过配置`environment`为后台服务配置代理，定向配置`.github.com`经过代理服务
