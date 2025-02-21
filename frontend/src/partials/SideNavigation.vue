<template>
  <div class="sticky top-0 w-16 md:w-24 shrink-0 h-screen overflow-y-auto no-scrollbar border-r border-slate-200 dark:border-slate-800">
    <div class="h-full flex flex-col justify-between after:flex-1 after:mt-auto">
      <div class="flex-1 grow flex items-center">
        <nav class="w-full">
          <ul class="space-y-4">
            <li class="py-2">
              <router-link to="/" custom v-slot="{ href, navigate, isExactActive }">
                <a class="w-full h-6 flex items-center justify-center relative after:absolute after:w-0.5 after:right-0 after:top-0 after:bottom-0" :class="currentRoute.fullPath !== '/about' && currentRoute.fullPath !== '/subscribe' ? 'text-sky-500 after:bg-sky-500' : 'text-slate-400 hover:text-slate-500 dark:text-slate-500 dark:hover:text-slate-400'" :href="href" @click="navigate">
                  <span class="sr-only">情报推送</span>
                  情报推送
                </a>
              </router-link>
            </li>
            <!--
            <li class="py-2">
              <router-link to="/about" custom v-slot="{ href, navigate, isExactActive }">
                <a class="w-full h-6 flex items-center justify-center relative after:absolute after:w-0.5 after:right-0 after:top-0 after:bottom-0" :class="isExactActive ? 'text-sky-500 after:bg-sky-500' : 'text-slate-400 hover:text-slate-500 dark:text-slate-500 dark:hover:text-slate-400'" :href="href" @click="navigate">
                  <span class="sr-only">About</span>
                  <svg class="fill-current" xmlns="http://www.w3.org/2000/svg" width="20" height="20">
                    <path fill-opacity=".16" d="M10 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8Z" />
                    <path d="M9 5h2v2H9V5Zm0 4h2v6H9V9Zm1-9C4.48 0 0 4.48 0 10s4.48 10 10 10 10-4.48 10-10S15.52 0 10 0Zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8Z" />
                  </svg>
                </a>
              </router-link>
            </li>
            <li class="py-2">
              <router-link to="/subscribe" custom v-slot="{ href, navigate, isExactActive }">
                <a class="w-full h-6 flex items-center justify-center relative after:absolute after:w-0.5 after:right-0 after:top-0 after:bottom-0" :class="isExactActive ? 'text-sky-500 after:bg-sky-500' : 'text-slate-400 hover:text-slate-500 dark:text-slate-500 dark:hover:text-slate-400'" :href="href" @click="navigate">
                  <span class="sr-only">Subscribe</span>
                  <svg class="fill-current" xmlns="http://www.w3.org/2000/svg" width="21" height="21">
                    <path fill-opacity=".16" d="m13.4 18-3-7.4-7.4-3L19 2z" />
                    <path d="M13.331 15.169 17.37 3.63 5.831 7.669l5.337 2.163 2.163 5.337Zm-3.699-3.801L.17 7.53 20.63.37l-7.161 20.461-3.837-9.463Z" />
                  </svg>
                </a>
              </router-link>
            </li>
            -->
          </ul>
        </nav>
      </div>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'

export default {
  name: 'SideNavigation',
  setup() {
    const currentRoute = useRouter().currentRoute.value

    return {
      currentRoute,
    }
  }
}
</script>
