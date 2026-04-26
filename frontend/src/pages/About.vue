<template>
  <div class="min-h-screen flex">
    <main class="grow overflow-hidden">
      <div class="flex flex-col min-h-screen overflow-hidden supports-[overflow:clip]:overflow-clip">
        <Header />

        <div class="w-full max-w-[1072px] mx-auto grow md:flex space-y-8 md:space-y-0 md:space-x-8 pb-16 pt-20 md:pb-20 md:pt-28">
          <div class="grow px-6 md:min-w-[700px]">
            <div class="max-w-[700px]">
              <section>
                <h1 class="h1 font-aspekta mb-5">关于 <span class="inline-flex relative text-sky-500 before:absolute before:inset-0 before:bg-sky-200 dark:before:bg-sky-500 before:opacity-30 before:-z-10 before:-rotate-2 before:translate-y-1/4">{{ aboutConfig.titleHighlight }}</span></h1>

                <div class="text-slate-500 dark:text-slate-400 space-y-8">
                  <div v-for="section in aboutConfig.sections" :key="section.title" class="space-y-4">
                    <h2 class="h3 font-aspekta text-slate-800 dark:text-slate-100">{{ section.title }}</h2>
                    <p v-for="text in section.paragraphs" :key="text">{{ text }}</p>
                  </div>

                  <div class="space-y-4">
                    <h2 class="h3 font-aspekta text-slate-800 dark:text-slate-100">{{ aboutConfig.timelineTitle }}</h2>
                    <ul class="-my-2">
                      <li v-for="item in aboutConfig.timeline" :key="`${item.time}-${item.title}`" class="relative py-2">
                        <div class="flex items-start mb-1">
                          <div class="absolute left-0 h-full w-px bg-slate-200 dark:bg-slate-800 self-start ml-[28px] -translate-x-1/2 translate-y-3" aria-hidden="true"></div>
                          <div class="absolute left-0 h-14 w-14 flex items-center justify-center border border-slate-200 dark:border-slate-800 dark:bg-gradient-to-t dark:from-slate-800 dark:to-slate-800/30 bg-white dark:bg-slate-900 rounded-full">
                            <svg xmlns="http://www.w3.org/2000/svg" width="17" height="17">
                              <path fill="#6366F1" d="M2.486 5.549C3.974 7.044 5.953 7.89 8.009 8.045c-.138-2.065-.997-4.053-2.486-5.548C4.035 1.002 2.117.154 0 0c.138 2.065.997 4.053 2.486 5.549Zm12.028 0c-1.488 1.495-3.467 2.342-5.523 2.496.138-2.065.997-4.053 2.486-5.548C12.888 1.002 14.883.154 17 0c-.153 2.065-.997 4.053-2.486 5.549Zm0 5.902c-1.488-1.495-3.467-2.342-5.523-2.496.138 2.065.997 4.053 2.486 5.548C12.965 15.998 14.944 16.846 17 17c-.153-2.127-.997-4.13-2.486-5.549Zm-12.028 0c1.488-1.495 3.467-2.342 5.6-2.496-.138 2.065-.998 4.053-2.486 5.548C4.035 15.998 2.117 16.861 0 17c.138-2.127.997-4.13 2.486-5.549Z"></path>
                            </svg>
                          </div>
                          <div class="pl-20 space-y-1">
                            <div class="text-xs text-slate-500 uppercase">{{ item.time }}</div>
                            <div class="font-aspekta font-[650] text-slate-800 dark:text-slate-100">{{ item.title }}</div>
                            <div class="text-sm font-medium text-slate-800 dark:text-slate-100">{{ item.subtitle }}</div>
                            <div class="text-sm text-slate-500 dark:text-slate-400">{{ item.description }}</div>
                          </div>
                        </div>
                      </li>
                    </ul>
                  </div>

                  <p v-if="globalConfig.showSponsorPage">如果您认可我们的项目，也欢迎打赏赞助：
                    <router-link to="/sponsor" class="font-medium text-sm cursor-pointer">打赏赞助</router-link>
                  </p>
                </div>
              </section>
            </div>
          </div>

          <aside class="md:w-[240px] lg:w-[300px] shrink-0 px-6">
            <div class="space-y-6">
              <WidgetAds />
              <WidgetLinks />
            </div>
          </aside>
        </div>

        <Footer />
      </div>
    </main>
  </div>
</template>

<script>
import { inject } from 'vue'
import Header from '../partials/Header.vue'
import WidgetAds from '../partials/WidgetAds.vue'
import WidgetLinks from '../partials/WidgetLinks.vue'
import Footer from '../partials/Footer.vue'
import { useHead } from '@vueuse/head'
import aboutConfig from '../config/about.config'

export default {
  name: 'About',
  components: { Header, WidgetAds, WidgetLinks, Footer },
  setup() {
    const globalConfig = inject('globalConfig')
    useHead({
      title: '关于我们',
      titleTemplate: '%s | ' + globalConfig.siteTitle,
      meta: [
        { name: 'description', content: globalConfig.siteDescript },
        { name: 'keywords', content: globalConfig.siteKeywords }
      ]
    })

    return {
      globalConfig,
      aboutConfig
    }
  }
}
</script>
