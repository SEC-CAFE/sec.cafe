<template>
  <div class="rounded-lg border border-slate-200 dark:border-slate-800 dark:bg-gradient-to-t dark:from-slate-800 dark:to-slate-800/30 p-5">
    <div class="font-aspekta font-[650] mb-3">友情链接</div>
    <ul class="space-y-3">
      <li v-for="item in globalConfig.friendLinks" :key="item.url">
        <span class="text-sky-500 mr-2">—</span>
          <a :href="item.url" target="_blank" class="font-aspekta font-[650] text-sm inline-flex relative hover:text-sky-500 duration-150 ease-out before:scale-x-0 before:origin-center before:absolute before:inset-0 before:bg-sky-200 dark:before:bg-sky-500 before:opacity-30 before:-z-10 before:translate-y-1/4 before:-rotate-2 hover:before:scale-100 before:duration-150 before:ease-in-out">
            {{ item.name }}
          </a>
      </li>
    </ul>
  </div>
</template>

<script>
import { inject } from 'vue'

export default {
  name: 'WidgetLinks',
  setup() {
    const globalConfig = inject('globalConfig')
    return { globalConfig }
  }
}
</script>
