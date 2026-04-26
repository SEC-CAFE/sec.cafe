<template>
  <div class="min-h-screen flex">
    <main class="grow overflow-hidden">
      <div class="flex flex-col min-h-screen overflow-hidden supports-[overflow:clip]:overflow-clip">
        <Header />

        <div class="w-full max-w-[1072px] mx-auto grow md:flex space-y-8 md:space-y-0 md:space-x-8 pb-16 pt-20 md:pb-20 md:pt-28">
          <div class="grow px-6 md:min-w-[700px]">
            <div class="max-w-[700px]">
              <div class="space-y-10">
                <section>
                  <h1 class="h1 font-aspekta mb-5">打赏赞助</h1>

                  <div v-if="!globalConfig.showSponsorPage" class="text-slate-500 dark:text-slate-400 space-y-4">
                    <p>该页面当前未开放。</p>
                  </div>

                  <div v-else class="text-slate-500 dark:text-slate-400 space-y-8">
                    <div class="space-y-4">
                      <p v-for="text in sponsorConfig.intro" :key="text">{{ text }}</p>
                      <p>联系方式：<a class="font-medium text-sky-500 hover:underline" :href="`mailto:${globalConfig.contactEmail}`">{{ globalConfig.contactEmail }}</a>(邮箱) {{ globalConfig.contactWechat }}(微信)</p>
                      <p>{{ globalConfig.contactGroupHint }}</p>
                      <h2>打赏赞助</h2>
                      <img
                        v-for="qrcode in sponsorConfig.qrcodes"
                        :key="qrcode.id"
                        :class="isHover != qrcode.id && isHover != -1 ? 'blur-[2px]' : ''"
                        :qrcode_id="qrcode.id"
                        :ref="getDom"
                        class="inline-flex rounded-lg mr-4"
                        :src="qrcode.src"
                        :width="qrcode.width"
                        :alt="qrcode.label"
                      />
                      <a class="ml-1" :href="sponsorConfig.patreonUrl" target="_blank"><img src="../images/patreon.png" width="210" /></a>
                    </div>

                    <div class="mt-8 flow-root">
                      <h2 class="h3 font-aspekta text-slate-800 dark:text-slate-100">打赏赞助列表</h2>
                      <div class="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
                        <div class="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
                          <table class="min-w-full divide-y divide-slate-300 dark:divide-gray-700">
                            <thead>
                              <tr class="text-slate-500 dark:text-slate-400">
                                <th scope="col" class="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-0">时间</th>
                                <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">昵称</th>
                                <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">金额</th>
                                <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">备注</th>
                              </tr>
                            </thead>
                            <tbody class="divide-y dark:divide-gray-800 divide-slate-200">
                              <tr v-for="person in sponsorConfig.sponsors" :key="`${person.time}-${person.name}`" class="text-slate-500 dark:text-slate-400">
                                <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500 sm:pl-0">{{ person.time }}</td>
                                <td class="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900">{{ person.name }}</td>
                                <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{{ person.price }}</td>
                                <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{{ person.comment }}</td>
                              </tr>
                            </tbody>
                          </table>
                        </div>
                      </div>
                    </div>
                    <p>感谢您的认可与支持！</p>
                  </div>
                </section>
              </div>
            </div>
          </div>

          <aside class="md:w-[240px] lg:w-[300px] shrink-0 px-6">
            <div class="space-y-6">
              <WidgetSponsor />
              <WidgetAds />
            </div>
          </aside>
        </div>

        <Footer />
      </div>
    </main>
  </div>
</template>

<script>
import { ref, inject } from 'vue'
import Header from '../partials/Header.vue'
import WidgetSponsor from '../partials/WidgetSponsor.vue'
import WidgetAds from '../partials/WidgetAds.vue'
import Footer from '../partials/Footer.vue'
import { useHead } from '@vueuse/head'
import sponsorConfig from '../config/sponsor.config'

export default {
  name: 'Sponsor',
  components: { Header, WidgetSponsor, WidgetAds, Footer },
  data() {
    return { isHover: -1 }
  },
  setup() {
    const globalConfig = inject('globalConfig')
    useHead({
      title: '打赏赞助',
      titleTemplate: '%s | ' + globalConfig.siteTitle,
      meta: [
        { name: 'description', content: globalConfig.siteDescript },
        { name: 'keywords', content: globalConfig.siteKeywords }
      ]
    })
    const qrCodes = ref([])
    function getDom(el) {
      if (el) qrCodes.value.push(el)
    }

    return {
      globalConfig,
      sponsorConfig,
      qrCodes,
      getDom
    }
  },
  methods: {
    handleMouseover(e) {
      this.isHover = -1
      for (const key in this.qrCodes) {
        const element = this.qrCodes[key]
        if (element.isEqualNode(e.target)) {
          this.isHover = Number(e.target.getAttribute('qrcode_id'))
        }
      }
    }
  },
  mounted() {
    document.addEventListener('mouseover', this.handleMouseover)
  },
  beforeUnmount() {
    document.removeEventListener('mouseover', this.handleMouseover)
  }
}
</script>
