<template>
  <div class="rounded-lg border border-slate-200 dark:border-slate-800 dark:bg-gradient-to-t dark:from-slate-800 dark:to-slate-800/30 p-5">
    <div class="flex items-center space-x-3 mb-2">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#38BDF8" class="w-6 h-6">
        <path d="M16.881 4.345A23.112 23.112 0 0 1 8.25 6H7.5a5.25 5.25 0 0 0-.88 10.427 21.593 21.593 0 0 0 1.378 3.94c.464 1.004 1.674 1.32 2.582.796l.657-.379c.88-.508 1.165-1.593.772-2.468a17.116 17.116 0 0 1-.628-1.607c1.918.258 3.76.75 5.5 1.446A21.727 21.727 0 0 0 18 11.25c0-2.414-.393-4.735-1.119-6.905ZM18.26 3.74a23.22 23.22 0 0 1 1.24 7.51 23.22 23.22 0 0 1-1.41 7.992.75.75 0 1 0 1.409.516 24.555 24.555 0 0 0 1.415-6.43 2.992 2.992 0 0 0 .836-2.078c0-.807-.319-1.54-.836-2.078a24.65 24.65 0 0 0-1.415-6.43.75.75 0 1 0-1.409.516c.059.16.116.321.17.483Z" />
      </svg>


      <span class="text-xs text-slate-400 dark:text-slate-500">开源通知</span>
    </div>
    <div class="font-aspekta font-[650] mb-1">SEC.CAFE 现已开源!!!</div>
    <p class="text-sm text-slate-500 dark:text-slate-400">虽然SEC.CAFE提供了订阅服务，但也有很多私有化部署及情报源的定制需求，经过考虑，决定开源SEC.CAFE，这也更符合SEC.CAFE的初心，任何人都可以基于开源代码进行定制，建立自己的漏洞情报监控服务！</p>
    <div class="mt-5">
      <a class="btn-sm w-full  text-slate-100 bg-sky-500 hover:bg-sky-600" target="_blank" href="https://github.com/SEC-CAFE/sec.cafe">访问项目</a>
    </div>
  </div>


</template>

<script>
export default {
  name: 'WidgetUpdate',
}
</script>
