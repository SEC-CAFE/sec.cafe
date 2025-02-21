import { createRouter, createWebHistory } from 'vue-router'
import Home from './pages/Home.vue'
import About from './pages/About.vue'
import Sponsor from './pages/Sponsor.vue'
import SettingsVuliPush from './pages/SettingsVuliPush.vue'
import Links from './pages/Links.vue'
import Spider from './pages/Spider.vue'
import Login from './pages/Login.vue'
import LoginCallback from './pages/LoginCallback.vue'

import { useAuthStore } from './store/modules/auth'

const routerHistory = createWebHistory()

const router = createRouter({
  scrollBehavior(to) {
    if (to.hash) {
      window.scroll({ top: 0 })
    } else {
      document.querySelector('html').style.scrollBehavior = 'auto'
      window.scroll({ top: 0 })
      document.querySelector('html').style.scrollBehavior = ''
    }
  },
  history: routerHistory,
  routes: [
    {
      path: '/',
      component: Home
    },
    {
      path: '/Links',
      component: Links
    },
    {
      path: '/about',
      component: About
    },
    {
      path: '/sponsor',
      component: Sponsor
    },
    {
      path: '/spider',
      component: Spider
    },
    {
      path: '/settings',
      component: SettingsVuliPush,
      meta: {requiresAuth: true}
    },
    {
      path: '/auth/login',
      component: Login
    },
    {
      path: '/auth/callback',
      component: LoginCallback
    },
  ]
})

router.beforeEach((to, from, next) => {
  const authUser = useAuthStore();
  authUser.checkUser();
  const isAuthenticated = authUser.isLoggedIn;
  if (to.meta.requiresAuth && !isAuthenticated) {
    localStorage.removeItem('sec_cafe_redirect');
    localStorage.setItem('sec_cafe_redirect', to.path);
    next('/auth/login')
  }else{
    next();
  }
})

export default router
