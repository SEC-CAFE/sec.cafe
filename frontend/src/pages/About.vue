<template>
  <div class="min-h-screen flex">

    <!-- Main content -->
    <main class="grow overflow-hidden">
      <div class="flex flex-col min-h-screen overflow-hidden supports-[overflow:clip]:overflow-clip">

        <Header />

        <!-- Content -->
        <div class="w-full max-w-[1072px] mx-auto grow md:flex space-y-8 md:space-y-0 md:space-x-8 pb-16 pt-20 md:pb-20 md:pt-28">

          <!-- Middle area -->
          <div class="grow px-6 md:min-w-[700px]">
            <div class="max-w-[700px]">

              <section>
                <!-- Page title -->
                <h1 class="h1 font-aspekta mb-5">关于 <span class="inline-flex relative text-sky-500 before:absolute before:inset-0 before:bg-sky-200 dark:before:bg-sky-500 before:opacity-30 before:-z-10 before:-rotate-2 before:translate-y-1/4">SEC.CAFE 安全咖啡</span></h1>
                <!-- Page content -->
                <div class="text-slate-500 dark:text-slate-400 space-y-8">
                  <div class="space-y-4">
                    <h2 class="h3 font-aspekta text-slate-800 dark:text-slate-100">初衷</h2>
                    <p>
                      一直都比较有想法，但也一直停留在自己的笔记里，所以希望通过SEC.CAFE实现自己的一些想法，把一些好玩好用的安全项目逐步上线，让它成为一个可以被大家真的使用起来的安全社区！
                    </p>
                  </div>
                  <div class="space-y-4">
                    <h2 class="h3 font-aspekta text-slate-800 dark:text-slate-100">为什么取名SEC.CAFE</h2>
                    <p>
                      一方面是自己手上正好有这样一个域名(还有sec.style/guide，大家有好想法也可以告诉我)。
                    </p>
                    <p>
                      另一方面觉得做安全真的比较累，比较卷，希望大家能坐下来休息下，喝一杯咖啡，让安全重新成为最初的兴趣，回归每一次突破的乐趣。
                    </p>
                  </div>
                  <div class="space-y-4">
                    <h2 class="h3 font-aspekta text-slate-800 dark:text-slate-100">更新日志</h2>
                    <ul class="-my-2">
                      <!-- Role -->
                      <li class="relative py-2">
                        <div class="flex items-start mb-1">
                          <div class="absolute left-0 h-full w-px bg-slate-200 dark:bg-slate-800 self-start ml-[28px] -translate-x-1/2 translate-y-3" aria-hidden="true"></div>
                          <div class="absolute left-0 h-14 w-14 flex items-center justify-center border border-slate-200 dark:border-slate-800 dark:bg-gradient-to-t dark:from-slate-800 dark:to-slate-800/30 bg-white dark:bg-slate-900 rounded-full">
                            <svg xmlns="http://www.w3.org/2000/svg" width="17" height="17">
                              <path fill="#6366F1" d="M2.486 5.549C3.974 7.044 5.953 7.89 8.009 8.045c-.138-2.065-.997-4.053-2.486-5.548C4.035 1.002 2.117.154 0 0c.138 2.065.997 4.053 2.486 5.549Zm12.028 0c-1.488 1.495-3.467 2.342-5.523 2.496.138-2.065.997-4.053 2.486-5.548C12.888 1.002 14.883.154 17 0c-.153 2.065-.997 4.053-2.486 5.549Zm0 5.902c-1.488-1.495-3.467-2.342-5.523-2.496.138 2.065.997 4.053 2.486 5.548C12.965 15.998 14.944 16.846 17 17c-.153-2.127-.997-4.13-2.486-5.549Zm-12.028 0c1.488-1.495 3.467-2.342 5.6-2.496-.138 2.065-.998 4.053-2.486 5.548C4.035 15.998 2.117 16.861 0 17c.138-2.127.997-4.13 2.486-5.549Z"></path>
                            </svg>
                          </div>
                          <div class="pl-20 space-y-1">
                            <div class="text-xs text-slate-500 uppercase">2023年5月</div>
                            <div class="font-aspekta font-[650] text-slate-800 dark:text-slate-100">漏洞情报</div>
                            <div class="text-sm font-medium text-slate-800 dark:text-slate-100">
                              多源聚合去重
                              <span class="text-slate-400 dark:text-slate-600">·</span>
                              快速监测
                              <span class="text-slate-400 dark:text-slate-600">·</span>
                              免费订阅
                            </div>
                            <div class="text-sm text-slate-500 dark:text-slate-400">从业这么多年，无论是在乙方安全公司安全研究，还是后来负责甲方做企业安全，漏洞情报一直都是个基础安全设施，所以选择作为第一个项目。</div>
                          </div>
                        </div>
                      </li>
                      <li class="relative py-2">
                        <div class="flex items-start mb-1">
                          <div class="absolute left-0 h-full w-px bg-slate-200 dark:bg-slate-800 self-start ml-[28px] -translate-x-1/2 translate-y-3" aria-hidden="true"></div>
                          <div class="absolute left-0 h-14 w-14 flex items-center justify-center border border-slate-200 dark:border-slate-800 dark:bg-gradient-to-t dark:from-slate-800 dark:to-slate-800/30 bg-white dark:bg-slate-900 rounded-full">
                            <svg xmlns="http://www.w3.org/2000/svg" width="17" height="17">
                              <path fill="#6366F1" d="M2.486 5.549C3.974 7.044 5.953 7.89 8.009 8.045c-.138-2.065-.997-4.053-2.486-5.548C4.035 1.002 2.117.154 0 0c.138 2.065.997 4.053 2.486 5.549Zm12.028 0c-1.488 1.495-3.467 2.342-5.523 2.496.138-2.065.997-4.053 2.486-5.548C12.888 1.002 14.883.154 17 0c-.153 2.065-.997 4.053-2.486 5.549Zm0 5.902c-1.488-1.495-3.467-2.342-5.523-2.496.138 2.065.997 4.053 2.486 5.548C12.965 15.998 14.944 16.846 17 17c-.153-2.127-.997-4.13-2.486-5.549Zm-12.028 0c1.488-1.495 3.467-2.342 5.6-2.496-.138 2.065-.998 4.053-2.486 5.548C4.035 15.998 2.117 16.861 0 17c.138-2.127.997-4.13 2.486-5.549Z"></path>
                            </svg>
                          </div>
                          <div class="pl-20 space-y-1">
                            <div class="text-xs text-slate-500 uppercase">2023年12月</div>
                            <div class="font-aspekta font-[650] text-slate-800 dark:text-slate-100">安全手册</div>
                            <div class="text-sm font-medium text-slate-800 dark:text-slate-100">企业安全实践、攻防与安全研究知识库</div>
                            <div class="text-sm text-slate-500 dark:text-slate-400">我们力争给安全从业者提供最完整、最准确的安全知识参考内容。 知识库内容主要是来自互联网及大家的贡献，也欢迎每一位使用安全手册的同行贡献你的一份力量。</div>
                          </div>
                        </div>
                      </li>
                      <li class="relative py-2">
                        <div class="flex items-start mb-1">
                          <div class="absolute left-0 h-full w-px bg-slate-200 dark:bg-slate-800 self-start ml-[28px] -translate-x-1/2 translate-y-3" aria-hidden="true"></div>
                          <div class="absolute left-0 h-14 w-14 flex items-center justify-center border border-slate-200 dark:border-slate-800 dark:bg-gradient-to-t dark:from-slate-800 dark:to-slate-800/30 bg-white dark:bg-slate-900 rounded-full">
                            <svg xmlns="http://www.w3.org/2000/svg" width="17" height="17">
                              <path fill="#6366F1" d="M2.486 5.549C3.974 7.044 5.953 7.89 8.009 8.045c-.138-2.065-.997-4.053-2.486-5.548C4.035 1.002 2.117.154 0 0c.138 2.065.997 4.053 2.486 5.549Zm12.028 0c-1.488 1.495-3.467 2.342-5.523 2.496.138-2.065.997-4.053 2.486-5.548C12.888 1.002 14.883.154 17 0c-.153 2.065-.997 4.053-2.486 5.549Zm0 5.902c-1.488-1.495-3.467-2.342-5.523-2.496.138 2.065.997 4.053 2.486 5.548C12.965 15.998 14.944 16.846 17 17c-.153-2.127-.997-4.13-2.486-5.549Zm-12.028 0c1.488-1.495 3.467-2.342 5.6-2.496-.138 2.065-.998 4.053-2.486 5.548C4.035 15.998 2.117 16.861 0 17c.138-2.127.997-4.13 2.486-5.549Z"></path>
                            </svg>
                          </div>
                          <div class="pl-20 space-y-1">
                            <div class="text-xs text-slate-500 uppercase">2024年9月</div>
                            <div class="font-aspekta font-[650] text-slate-800 dark:text-slate-100">SECSOSO 安全搜索</div>
                            <div class="text-sm font-medium text-slate-800 dark:text-slate-100">一个AI驱动的网络安全内容聚合搜索引擎</div>
                            <div class="text-sm text-slate-500 dark:text-slate-400">安全搜搜，搜索安全，AI驱动的网络安全内容聚合搜索！一个AI驱动的网络安全内容聚合搜索引擎，它基于互联网元搜索引擎、安全知识库、大模型、RAG等技术构建，专门为网络安全垂直行业提供服务。secsoso.com</div>
                          </div>
                        </div>
                      </li>
                      <!-- Role -->
                      <li class="relative py-2">
                        <div class="flex items-start mb-1">
                          <div class="absolute left-0 h-full w-px bg-slate-200 dark:bg-slate-800 self-start ml-[28px] -translate-x-1/2 translate-y-3" aria-hidden="true"></div>
                          <div class="absolute left-0 h-14 w-14 flex items-center justify-center border border-slate-200 dark:border-slate-800 dark:bg-gradient-to-t dark:from-slate-800 dark:to-slate-800/30 bg-white dark:bg-slate-900 rounded-full">
                            <svg xmlns="http://www.w3.org/2000/svg" width="17" height="17">
                              <path fill="#6366F1" d="M2.486 5.549C3.974 7.044 5.953 7.89 8.009 8.045c-.138-2.065-.997-4.053-2.486-5.548C4.035 1.002 2.117.154 0 0c.138 2.065.997 4.053 2.486 5.549Zm12.028 0c-1.488 1.495-3.467 2.342-5.523 2.496.138-2.065.997-4.053 2.486-5.548C12.888 1.002 14.883.154 17 0c-.153 2.065-.997 4.053-2.486 5.549Zm0 5.902c-1.488-1.495-3.467-2.342-5.523-2.496.138 2.065.997 4.053 2.486 5.548C12.965 15.998 14.944 16.846 17 17c-.153-2.127-.997-4.13-2.486-5.549Zm-12.028 0c1.488-1.495 3.467-2.342 5.6-2.496-.138 2.065-.998 4.053-2.486 5.548C4.035 15.998 2.117 16.861 0 17c.138-2.127.997-4.13 2.486-5.549Z"></path>
                            </svg>
                          </div>
                          <div class="pl-20 space-y-1">
                            <div class="text-xs text-slate-500 uppercase">2024</div>
                            <div class="font-aspekta font-[650] text-slate-800 dark:text-slate-100">敬请期待</div>
                            <div class="text-sm font-medium text-slate-800 dark:text-slate-100">敬请期待</div>
                            <div class="text-sm text-slate-500 dark:text-slate-400">敬请期待</div>
                          </div>
                        </div>
                      </li>
                    </ul>
                  </div>
                  <p>如果您认可我们的项目，也欢迎打赏赞助：
                      <router-link class="" to="/sponsor" v-slot="{ href, navigate, isExactActive }" >
                        <a class="font-medium text-sm cursor-pointer" :href="href">打赏赞助</a>
                      </router-link>
                    </p>

                </div>
              </section>

            </div>
          </div>

          <!-- Right sidebar -->
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
import { inject } from 'vue';

import SideNavigation from '../partials/SideNavigation.vue'
import Header from '../partials/Header.vue'
import WidgetSponsor from '../partials/WidgetSponsor.vue'
import WidgetAds from '../partials/WidgetAds.vue'
import WidgetLinks from '../partials/WidgetLinks.vue'
import Footer from '../partials/Footer.vue'
import { useHead } from '@vueuse/head'

export default {
  name: 'About',
  components: {
    SideNavigation,
    Header,
    WidgetSponsor,
    WidgetAds,
    WidgetLinks,
    Footer,
  },
  setup() {
    const globalConfig = inject('globalConfig');
    const pageKeywords = '';
    useHead({
      title: '关于我们',
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

  }
}

</script>
