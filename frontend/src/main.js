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
      const originalRequest = error.config;
      if (error.response.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;
        store.dispatch('logOut');
        localStorage.removeItem('sec_cafe_redirect');
        localStorage.setItem('sec_cafe_redirect', window.location.href);
        return router.push('/auth/login')
      }
    }
  }
);

app.provide('globalConfig', {
  siteTitle: import.meta.env.VITE_APP_TITLE,
  siteDescript: import.meta.env.VITE_APP_DESCRIPT,
  siteKeywords: import.meta.env.VITE_APP_KEYWORDS,
  icpNum: import.meta.env.VITE_APP_ICP_NUM,
  gaNum: import.meta.env.VITE_APP_GA_NUM,
  gaCode: import.meta.env.VITE_APP_GA_CODE
});

app.use(pinia)
app.use(router)
app.use(store);
app.use(createHead());
app.mount('#app')
