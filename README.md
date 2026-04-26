# sec.cafe 安全咖啡

[![License](https://img.shields.io/badge/license-MIT-red.svg)](https://github.com/SEC-CAFE/sec.cafe/tree/main?tab=MIT-1-ov-file) 
[![Sponsor](https://img.shields.io/badge/Sponsor-patreon-73d6a1)](https://sec.cafe/sponsor) 
[![Powered By](https://img.shields.io/badge/SEC.CAFE-A%20Fooying's%20Project-blue)](https://sec.cafe) 


安全本应纯粹，规避内卷，用一杯咖啡回归安全的乐趣！SEC.CAFE 安全咖啡是一个安全爱好者的服务平台与社区。最基本的功能是提供漏洞情报的监测与订阅功能，同时实现多源聚合去重。

![漏洞去重](/.github/imgs/漏洞去重.jpg)

###  功能说明
* 多源漏洞聚合去重，实现多源漏洞情报的监控，并自动化去重
* 支持RSS、API、邮件、钉钉、企业微信等多种方式情报推送
* 支持对英文漏洞情报的标题及概要的自动化中文翻译
* 简单的安全导航功能
* 支持模板的化的漏洞情报爬取配置

### 当前支持漏洞情报源
| 情报源 | 网址 | 状态 | 
| --- | --- | --- |
| 阿里云漏洞库(AVD) | https://avd.aliyun.com | 在线 | 
| 360网络安全响应中心 | https://cert.360.cn/warning | 在线 | 
| 腾讯云安全公告 | https://cloud.tencent.com/announce/?categorys=21 | 在线 | 
| 奇安信NOX漏洞库 | https://nox.qianxin.com/KeyPoint | 下线 | 
| 绿盟威胁情报中心 | https://nti.nsfocus.com/threatNotice | 在线 | 
| 深信服漏洞情报 | https://sec.sangfor.com.cn/security-vulnerability | 在线 | 
| 用友安全中心 | https://security.yonyou.com/#/noticeList | 下线 | 
| Seebug 漏洞平台 | https://www.seebug.org | 在线 | 
| 安恒星图平台 | https://ti.dbappsecurity.com.cn/vul | 在线 | 
| 奇安信威胁情报中心 | https://ti.qianxin.com/ | 在线 | 
| 长亭漏洞库 | https://stack.chaitin.com/vuldb/index | 在线 | 
| OSCS开源安全情报 | https://stack.chaitin.com/vuldb/index | 在线 | 
| 启明星辰安全通告 | https://www.venustech.com.cn/new_type/aqtg/ | 在线 | 
| 微步在线X情报社区 | https://x.threatbook.com/v5/vul/notice | 在线 | 
| CISA KEV | https://www.cisa.gov/known-exploited-vulnerabilities-catalog | 在线 | 

#### 项目技术栈
* UI：Vue3 + FastAPI + postgreSQL
* 爬虫：Celery + 自实现模板解析爬虫
* 情报推送：Celery + 自实现逻辑

采用容器化部署，也支持github workflows部署  

### 部署说明
部署请参考[部署说明](https://github.com/SEC-CAFE/sec.cafe/blob/main/DEPLOY.md)

### 可自定义配置（重点）
项目已支持大量配置化能力，常见改动不需要再改代码：

#### 前端环境变量（`frontend/.env.production`）
- 站点基础：`VITE_APP_TITLE`、`VITE_APP_DESCRIPT`、`VITE_APP_KEYWORDS`
- 备案与版权：`VITE_APP_ICP_NUM`、`VITE_APP_GA_NUM`、`VITE_APP_GA_CODE`、`VITE_APP_COPYRIGHT_TEXT`
- 分析与广告：`VITE_APP_UMAMI_*`、`VITE_APP_GOOGLE_ADS_*`
- 模块开关（默认关闭）：`VITE_APP_SHOW_SPONSOR_PAGE`、`VITE_APP_SHOW_BOOK_RECOMMEND`、`VITE_APP_SHOW_AD_BLOCK`、`VITE_APP_SHOW_YEARLY_SPONSORS`
- 导航外链：`VITE_APP_HANDBOOK_URL`、`VITE_APP_SECSOSO_URL`、`VITE_APP_API_DOCS_URL`
- 联系方式：`VITE_APP_CONTACT_EMAIL`、`VITE_APP_CONTACT_WECHAT`、`VITE_APP_CONTACT_GROUP_HINT`
- 爬虫说明页展示UA：`VITE_APP_SPIDER_UA`
- 友情链接：`VITE_APP_FRIEND_LINKS`（JSON字符串）
- 说明：`Powered By` 为项目固定标识，不提供配置项。

#### 前端内容配置文件（建议运营同学直接维护）
- 关于我们内容：`frontend/src/config/about.config.js`
- 赞助页/年度赞助商内容：`frontend/src/config/sponsor.config.js`

#### 后端爬虫与相似性配置（`backend/.envs/prod.crawler.env`）
- 爬虫请求UA：`REQ_UA`
- 请求证书校验：`REQ_VERIFY_SSL`
- AI判重：`OPENAPI_KEY`、`OPENAPI_BASE_URL`、`OPENAPI_MODEL`
- 判重阈值：`VUL_SIMILARITY_*`（时间窗口、阈值、提示词、置信度、开关等）

#### 私有部署配置文件
- `deploy/v2_config.json` 为本地私有配置，已加入 `.gitignore`。
- 开源仓库提供 `deploy/v2_config.example.json` 作为模板。

### 新增情报源
* 在`backend/crawler/worker/vuli_monitor/templates`目录下新增yml文件，yml文件配置方式请参考[爬取配置说明](https://github.com/SEC-CAFE/sec.cafe/blob/main/CRAWLER.md)
* 更新Crawler代码并重启服务
