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

              <div class="space-y-10">

                <section>
                  <!-- Page title -->
                  <h1 class="h1 font-aspekta mb-5">漏洞情报订阅</h1>
                  <!-- Page content -->
                  <div class="text-slate-500 dark:text-slate-400 space-y-8">
                    <!--<p class="text-lg">敬请期待！</p>-->
                    <p class="text-lg">欢迎订阅，我们提供免费的API及相关订阅功能，但为保证各情报源平台商业利益，不允许用于商业用途，仅允许用于个人安全研究或企业安全建设用途。</p>
                    <p>API及订阅功能注册登录即可使用，个人可免费使用，企业用户请购买企业版或赞助广告(用于支出服务器等成本，全凭自觉，感谢支持)；如有特殊需求，请联系站长。</p>
                    <p>购买/联系方式：<a class="font-medium text-sky-500 hover:underline" href="mailto:f00y1n9@gmail.com">f00y1n9#gmail.com</a>(邮箱) fooying(微信)</p>
                    <div>
                      <div class="mx-auto max-w-7xl px-6 lg:px-8">
                        <!-- xs to lg -->
                        <div class="mx-auto mt-12 max-w-md space-y-8 sm:mt-16 lg:hidden">
                          <section v-for="tier in tiers" :key="tier.id" :class="[tier.mostPopular ? 'rounded-xl bg-gray-400/5 ring-1 ring-inset ring-gray-200' : '', 'p-8']">
                            <h3 :id="tier.id" class="text-sm font-semibold leading-6 text-slate-500 dark:text-slate-400">{{ tier.name }}</h3>
                            <p class="mt-2 flex items-baseline gap-x-1 text-slate-500 dark:text-slate-400">
                              <div v-if="typeof tier.priceMonthly === 'string'" class="flex items-baseline gap-x-1 text-slate-500 dark:text-slate-400">
                                <span class="text-4xl font-bold">{{ tier.priceMonthly }}</span>
                                <span class="text-sm font-semibold">/月</span>
                              </div>
                              <div v-else class="items-baseline gap-x-1 text-slate-500 dark:text-slate-400">
                                <div v-for="price in tier.priceMonthly">
                                  <span class="text-2xl font-bold">{{ price.price }}</span>
                                  <span class="text-sm font-semibold">/月({{ price.name }})</span>
                                </div>
                              </div>
                            </p>
                            <ul role="list" class="mt-10 space-y-4 text-sm leading-6 text-slate-500 dark:text-slate-400">
                              <li v-for="section in sections" :key="section.name">
                                <ul role="list" class="space-y-4">
                                  <template v-for="feature in section.features" :key="feature.name">
                                    <li v-if="feature.tiers[tier.name]" class="flex gap-x-3">
                                      <CheckIcon class="h-6 w-5 flex-none text-sky-600" aria-hidden="true" />
                                      <span>
                                        {{ feature.name }}
                                        {{ ' ' }}
                                        <span v-if="typeof feature.tiers[tier.name] === 'string'" class="text-sm leading-6 text-gray-500">({{ feature.tiers[tier.name] }})</span>
                                      </span>
                                    </li>
                                  </template>
                                </ul>
                              </li>
                            </ul>
                          </section>
                        </div>

                        <!-- lg+ -->
                        <div class="isolate mt-10 hidden lg:block">
                          <div class="relative -mx-8">
                            <div v-if="tiers.some((tier) => tier.mostPopular)" class="absolute inset-x-3 inset-y-0 -z-10 flex">
                              <div class="flex w-1/3 px-4" aria-hidden="true" :style="{ marginLeft: `${(tiers.findIndex((tier) => tier.mostPopular) + 1) * 100/3}%` }">
                                <div class="w-full rounded-t-xl border-x border-t border-slate-200 dark:border-slate-800 bg-gray-400/5" />
                              </div>
                            </div>
                            <table class="w-full table-fixed border-separate border-spacing-x-8 text-left">
                              <caption class="sr-only">
                                Pricing plan comparison
                              </caption>
                              <colgroup>
                                <col class="w-1/3" />
                                <col class="w-1/3" />
                                <col class="w-1/3" />
                              </colgroup>
                              <thead>
                                <tr>
                                  <td />
                                  <th v-for="tier in tiers" :key="tier.id" scope="col" class="px-6 pt-6 xl:px-8 xl:pt-8">
                                    <div class="text-sm font-semibold leading-7 text-slate-500 dark:text-slate-400">{{ tier.name }}</div>
                                  </th>
                                </tr>
                              </thead>
                              <tbody>
                                <tr>
                                  <th scope="row"><span class="sr-only">Price</span></th>
                                  <td v-for="tier in tiers" :key="tier.id" class="px-6 pt-2">
                                    <div v-if="typeof tier.priceMonthly === 'string'" class="flex items-baseline gap-x-1 text-slate-500 dark:text-slate-400">
                                      <span class="text-4xl font-bold">{{ tier.priceMonthly }}</span>
                                      <span class="text-sm font-semibold leading-6">/月</span>
                                    </div>
                                    <div v-else class="items-baseline gap-x-1 text-slate-500 dark:text-slate-400">
                                      <div v-for="price in tier.priceMonthly">
                                        <span class="text-2xl font-bold">{{ price.price }}</span>
                                        <span class="text-sm font-semibold leading-6">/月({{ price.name }})</span>
                                      </div>
                                    </div>
                                  </td>
                                </tr>
                                <template v-for="(section, sectionIdx) in sections" :key="section.name">
                                  <tr>
                                    <th scope="colgroup" colspan="3" :class="[sectionIdx === 0 ? 'pt-8' : 'pt-16', 'pb-4 text-sm font-semibold leading-6 text-slate-500 dark:text-slate-400']">
                                      {{ section.name }}
                                      <div class="absolute inset-x-8 mt-4 h-px bg-gray-900/10 dark:bg-slate-600" />
                                    </th>
                                  </tr>
                                  <tr v-for="feature in section.features" :key="feature.name">
                                    <th scope="row" class="py-4 text-sm font-normal leading-6 text-slate-500 dark:text-slate-400">
                                      {{ feature.name }}
                                      <div class="absolute inset-x-8 mt-4 h-px bg-gray-900/5 dark:bg-slate-800" />
                                    </th>
                                    <td v-for="tier in tiers" :key="tier.id" class="px-6 py-4 xl:px-8">
                                      <div v-if="typeof feature.tiers[tier.name] === 'string'" class="text-center text-sm leading-6 text-gray-500">{{ feature.tiers[tier.name] }}</div>
                                      <template v-else>
                                        <CheckIcon v-if="feature.tiers[tier.name] === true" class="mx-auto h-5 w-5 text-sky-600 dark:text-slate-400" aria-hidden="true" />
                                        <MinusIcon v-else class="mx-auto h-5 w-5 text-gray-400" aria-hidden="true" />
                                        <span class="sr-only">{{ feature.tiers[tier.name] === true ? 'Included' : 'Not included' }} in {{ tier.name }}</span>
                                      </template>
                                    </td>
                                  </tr>
                                </template>
                              </tbody>
                            </table>
                          </div>
                        </div>
                      </div>
                    </div>
                    <p>漏洞情报爬取源详见：
                      <router-link class="" to="/spider" v-slot="{ href, navigate, isExactActive }" >
                        <a class="font-medium text-sm cursor-pointer" :href="href">《情报源及爬虫说明》</a>
                      </router-link>
                    </p>
                  </div>
                </section>

              </div>

            </div>
          </div>

          <!-- Right sidebar -->
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
import { inject } from 'vue';

import SideNavigation from '../partials/SideNavigation.vue'
import Header from '../partials/Header.vue'
import WidgetSponsor from '../partials/WidgetSponsor.vue'
import WidgetAds from '../partials/WidgetAds.vue'
import Footer from '../partials/Footer.vue'
import { useHead } from '@vueuse/head'
import { CheckIcon, MinusIcon } from '@heroicons/vue/20/solid'

export default {
  name: 'Subscribe',
  components: {
    SideNavigation,
    Header,
    WidgetSponsor,
    WidgetAds,
    Footer,
    CheckIcon,
    MinusIcon
  },
  setup() {
    const globalConfig = inject('globalConfig');
    const pageKeywords = '';
    useHead({
      title: '漏洞情报订阅',
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

    const tiers = [
      {
        name: '个人',
        id: 'free',
        href: '#',
        priceMonthly: '¥0',
        description: '免费订阅，注册用户即可使用',
        mostPopular: false,
      },
      {
        name: '企业',
        id: 'vip',
        href: '#',
        priceMonthly: '¥2000',
        description: 'VIP订阅，付费开通',
        mostPopular: true,
      }
    ]
    const sections = [
      {
        name: '功能特性',
        features: [
          { name: '情报合并去重', tiers: { 个人: true, 企业: true } },
          { name: '更新周期', tiers: { 个人: '每小时', 企业: '每小时' } },
          { name: '返回条数', tiers: { 个人: '最多20条', 企业: '最多50条' } },
          { name: '基于组件筛选', tiers: { 个人: false, 企业: true } },
          { name: '发布时间筛选', tiers: { 个人: false, 企业: true } },
          { name: '标题关键字筛选', tiers: { 个人: false, 企业: true } },
        ],
      },
      {
        name: '接口调用',
        features: [
          { name: '次数限制', tiers: { 个人: '30/天', 企业: '无限制' } },
          { name: 'Webhook推送', tiers: { 个人: true, 企业: true } },
        ],
      },
      {
        name: '支持字段',
        features: [
          { name: '编号', tiers: { 个人: true, 企业: true } },
          { name: '标题', tiers: { 个人: true, 企业: true } },
          { name: '发布时间', tiers: { 个人: true, 企业: true } },
          { name: 'url', tiers: { 个人: true, 企业: true } },
          { name: 'CVE编号', tiers: { 个人: true, 企业: true } },
          { name: '漏洞描述', tiers: { 个人: true, 企业: true } },
          { name: '重复漏洞(其他来源)', tiers: { 个人:true, 企业: true } },
          { name: 'CNNVD编号', tiers: { 个人: false, 企业: true } },
          { name: 'CNVD编号', tiers: { 个人: false, 企业: true } },
          { name: '影响组件', tiers: { 个人: false, 企业: true } },
          { name: '风险类型', tiers: { 个人: false, 企业: true } },
          { name: '利用状态', tiers: { 个人: false, 企业: true } },
          { name: 'CVSS3.0', tiers: { 个人: false, 企业: true } },
          { name: '漏洞级别', tiers: { 个人: false, 企业: true } },
          { name: '补丁情况', tiers: { 个人: false, 企业: true } },
          { name: '参考链接', tiers: { 个人: false, 企业: true } },
          { name: '漏洞标签', tiers: { 个人: false, 企业: true } },
          { name: '更新时间', tiers: { 个人: false, 企业: true } },
        ],
      }
    ]
    return {
      tiers,
      sections
    }
  }
}
</script>
