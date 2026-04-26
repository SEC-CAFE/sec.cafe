import { createApp } from 'vue'
import axios from 'axios'
import {createHead} from '@vueuse/head'

import router from './router'
import App from './App.vue'
import store from './store'

import './css/style.css'

const app = createApp(App)

const parseJsonConfig = (value, fallback) => {
  if (!value) return fallback
  try {
    return JSON.parse(value)
  } catch (e) {
    return fallback
  }
}

const parseBool = (value, fallback = false) => {
  if (value === undefined || value === null || value === '') return fallback
  return ['1', 'true', 'yes', 'on'].includes(String(value).toLowerCase())
}

const optionalScripts = {
  ads: null,
  umami: null,
  baiduHm: null
}

const UMAMI_SCRIPT_URL = 'https://analytics.umami.is/script.js'

const ensureGoogleAdsScript = (client) => {
  if (!client || optionalScripts.ads) return
  const script = document.createElement('script')
  script.async = true
  script.src = `https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${client}`
  script.crossOrigin = 'anonymous'
  document.head.appendChild(script)
  optionalScripts.ads = script
}

const ensureUmamiScript = (websiteId) => {
  if (!websiteId || optionalScripts.umami) return
  const script = document.createElement('script')
  script.async = true
  script.src = UMAMI_SCRIPT_URL
  script.setAttribute('data-website-id', websiteId)
  document.body.appendChild(script)
  optionalScripts.umami = script
}

const ensureBaiduHmScript = (hmId) => {
  if (!hmId || optionalScripts.baiduHm) return
  window._hmt = window._hmt || []
  const script = document.createElement('script')
  script.async = true
  script.src = `https://hm.baidu.com/hm.js?${hmId}`
  document.body.appendChild(script)
  optionalScripts.baiduHm = script
}

try {
  let user = JSON.parse(localStorage.getItem('sec_cafe_user'));
  let token_obj = user.access_token;
  let access_token = token_obj == null ? '' : token_obj.token;
  axios.defaults.headers.common['Authorization'] = 'Bearer '+ access_token;
} catch (e) {
  localStorage.removeItem('sec_cafe_user');
}

axios.defaults.withCredentials = true;
axios.defaults.baseURL = import.meta.env.VITE_APP_BASE_API;

window.addGoogleAds = function () {
  const nodes = document.getElementsByClassName('addGoogleItem')
  for (let index = 0; index < nodes.length; index++) {
    (window.adsbygoogle = window.adsbygoogle || []).push({})
  }
}


axios.interceptors.response.use(
  response => {
    const headers = response.headers;
    let access_token = headers['set-access-token'];
    let expire = headers['set-access-token-expire'];
    if (access_token) {
      const params = {
        access_token: access_token,
        expire: expire,
      };
      store.dispatch('getMe', params);
    }
    return response
  },
  error => {
    if (error) {
      const originalRequest = error.config || {};
      if (error.response && error.response.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;
        store.dispatch('logOut');
        localStorage.removeItem('sec_cafe_redirect');
        localStorage.setItem('sec_cafe_redirect', window.location.href);
        return router.push('/auth/login')
      }
    }
    return Promise.reject(error)
  }
);

app.provide('globalConfig', {
  siteTitle: import.meta.env.VITE_APP_TITLE,
  siteDescript: import.meta.env.VITE_APP_DESCRIPT,
  siteKeywords: import.meta.env.VITE_APP_KEYWORDS,
  icpNum: import.meta.env.VITE_APP_ICP_NUM,
  gaNum: import.meta.env.VITE_APP_GA_NUM,
  gaCode: import.meta.env.VITE_APP_GA_CODE,
  baiduHmId: import.meta.env.VITE_APP_BAIDU_HM_ID || '',
  googleAdsClient: import.meta.env.VITE_APP_GOOGLE_ADS_CLIENT || '',
  googleAdsSlot: import.meta.env.VITE_APP_GOOGLE_ADS_SLOT || '',
  umamiWebsiteId: import.meta.env.VITE_APP_UMAMI_WEBSITE_ID || '',
  footerSlogan: import.meta.env.VITE_APP_FOOTER_SLOGAN || '',
  footerProjectShow: parseBool(import.meta.env.VITE_APP_FOOTER_PROJECT_SHOW, true),
  footerProjectText: import.meta.env.VITE_APP_FOOTER_PROJECT_TEXT || "A Fooying's Project",
  footerProjectUrl: import.meta.env.VITE_APP_FOOTER_PROJECT_URL || 'https://www.fooying.com',
  footerProjectLogo: import.meta.env.VITE_APP_FOOTER_PROJECT_LOGO || 'fooying-logo.png',
  copyrightText: import.meta.env.VITE_APP_COPYRIGHT_TEXT || 'Copyright © SEC.CAFE.',
  spiderUa: import.meta.env.VITE_APP_SPIDER_UA || 'sec_cafe(https://sec.cafe/spider)',
  showSponsorPage: parseBool(import.meta.env.VITE_APP_SHOW_SPONSOR_PAGE, false),
  showBookRecommend: parseBool(import.meta.env.VITE_APP_SHOW_BOOK_RECOMMEND, false),
  showAdsBlock: parseBool(import.meta.env.VITE_APP_SHOW_AD_BLOCK, false),
  showYearlySponsors: parseBool(import.meta.env.VITE_APP_SHOW_YEARLY_SPONSORS, false),
  navExternalLinks: parseJsonConfig(import.meta.env.VITE_APP_NAV_EXTERNAL_LINKS, [
    { name: '安全手册', url: import.meta.env.VITE_APP_HANDBOOK_URL || '/handbook', position: 'main' },
    { name: '安全搜搜', url: import.meta.env.VITE_APP_SECSOSO_URL || 'https://secsoso.com?ref=https://sec.cafe', position: 'main', badge: 'beta' },
    { name: 'API文档', url: import.meta.env.VITE_APP_API_DOCS_URL || 'https://api.sec.cafe/docs', position: 'help' }
  ]),
  handbookUrl: import.meta.env.VITE_APP_HANDBOOK_URL || '/handbook',
  secsosoUrl: import.meta.env.VITE_APP_SECSOSO_URL || 'https://secsoso.com?ref=https://sec.cafe',
  apiDocsUrl: import.meta.env.VITE_APP_API_DOCS_URL || 'https://api.sec.cafe/docs',
  contactEmail: import.meta.env.VITE_APP_CONTACT_EMAIL || 'f00y1n9@gmail.com',
  contactWechat: import.meta.env.VITE_APP_CONTACT_WECHAT || 'fooying',
  contactGroupHint: import.meta.env.VITE_APP_CONTACT_GROUP_HINT || '微信群请添加微信[_ffff01]为好友邀请进群！',
  friendLinks: parseJsonConfig(import.meta.env.VITE_APP_FRIEND_LINKS, [
    { name: 'SEC.CAFE 安全咖啡', url: 'https://sec.cafe?ref=github_opensource' },
    { name: 'SECSOSO 安全搜搜', url: 'https://secsoso.com?ref=https://sec.cafe' },
    { name: "Fooying's Blog", url: 'https://www.fooying.com?ref=https://sec.cafe' }
  ])
});

ensureGoogleAdsScript(import.meta.env.VITE_APP_GOOGLE_ADS_CLIENT)
ensureUmamiScript(import.meta.env.VITE_APP_UMAMI_WEBSITE_ID)
ensureBaiduHmScript(import.meta.env.VITE_APP_BAIDU_HM_ID)

app.use(router)
app.use(store);
app.use(createHead());
app.mount('#app')
