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
                <h1 class="h1 font-aspekta mb-5">情报源及爬虫说明</h1>
                <!-- Page content -->
                <div class="text-slate-500 dark:text-slate-400 space-y-8">
                  <div class="space-y-4">
                    <p>
                      SEC.CAFE 安全咖啡是一个安全爱好者的技术分享站点，提供免费的服务，提供最基本的安全信息聚合与服务，解决安全研究需求。
                    </p>
                    <p>
                      其中漏洞情报等服务依赖于爬虫，具体信息源可见下方列表；为保证各信息源平台商业利益，相关信息不允许用于商业用途，仅允许用于个人安全研究或企业安全建设用途；</p>
                    <p>为实现这一目的，我们做了以下几点努力：</p>
                    <ul class="list-disc list-inside space-y-2">
                        <li>限制访问频率，当前每小时爬取一次(正常最多请求不超过 20 次)；</li>
                        <li>爬虫仅爬取公开信息；</li>
                        <li>漏洞情报等相关信息聚合尽量减少非必要信息展示，详情引导跳转到源链接；</li>
                        <li>在相关页面标注内容，禁止用于商业用途。</li>
                    </ul>
                    <p>爬虫 UA 统一为<span class="text-slate-800 dark:text-slate-100 font-medium ">sec_cafe(https://sec.cafe/spider)</span>，如造成影响，请联系站长：<a class="hover:underline" href="mailto:f00y1n9@gmail.com">f00y1n9#gmail.com</a>(邮箱) fooying(微信)</p>
                  </div>

                  <div class="space-y-4">
                    <h2 class="h3 font-aspekta text-slate-800 dark:text-slate-100">漏洞情报源</h2>
                    <div class="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
                      <div class="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
                        <table class="min-w-full divide-y divide-slate-300 dark:divide-gray-700">
                          <thead>
                            <tr class="text-slate-500 dark:text-slate-400">
                              <th scope="col" class="py-3.5 pl-4 pr-3 text-left text-sm font-semibold sm:pl-0">情报源</th>
                              <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold">网址</th>
                              <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold">状态</th>
                            </tr>
                          </thead>
                          <tbody class="divide-y dark:divide-gray-800 divide-slate-200">
                            <tr v-for="s in vuli_sources" :key="s.name" class="text-slate-500 dark:text-slate-400">
                              <td class="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium sm:pl-0">{{ s.name }}</td>
                              <td class="whitespace-nowrap px-3 py-4 text-sm"><a :href="s.url">{{ s.url }}</a></td>
                              <td class="whitespace-nowrap px-3 py-4 text-sm">{{ s.status }}</td>
                            </tr>
                          </tbody>
                        </table>
                      </div>
                    </div>
                  </div>

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
import { ref, inject} from 'vue'

import SideNavigation from '../partials/SideNavigation.vue'
import Header from '../partials/Header.vue'
import WidgetSponsor from '../partials/WidgetSponsor.vue'
import WidgetAds from '../partials/WidgetAds.vue'
import WidgetLinks from '../partials/WidgetLinks.vue'
import Footer from '../partials/Footer.vue'
import { useHead } from '@vueuse/head'

export default {
  name: 'Spider',
  components: {
    SideNavigation,
    Header,
    WidgetSponsor,
    WidgetAds,
    WidgetLinks,
    Footer,
  },
  data() {
    return {
      isHover: -1,
    }
  },
  setup() {
    const globalConfig = inject('globalConfig');
    const pageKeywords = '';
    useHead({
      title: '情报源及爬虫说明',
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

    let qrCodes = ref([]);
    function getDom(el){
      if(el) {
        qrCodes.value.push(el);
      }
    }
    let vuli_sources = [
      { name: '阿里云漏洞库(AVD)', url: 'https://avd.aliyun.com', status: '在线' },
      { name: '360网络安全响应中心', url: 'https://cert.360.cn/warning', status: '在线' },
      { name: '腾讯云安全公告', url: 'https://cloud.tencent.com/announce/?categorys=21', priority: 2, status: '在线' },
      { name: '奇安信NOX漏洞库', url: 'https://nox.qianxin.com/KeyPoint', status: '下线' },
      { name: '绿盟威胁情报中心', url: 'https://nti.nsfocus.com/threatNotice', status: '在线' },
      { name: '深信服漏洞情报', url: 'https://sec.sangfor.com.cn/security-vulnerability', status: '在线' },
      { name: '用友安全中心', url: 'https://security.yonyou.com/#/noticeList', status: '下线' },
      { name: 'Seebug 漏洞平台', url: 'https://www.seebug.org', status: '在线' },
      { name: '安恒星图平台', url: 'https://ti.dbappsecurity.com.cn/vul', status: '在线' },
      { name: '奇安信威胁情报中心', url: 'https://ti.qianxin.com/', status: '在线' },
      { name: '长亭漏洞库', url: 'https://stack.chaitin.com/vuldb/index', status: '在线' },
      { name: 'OSCS开源安全情报', url: 'https://stack.chaitin.com/vuldb/index', status: '在线' },
      { name: '启明星辰安全通告', url: 'https://www.venustech.com.cn/new_type/aqtg/', status: '在线' },
      { name: '微步在线X情报社区', url: 'https://x.threatbook.com/v5/vul/notice', status: '在线' },
      { name: 'CISA KEV', url: 'https://www.cisa.gov/known-exploited-vulnerabilities-catalog', status: '在线' },
    ]
    return {
      qrCodes,
      vuli_sources,
      getDom
    }
  },
  methods: {
    handleMouseover(e){
      this.isHover = -1;
      for (const key in this.qrCodes) {
        var element = this.qrCodes[key];
        if (element.isEqualNode(e.target)){
          this.isHover = e.target.getAttribute('qrcode_id');
        }
      }
    }
  },
  mounted() {
    document.addEventListener('mouseover', this.handleMouseover)
  },
  beforeUnmount() {
    document.removeEventListener('mouseover', this.handleMouseover)
  },
}

</script>
