<template>
  <div v-if="showBookRecommend" class="rounded-lg border border-slate-200 dark:border-slate-800 dark:bg-gradient-to-t dark:from-slate-800 dark:to-slate-800/30 p-5">
    <div class="flex items-center space-x-3 mb-2">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="28">
        <path fill="#38BDF8" fill-rule="evenodd" d="M7.5 6v.75H5.513c-.96 0-1.764.724-1.865 1.679l-1.263 12A1.875 1.875 0 0 0 4.25 22.5h15.5a1.875 1.875 0 0 0 1.865-2.071l-1.263-12a1.875 1.875 0 0 0-1.865-1.679H16.5V6a4.5 4.5 0 1 0-9 0ZM12 3a3 3 0 0 0-3 3v.75h6V6a3 3 0 0 0-3-3Zm-3 8.25a3 3 0 1 0 6 0v-.75a.75.75 0 0 1 1.5 0v.75a4.5 4.5 0 1 1-9 0v-.75a.75.75 0 0 1 1.5 0v.75Z" clip-rule="evenodd" />
      </svg>
      <span class="text-xs text-slate-400 dark:text-slate-500">好书推荐</span>
    </div>
    <div class="text-center">
      <a href="https://s.click.taobao.com/D3ISYlt" target="_blank" title="套装 官网正版 红蓝攻防实战演练 共2册 红蓝攻防 构建实战化网络安全防御体系+ATT&CK视角下的红蓝对抗实战指南  ¥168">
        <img class="inline-flex" src="../images/ad1.jpeg" width="300"/>
      </a>
    </div>
  </div>

  <div v-if="showGoogleAds" class="rounded-lg border border-slate-200 dark:border-slate-800 dark:bg-gradient-to-t dark:from-slate-800 dark:to-slate-800/30 p-5">
    <div class="flex items-center space-x-3 mb-2">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20px">
        <path fill="#38BDF8" fill-rule="evenodd" d="M9 4.5a.75.75 0 0 1 .721.544l.813 2.846a3.75 3.75 0 0 0 2.576 2.576l2.846.813a.75.75 0 0 1 0 1.442l-2.846.813a3.75 3.75 0 0 0-2.576 2.576l-.813 2.846a.75.75 0 0 1-1.442 0l-.813-2.846a3.75 3.75 0 0 0-2.576-2.576l-2.846-.813a.75.75 0 0 1 0-1.442l2.846-.813A3.75 3.75 0 0 0 7.466 7.89l.813-2.846A.75.75 0 0 1 9 4.5Z" clip-rule="evenodd" />
      </svg>
      <span class="text-xs text-slate-400 dark:text-slate-500">AD</span>
    </div>
    <div class="text-center addGoogleItem">
      <ins class="adsbygoogle"
        style="display:inline-block;width:210px;height:400px"
        :data-ad-client="globalConfig.googleAdsClient"
        :data-ad-slot="globalConfig.googleAdsSlot"></ins>
    </div>
  </div>
</template>

<script>
import { computed, inject, onMounted } from 'vue'

export default {
  name: 'WidgetAds',
  setup() {
    const globalConfig = inject('globalConfig')
    const showBookRecommend = computed(() => !!globalConfig.showBookRecommend)
    const showGoogleAds = computed(() => !!(globalConfig.showAdsBlock && globalConfig.googleAdsClient && globalConfig.googleAdsSlot))

    onMounted(() => {
      if (showGoogleAds.value && typeof window.addGoogleAds === 'function') {
        window.addGoogleAds()
      }
    })

    return {
      globalConfig,
      showBookRecommend,
      showGoogleAds
    }
  }
}
</script>
