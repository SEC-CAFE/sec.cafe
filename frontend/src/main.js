import { createApp } from 'vue'
import axios from 'axios'
import {createHead} from '@vueuse/head'
import { createPinia } from 'pinia'

import router from './router'
import App from './App.vue'
import store from './store'

import './css/style.css'

const pinia = createPinia()
const app = createApp(App)

const parseJsonConfig = (value, fallback) => {
  if (!value) return fallback
  try {
    return JSON.parse(value)
  } catch (e) {
    return fallback
  }
}

const optionalScripts = {
  ads: null,
  umami: null
}

const ensureGoogleAdsScript = (client) => {
  if (!client || optionalScripts.ads) return
  const script = document.createElement('script')
  script.async = true
  script.src = `https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${client}`
  script.crossOrigin = 'anonymous'
  document.head.appendChild(script)
  optionalScripts.ads = script
}

const ensureUmamiScript = (scriptUrl, websiteId) => {
  if (!scriptUrl || !websiteId || optionalScripts.umami) return
  const script = document.createElement('script')
  script.async = true
  script.src = scriptUrl
  script.setAttribute('data-website-id', websiteId)
  document.body.appendChild(script)
  optionalScripts.umami = script
}

try {
  let user = JSON.parse(localStorage.getItem('sec_cafe_user'));
  let token_obj = user.access_token;
  let access_token = token_obj == null ? '' : token_obj.token;
  axios.defaults.headers.common['Authorization'] = 'Bearer '+ access_token;
} catch (e) {
  localStorage.removeItem('sec_cafe_token');
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
  googleAdsClient: import.meta.env.VITE_APP_GOOGLE_ADS_CLIENT || '',
  googleAdsSlot: import.meta.env.VITE_APP_GOOGLE_ADS_SLOT || '',
  umamiScriptUrl: import.meta.env.VITE_APP_UMAMI_SCRIPT_URL || '',
  umamiWebsiteId: import.meta.env.VITE_APP_UMAMI_WEBSITE_ID || '',
  footerSlogan: import.meta.env.VITE_APP_FOOTER_SLOGAN || '',
  spiderUa: import.meta.env.VITE_APP_SPIDER_UA || 'sec_cafe(https://sec.cafe/spider)',
  friendLinks: parseJsonConfig(import.meta.env.VITE_APP_FRIEND_LINKS, [
    { name: 'SEC.CAFE 安全咖啡', url: 'https://sec.cafe?ref=github_opensource' },
    { name: 'SECSOSO 安全搜搜', url: 'https://secsoso.com?ref=https://sec.cafe' },
    { name: "Fooying's Blog", url: 'https://www.fooying.com?ref=https://sec.cafe' }
  ])
});

ensureGoogleAdsScript(import.meta.env.VITE_APP_GOOGLE_ADS_CLIENT)
ensureUmamiScript(import.meta.env.VITE_APP_UMAMI_SCRIPT_URL, import.meta.env.VITE_APP_UMAMI_WEBSITE_ID)

app.use(pinia)
app.use(router)
app.use(store);
app.use(createHead());
app.mount('#app')
