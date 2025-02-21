
<template>
  <!--
    This example requires updating your template:

    ```
    <html class="h-full bg-white">
    <body class="h-full">
    ```
  -->
  <div class="flex min-h-full flex-1 flex-col items-center justify-center px-6 py-12 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-sm">
      <div class="shrink-0 mr-4 text-center">
          <!-- Logo -->
        <router-link to="/" class="block" :aria-label=siteTitle>
          <h3 class="font-aspekta text-lg font-[650] mb-1">
            <a class="inline-flex relative text-sky-500 before:absolute before:inset-0 before:bg-sky-200 dark:before:bg-sky-500 before:opacity-30 before:-z-10 before:-rotate-2 before:translate-y-1/4">
              {{ siteTitle }}
            </a>
          </h3>
        </router-link>
      </div>
    </div>

    <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
      <div>
        <div class="relative mt-10">
          <div class="absolute inset-0 flex items-center" aria-hidden="true">
            <div class="w-full border-t border-gray-200" />
          </div>
          <div class="relative flex justify-center text-sm font-medium leading-6">
            <span class="bg-white px-6 text-gray-900">登录中，请稍候</span>
          </div>
        </div>

        <div class="mt-6 grid grid-cols-1 gap-4">
          <a href="/" class="flex w-full items-center justify-center gap-3 rounded-md bg-sky-500 px-3 py-1.5 text-white hover:bg-sky-600">
            <span class="text-sm font-semibold leading-6">没有自动跳转？返回首页</span>
          </a>
        </div>
      </div>

    </div>
  </div>
</template>
<script>
import { inject } from 'vue';
import { useHead } from '@vueuse/head'
export default {
  name: 'LoginCallback',
  setup() {
    const globalConfig = inject('globalConfig');
    const siteTitle = globalConfig.siteTitle;
    const pageKeywords = '';
    useHead({
      title: '登录跳转',
      titleTemplate: '%s | ' + globalConfig.siteTitle,
      meta: [
        {
          name: 'description',
          content: globalConfig.siteDescript
        },
        {
          name: 'keywords',
          content: globalConfig.siteKeywords + pageKeywords
        }
      ]
    });
    return {
      siteTitle
    }
  },
  created: function() {
    return this.$store.dispatch('apiCallback');
  }
}
</script>
