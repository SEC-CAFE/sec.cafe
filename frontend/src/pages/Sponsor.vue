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
                  <h1 class="h1 font-aspekta mb-5">打赏赞助</h1>
                  <!-- Page content -->
                  <div class="text-slate-500 dark:text-slate-400 space-y-8">
                    <div class="space-y-4">
                      <p>
                        如果你有想法，欢迎提出你的建议或参与到这个项目。
                      </p>
                      <p>
                        你也可以选择打赏该项目(直接扫描打赏)，帮助该项目持续运营下去；或者成为我们的赞助商，我们将在首页右侧挂上您的Logo。
                      </p>
                      <p>联系方式：<a class="font-medium text-sky-500 hover:underline" href="mailto:f00y1n9@gmail.com">f00y1n9#gmail.com</a>(邮箱) fooying(微信)</p>
                      <p>微信群请添加微信[_ffff01]为好友邀请进群！</p>
                      <p></p>
                      <h2>打赏赞助</h2>
                      <img :class="isHover!=1&&isHover!=-1 ? 'blur-[2px]' : ''"  qrcode_id=1 :ref="getDom" class="inline-flex rounded-lg mr-4" src="../images/wechatpay.jpg" width="100" />
                      <img :class="isHover!=2&&isHover!=-1 ? 'blur-[2px]' : ''"  qrcode_id=2 :ref="getDom" class="inline-flex rounded-lg" src="../images/alipay.jpg" width="100" />
                      <a class="ml-1" href="https://www.patreon.com/user?u=93897763" target="_blank"><img src="../images/patreon.png" width="210" /></a>
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
                              <tr v-for="person in sponsors" :key="person.name" class="text-slate-500 dark:text-slate-400">
                                <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500 sm:pl-0">{{ person.time }}</td>
                                <td class="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900 ">{{ person.name }}</td>
                                <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{{ person.price }}</td>
                                <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{{ person.comment }}</td>
                              </tr>
                            </tbody>
                          </table>
                        </div>
                      </div>
                    </div>
                    <p>感谢您的认可与支持！ </p>
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
import { ref, inject} from 'vue'
import SideNavigation from '../partials/SideNavigation.vue'
import Header from '../partials/Header.vue'
import WidgetSponsor from '../partials/WidgetSponsor.vue'
import WidgetAds from '../partials/WidgetAds.vue'
import Footer from '../partials/Footer.vue'
import { useHead } from '@vueuse/head'
import { CheckIcon, MinusIcon } from '@heroicons/vue/20/solid'

export default {
  name: 'Sponsor',
  components: {
    SideNavigation,
    Header,
    WidgetSponsor,
    WidgetAds,
    Footer,
    CheckIcon,
    MinusIcon
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
      title: '打赏赞助',
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

    const sponsors = [
    {
        name: "O*t",
        price: 188.88,
        comment: "赞助商要求：把赞助商的名字挂在上面(要挂什么名字请联系我哈，用打赏账号加我微信fooying)",
        time: "2024-11-15"
      },
      {
        name: "*夏",
        price: 66,
        comment: "",
        time: "2024-09-24"
      },
      {
        name: "l*g",
        price: 5,
        comment: "",
        time: "2024-09-23"
      },
      {
        name: "H*y",
        price: 9.9,
        comment: "奖励一杯瑞幸咖啡☕️",
        time: "2024-06-13"
      },
      {
        name: "fs12",
        price: 5,
        comment: "",
        time: "2024-06-04"
      },
      {
        name: "xidd",
        price: 50,
        comment: "ai知识库不错",
        time: "2024-05-12"
      },
      {
        name: "匿名",
        price: 20,
        comment: "",
        time: "2023-05-01"
      },
      {
        name: "w",
        price: 100,
        comment: "不错的项目",
        time: "2023-04-28"
      }
    ]

    return {
      sponsors,
      qrCodes,
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
  }
}
</script>
