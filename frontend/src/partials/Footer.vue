<template>
  <footer class="border-t border-slate-200 dark:border-slate-800">
    <div class="py-8 max-w-7xl mx-auto">
      <div class="text-center md:flex md:items-center md:justify-between">
        <div class="mb-4 order-2 md:ml-4 md:mb-0 space-x-2 text-xs text-slate-500 dark:text-slate-400">
          <h2 class="inline-flex md:float-right">
            <a class="pt-0.4 pl-1" href="https://sec.cafe">Powered By SEC.CAFE</a>
          </h2>
        </div>


        <!-- Copyright -->

        <div class="text-xs text-slate-400 dark:text-slate-500 md:inline-flex">
          <div class="md:text-xs text-sm text-slate-800 dark:text-slate-400">Copyright &copy; {{ globalConfig.siteTitle }}.</div>
          <a v-if=globalConfig.gaNum class="pl-1 flex items-center justify-center" :href="`https://beian.mps.gov.cn/#/query/webSearch?code=` + globalConfig.gaCode" rel="noreferrer" target="_blank">
            <img class="w-3 h-3" src="../images/logo.gabei.png">
            &nbsp;{{ globalConfig.gaNum }}
          </a>
          <a v-if=globalConfig.icpNum class="pl-1" href="https://beian.miit.gov.cn/" target="_blank">{{ globalConfig.icpNum }}</a>
        </div>

      </div>
    </div>
  </footer>
</template>

<script>
import { inject } from 'vue';

export default {
  name: 'Footer',
  setup() {
    const globalConfig = inject('globalConfig');
    return {
      globalConfig
    }
  },
}
</script>
