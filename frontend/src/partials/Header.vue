<template>
  <header class="fixed w-full z-30 md:bg-opacity-90 transition duration-300 ease-in-out" :class="{ 'bg-white dark:bg-slate-900 backdrop-blur-sm shadow-lg dark:shadow-sky-950': !top }">
    <div class="w-full max-w-[1072px] mx-auto flex items-center justify-between h-16 before:block px-6">
      <div class="shrink-0 mr-4">
          <!-- Logo -->
          <router-link to="/" class="block" aria-label="SEC.CAFE">
            <h3 class="font-aspekta text-lg font-[650] mb-1">
            <a class="inline-flex relative text-sky-500 before:absolute before:inset-0 before:bg-sky-200 dark:before:bg-sky-500 before:opacity-30 before:-z-10 before:-rotate-2 before:translate-y-1/4">
              {{ siteTitle }}
            </a>
            </h3>
          </router-link>
        </div>

      <nav class="hidden md:flex md:grow">
        <!-- Desktop menu links -->
        <ul class="flex grow justify-end flex-wrap items-center font-medium">
          <li class="px-3">
            <router-link class="" to="/"   v-slot="{ href, navigate, isExactActive }" >
              <a class="block py-1" :class="isExactActive ? 'text-sky-500 after:bg-sky-500' : 'text-slate-800 dark:text-slate-100 hover:text-slate-600 dark:hover:text-slate-300'" :href="href" @click="navigate">
                漏洞情报
              </a>
            </router-link>
          </li>
          <li class="px-3">
            <!--
            <a class="block py-1  mr-4 text-slate-800 dark:text-slate-100 hover:text-slate-600 dark:hover:text-slate-300" href="/handbook">
              安全手册
              <span class="text-xs absolute mr-2.5 mb-2.5">beta</span>
            </a>
            -->
            <a class="block py-1 text-slate-800 dark:text-slate-100 hover:text-slate-600 dark:hover:text-slate-300" href="https://sec.cafe/handbook">
              安全手册            </a>
          </li>
          <li class="px-3">
            <a class="block py-1  mr-4 text-slate-800 dark:text-slate-100 hover:text-slate-600 dark:hover:text-slate-300" target="_blank" href="https://secsoso.com">
              安全搜搜
              <span class="text-xs absolute mr-2.5 mb-2.5">beta</span>
            </a>
          </li>

          <li class="px-3">
            <router-link class="" to="/links" v-slot="{ href, navigate, isExactActive }" >
              <a class="block py-1" :class="isExactActive ? 'text-sky-500 after:bg-sky-500' : 'text-slate-800 dark:text-slate-100 hover:text-slate-600 dark:hover:text-slate-300'" :href="href" @click="navigate">安全导航</a>
            </router-link>
          </li>
          <li class="ml-6 flex items-center" >
            <Dropdown title="帮助" :vip=0 vip_tip="">
              <li v-show="!user.nickname">
                <router-link class="" to="/settings" v-slot="{ href, navigate, isExactActive }" >
                  <a class="font-medium text-sm  flex py-2 px-5 leading-tight cursor-pointer" :class="isExactActive ? 'text-sky-500 after:bg-sky-500' : 'text-gray-600 dark:text-slate-400 hover:text-gray-900 dark:hover:text-slate-100'" :href="href" @click="navigate">订阅</a>
                </router-link>
              </li>
              <li>
                <a class="font-medium text-sm text-gray-600 dark:text-slate-400 hover:text-gray-900 dark:hover:text-slate-100 flex py-2 px-5 leading-tight cursor-pointer" href="https://api.sec.cafe/docs" target="_blank">API文档</a>
              </li>
              <li>
                <a class="font-medium text-sm text-gray-600 dark:text-slate-400 hover:text-gray-900 dark:hover:text-slate-100 flex py-2 px-5 leading-tight cursor-pointer" href="https://discord.gg/WXSvykbYDb" target="_blank">Discord社区</a>
              </li>
              <li>
                <router-link class="" to="/about" v-slot="{ href, navigate, isExactActive }" >
                  <a class="font-medium text-sm  flex py-2 px-5 leading-tight cursor-pointer" :class="isExactActive ? 'text-sky-500 after:bg-sky-500' : 'text-gray-600 dark:text-slate-400 hover:text-gray-900 dark:hover:text-slate-100'" :href="href" @click="navigate">关于</a>
                </router-link>
              </li>
              <li>
                <router-link class="" to="/sponsor" v-slot="{ href, navigate, isExactActive }" >
                  <a class="font-medium text-sm  flex py-2 px-5 leading-tight cursor-pointer" :class="isExactActive ? 'text-sky-500 after:bg-sky-500' : 'text-gray-600 dark:text-slate-400 hover:text-gray-900 dark:hover:text-slate-100'" :href="href" @click="navigate">打赏赞助</a>
                </router-link>
              </li>
            </Dropdown>
          </li>

          <li v-if="user.nickname" class="ml-6 flex items-center">
            <Dropdown :title="user.nickname" :vip="user.vip.type" :vip_tip="'VIP过期时间: ' +user.vip.expire_time">
              <li>
                <a class="font-medium text-sm text-gray-600 dark:text-slate-400 hover:text-gray-900 dark:hover:text-slate-100 flex py-2 px-5 leading-tight cursor-pointer" @click="showApiToken">API Token</a>
              </li>
              <li>
                <router-link class="" to="/settings"   v-slot="{ href, navigate, isExactActive }" >
                  <a class="py-2 font-medium text-sm flex px-5 leading-tight cursor-pointer" :class="isExactActive ? 'text-sky-500 after:bg-sky-500' : 'text-gray-600 dark:text-slate-400 hover:text-gray-900 dark:hover:text-slate-100'" :href="href" @click="navigate">
                    订阅设置
                  </a>
                </router-link>
              </li>
              <li>
                <a class="font-medium text-sm text-gray-600 dark:text-slate-400 hover:text-gray-900 dark:hover:text-slate-100 flex py-2 px-5 leading-tight cursor-pointer" @click="logOut">退出</a>
              </li>
            </Dropdown>
          </li>
          <li v-else class="ml-6">
            <router-link to="/auth/login" class="cursor-pointer block py-1 text-slate-800  hover:text-slate-600 dark:text-slate-100 dark:hover:text-slate-300">
              登录
            </router-link>
          </li>

          <li class="pl-1">
            <!-- Light switch -->
            <div class="flex flex-col justify-center">
              <input type="checkbox" name="light-switch" id="light-switch" v-model="darkMode" class="light-switch sr-only" />
              <label class="relative cursor-pointer p-2" for="light-switch">
                <svg class="dark:hidden" width="16" height="16" xmlns="http://www.w3.org/2000/svg">
                  <path class="fill-slate-300" d="M7 0h2v2H7zM12.88 1.637l1.414 1.415-1.415 1.413-1.413-1.414zM14 7h2v2h-2zM12.95 14.433l-1.414-1.413 1.413-1.415 1.415 1.414zM7 14h2v2H7zM2.98 14.364l-1.413-1.415 1.414-1.414 1.414 1.415zM0 7h2v2H0zM3.05 1.706 4.463 3.12 3.05 4.535 1.636 3.12z" />
                  <path class="fill-slate-400" d="M8 4C5.8 4 4 5.8 4 8s1.8 4 4 4 4-1.8 4-4-1.8-4-4-4Z" />
                </svg>
                <svg class="hidden dark:block" width="16" height="16" xmlns="http://www.w3.org/2000/svg">
                  <path class="fill-slate-400" d="M6.2 1C3.2 1.8 1 4.6 1 7.9 1 11.8 4.2 15 8.1 15c3.3 0 6-2.2 6.9-5.2C9.7 11.2 4.8 6.3 6.2 1Z" />
                  <path class="fill-slate-500" d="M12.5 5a.625.625 0 0 1-.625-.625 1.252 1.252 0 0 0-1.25-1.25.625.625 0 1 1 0-1.25 1.252 1.252 0 0 0 1.25-1.25.625.625 0 1 1 1.25 0c.001.69.56 1.249 1.25 1.25a.625.625 0 1 1 0 1.25c-.69.001-1.249.56-1.25 1.25A.625.625 0 0 1 12.5 5Z" />
                </svg>
                <span class="sr-only">Switch to light / dark version</span>
              </label>
            </div>
          </li>
          <li>
            <a class="flex justify-center items-center text-slate-800 hover:text-slate-600 dark:text-slate-100 dark:hover:text-slate-300 transition duration-150 ease-in-out" href="https://github.com/SEC-CAFE" target="_blank" aria-label="Github">
              <svg class="w-8 h-8 fill-current" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
                <path d="M16 8.2c-4.4 0-8 3.6-8 8 0 3.5 2.3 6.5 5.5 7.6.4.1.5-.2.5-.4V22c-2.2.5-2.7-1-2.7-1-.4-.9-.9-1.2-.9-1.2-.7-.5.1-.5.1-.5.8.1 1.2.8 1.2.8.7 1.3 1.9.9 2.3.7.1-.5.3-.9.5-1.1-1.8-.2-3.6-.9-3.6-4 0-.9.3-1.6.8-2.1-.1-.2-.4-1 .1-2.1 0 0 .7-.2 2.2.8.6-.2 1.3-.3 2-.3s1.4.1 2 .3c1.5-1 2.2-.8 2.2-.8.4 1.1.2 1.9.1 2.1.5.6.8 1.3.8 2.1 0 3.1-1.9 3.7-3.7 3.9.3.4.6.9.6 1.6v2.2c0 .2.1.5.6.4 3.2-1.1 5.5-4.1 5.5-7.6-.1-4.4-3.7-8-8.1-8z"></path>
              </svg>
            </a>
          </li>
        </ul>

      </nav>
      <!-- Mobile menu -->
      <div class="flex md:hidden">

        <!-- Hamburger button -->
        <button class="hamburger" ref="hamburger" :class="{ active: mobileNavOpen }" aria-controls="mobile-nav" :aria-expanded="mobileNavOpen" @click="mobileNavOpen = !mobileNavOpen">
          <span class="sr-only">Menu</span>
          <svg class="w-6 h-6 fill-current text-gray-900 dark:text-sky-500" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <rect y="4" width="24" height="2" />
            <rect y="11" width="24" height="2" />
            <rect y="18" width="24" height="2" />
          </svg>
        </button>

        <!-- Mobile navigation -->
        <transition
          enter-active-class="transition ease-out duration-200 transform"
          enter-from-class="opacity-0 -translate-y-2"
          enter-to-class="opacity-100 translate-y-0"
          leave-active-class="transition ease-out duration-200"
          leave-from-class="opacity-100"
          leave-to-class="opacity-0"
        >
          <nav
            id="mobile-nav"
            ref="mobileNav"
            v-show="mobileNavOpen"
            class="absolute top-full h-screen pb-16 z-20 left-0 w-full overflow-scroll bg-white dark:bg-slate-900"
          >
            <ul class="px-5 py-2">
              <li>
                <router-link class="" to="/"   v-slot="{ href, navigate, isExactActive }" >
                  <a class="block py-1 font-medium" :class="isExactActive ? 'text-sky-500 after:bg-sky-500' : 'text-slate-800 dark:text-slate-100 hover:text-slate-600 dark:hover:text-slate-300'" :href="href" @click="navigate">
                    漏洞情报
                  </a>
                </router-link>
              </li>
              <li>
                <a class="block py-1 font-medium text-slate-800 dark:text-slate-100 hover:text-slate-600 dark:hover:text-slate-300" href="/handbook">安全手册</a>
              </li>
              <li>
                <a class="block py-1 font-medium text-slate-800 dark:text-slate-100 hover:text-slate-600 dark:hover:text-slate-300" href="https://secsoso.com?ref=https://sec.cafe" target="_blank">安全搜搜</a>
              </li>
              <li>
                <a class="block py-1 font-medium text-slate-800 dark:text-slate-100 hover:text-slate-600 dark:hover:text-slate-300" href="/links" target="_blank">安全导航</a>
              </li>
              <li>
                <a class="block py-1 font-medium text-slate-800 dark:text-slate-100 hover:text-slate-600 dark:hover:text-slate-300" href="https://api.sec.cafe/docs" target="_blank">API文档</a>
              </li>
              <li>
                <a class="block py-1 font-medium text-slate-800 dark:text-slate-100 hover:text-slate-600 dark:hover:text-slate-300" href="https://discord.gg/KNFWaRfk" target="_blank">Discord社区</a>
              </li>
              <li>
                <router-link class="" to="/about"   v-slot="{ href, navigate, isExactActive }" >
                  <a class="block py-1 font-medium" :class="isExactActive ? 'text-sky-500 after:bg-sky-500' : 'text-slate-800 dark:text-slate-100 hover:text-slate-600 dark:hover:text-slate-300'" :href="href" @click="navigate">关于</a>
                </router-link>
              </li>
              <li>
                <router-link class="" to="/sponsor"   v-slot="{ href, navigate, isExactActive }" >
                  <a class="block py-1 font-medium" :class="isExactActive ? 'text-sky-500 after:bg-sky-500' : 'text-slate-800 dark:text-slate-100 hover:text-slate-600 dark:hover:text-slate-300'" :href="href" @click="navigate">打赏赞助</a>
                </router-link>
              </li>

              <!--
              <li>
                <router-link to="/auth/login" class="btn-sm text-gray-200 bg-gray-900 hover:bg-gray-800 dark:text-slate-100 dark:bg-sky-500 w-full my-2">
                  <span>登录</span>
                </router-link>
              </li>
              -->
            </ul>
          </nav>
        </transition>

        </div>
    </div>

  </header>
  <Notification @closeNoti="closeNoti" :show="showNotification" :type="notificationType" :title="notificationTitle" :message="notificationMsg"></Notification>
</template>

<script>
import { ref, watch, inject } from 'vue'
import { mapGetters, mapActions } from 'vuex'
import { useRouter } from 'vue-router'
import Dropdown from '../components/Dropdown.vue'
import Notification from '../components/Notification.vue'

export default {
  name: 'Header',
  components: {
    Dropdown,
    Notification
  },
  data: function () {
    return {
      mobileNavOpen: false,
      top: true,
      showNotification: false,
      notificationTitle: '',
      notificationMsg: '',
      notificationType: 'info'
    }
  },
  methods: {
    clickOutside(e) {
      if (!this.mobileNavOpen || this.mobileNav.contains(e.target) || this.hamburger.contains(e.target)) return
      this.mobileNavOpen = false
    },
    keyPress(e) {
      if (!this.mobileNavOpen || e.keyCode !== 27) return
      this.mobileNavOpen = false
    },
    handleScroll() {
      var _scrollTop = window.scrollY || window.pageYOffset || document.documentElement.scrollTop
      this.top = _scrollTop > 10 ? false : true
    },
    logOut(){
      this.$store.dispatch('logOut');
      window.location.replace('/');
    },
    showNotifi(msg, title, type){
      this.notificationMsg = msg;
      this.notificationTitle = title;
      this.notificationType = type;
      this.showNotification = true;
    },
    showApiToken(){
      this.showNotifi(this.user.api_token, 'API Token', 'info');
    },
    closeNoti(){
      this.showNotification = false;
    }
  },
  mounted() {
    document.addEventListener('click', this.clickOutside)
    document.addEventListener('keydown', this.keyPress)
    document.addEventListener('scroll', this.handleScroll)
    //this.showNotifi('新功能上线提醒', '功能上线', 'warn');
    //setTimeout(this.closeNoti, 3000);
  },
  beforeUnmount() {
    document.removeEventListener('click', this.clickOutside)
    document.removeEventListener('keydown', this.keyPress)
    document.removeEventListener('scroll', this.handleScroll)
  },
  computed: {
    ...mapGetters({user: 'logined_user' }),
  },
  setup() {
    const darkMode = ref(localStorage.getItem('dark-mode'))
    const currentRoute = useRouter().currentRoute.value

    const globalConfig = inject('globalConfig');
    const siteTitle = globalConfig.siteTitle;

    watch(darkMode, () => {
      localStorage.setItem('dark-mode', darkMode.value)
      if (darkMode.value) {
        document.documentElement.classList.add('dark')
      } else {
        document.documentElement.classList.remove('dark')
      }
    })

    const mobileNav = ref();
    const hamburger = ref();

    return {
      darkMode,
      currentRoute,
      mobileNav,
      hamburger,
      siteTitle
    }
  },
}
</script>
