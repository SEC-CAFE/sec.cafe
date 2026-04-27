<template>
  <div class="min-h-screen flex">

    <!-- Main content -->
    <main class="grow overflow-hidden">
      <div class="flex flex-col min-h-screen overflow-hidden supports-[overflow:clip]:overflow-clip">

        <Header ref="header" />

        <!-- Content -->
        <div class="w-full max-w-[1072px] mx-auto grow md:flex space-y-8 md:space-y-0 md:space-x-8 pb-16 pt-20 md:pb-20 md:pt-28">
          <!-- <SideNavigation />-->
          <!-- Middle area -->
          <div class="grow px-6 md:min-w-[700px]">
            <div class="max-w-[700px]">

              <div class="space-y-10">

                <section>
                  <!-- Page title -->
                  <h1 class="h1 font-aspekta mb-5">漏洞情报订阅设置</h1>
                  <!-- Page content -->
                  <div class="text-slate-500 dark:text-slate-400 space-y-8">
                    <p class="text-lg">我们提供多种订阅方式，可根据您的场景自由选择：</p>
                    <ul class="space-y-4">
                      <li class="flex items-start">
                        <svg class="w-3 h-3 fill-current text-sky-500 mr-3 mt-1.5 shrink-0" viewBox="0 0 12 12" xmlns="http://www.w3.org/2000/svg">
                          <path d="M10.28 2.28L3.989 8.575 1.695 6.28A1 1 0 00.28 7.695l3 3a1 1 0 001.414 0l7-7A1 1 0 0010.28 2.28z"></path>
                        </svg>
                        <span>API主动请求：请访问 <a class="text-sky-500" href="https://api.sec.cafe/docs" target="_blank">API文档</a></span>
                      </li>
                      <li class="flex items-start">
                        <svg class="w-3 h-3 fill-current text-sky-500 mr-3 mt-1.5 shrink-0" viewBox="0 0 12 12" xmlns="http://www.w3.org/2000/svg">
                          <path d="M10.28 2.28L3.989 8.575 1.695 6.28A1 1 0 00.28 7.695l3 3a1 1 0 001.414 0l7-7A1 1 0 0010.28 2.28z"></path>
                        </svg>
                        <span>RSS订阅：请访问 <a class="text-sky-500" href="/feed/vuli" target="_blank">RSS源</a></span>
                      </li>
                      <li class="flex items-start">
                        <svg class="w-3 h-3 fill-current text-sky-500 mr-3 mt-1.5 shrink-0" viewBox="0 0 12 12" xmlns="http://www.w3.org/2000/svg">
                          <path d="M10.28 2.28L3.989 8.575 1.695 6.28A1 1 0 00.28 7.695l3 3a1 1 0 001.414 0l7-7A1 1 0 0010.28 2.28z"></path>
                        </svg>
                        <span>邮件推送：请于下方配置，同时请将发件人vul@mail.sec.cafe加入收件白名单</span>
                      </li>
                      <li class="flex items-start">
                        <svg class="w-3 h-3 fill-current text-sky-500 mr-3 mt-1.5 shrink-0" viewBox="0 0 12 12" xmlns="http://www.w3.org/2000/svg">
                          <path d="M10.28 2.28L3.989 8.575 1.695 6.28A1 1 0 00.28 7.695l3 3a1 1 0 001.414 0l7-7A1 1 0 0010.28 2.28z"></path>
                        </svg>
                        <span>Webhook推送：支持群机器人（企业微信、飞书、钉钉）、自定义WebHook，请于下方配置</span>
                      </li>
                    </ul>
                    <div>
                      <!-- Subscribe form -->
                      <div>
                        <div class="flex gap-5">
                          <div>
                            <label class="block text-sm font-medium mb-1" for="push_type">推送方式</label>
                            <select id="push_type" class="form-select" v-model="form.push_type" ref="push_type">
                              <option :key="item.value" v-for="item in options" :value="item.value" >{{ item.name }}</option>
                            </select>
                          </div>
                          <div>
                            <label class="block text-sm font-medium mb-1" for="hook_url">签名(可选)</label>
                            <div class="flex flex-col md:flex-row justify-center max-w-xs mx-auto md:max-w-md md:mx-0">
                              <input id="sign" type="text" class="form-input w-full mb-2 md:mb-0 md:mr-2" v-model="form.sign" ref="sign"/>
                            </div>
                          </div>
                          <div class="w-full">
                            <label class="block text-sm font-medium mb-1" for="hook_url">Webhook网址/邮箱地址</label>
                            <div class="flex flex-col md:flex-row justify-center max-w-xs mx-auto md:max-w-md md:mx-0">
                              <input id="hook_url" type="text" class="form-input w-full mb-2 md:mb-0 md:mr-2" v-model="form.hook_url" ref="hook_url"/>
                              <button class="btn text-white bg-sky-500 hover:bg-sky-600" @click="update_hook_url">更新/订阅</button>
                            </div>
                          </div>
                        </div>

                        <div class="mt-4 space-y-3">
                          <div class="flex items-end gap-3">
                            <div class="grow">
                              <label class="block text-sm font-medium mb-1" for="keyword_input">关键词过滤（可选）</label>
                              <input
                                id="keyword_input"
                                type="text"
                                class="form-input w-full"
                                v-model="keywordInput"
                                @keyup.enter="addKeyword"
                                placeholder="输入关键词后回车，例如：OpenSSH"
                              />
                            </div>
                            <button class="btn text-white bg-slate-600 hover:bg-slate-700" @click="addKeyword">添加</button>
                          </div>
                          <div class="flex flex-wrap gap-2" v-if="form.keywords.length">
                            <span v-for="(item, idx) in form.keywords" :key="`${item}-${idx}`" class="inline-flex items-center rounded-full bg-sky-100 text-sky-700 px-3 py-1 text-xs">
                              {{ item }}
                              <button class="ml-2 text-sky-600 hover:text-sky-800" @click="removeKeyword(idx)">×</button>
                            </span>
                          </div>
                          <div class="text-xs text-slate-500 dark:text-slate-400">
                            不配置关键词时，推送所有漏洞情报；配置后，命中任意关键词才会推送。
                          </div>
                          <div>
                            <label class="block text-sm font-medium mb-1" for="keyword_match_scope">关键词匹配范围</label>
                            <select id="keyword_match_scope" class="form-select w-full md:w-64" v-model="form.keyword_match_scope">
                              <option value="title">仅匹配标题</option>
                              <option value="title_desc">匹配标题和漏洞描述</option>
                            </select>
                          </div>
                        </div>
                        <!-- Success message -->
                        <!-- <p class="text-xs text-slate-500 mt-3 italic">Thanks for subscribing!</p> -->
                      </div>

                      <p class="mt-5 mb-5">注：推送样式及测试可点击<a class="text-sky-500" href="#" @click="check_hook_url">[测试发送]</a>进行在线测试。安全验证方式可选择签名或关键字"漏洞情报"。关键词过滤仅影响正式推送任务，不影响测试发送。</p>
                      <Banner2 v-if="setting_result.type" type="error" :open="banner2ErrorOpen">
                        {{ setting_result.msg }}
                      </Banner2>
                      <Banner2 v-else-if="setting_result" type="success" :open="banner2SuccessOpen">
                        {{ setting_result.msg }}
                      </Banner2>

                    </div>
                  </div>
                </section>


              </div>

            </div>
          </div>

          <!-- Right sidebar -->
          <aside class="md:w-[240px] lg:w-[300px] shrink-0">
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
import { mapGetters, mapActions } from 'vuex';

import SideNavigation from '../partials/SideNavigation.vue'
import Header from '../partials/Header.vue'
import WidgetSponsor from '../partials/WidgetSponsor.vue'
import WidgetAds from '../partials/WidgetAds.vue'
import Footer from '../partials/Footer.vue'
import { useHead } from '@vueuse/head'
import Banner2 from '../components/Banner2.vue'

export default {
  name: 'SettingsVuliPush',
  components: {
    SideNavigation,
    Header,
    WidgetSponsor,
    WidgetAds,
    Footer,
    Banner2
  },
  setup() {
    const banner2ErrorOpen = ref(true)
    const banner2SuccessOpen = ref(true)
    const globalConfig = inject('globalConfig');
    const pageKeywords = '';
    useHead({
      title: '漏洞情报订阅设置',
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
    return {
      banner2ErrorOpen,
      banner2SuccessOpen
    }
  },
  created: function() {
    return this.$store.dispatch('getVuliPushUrl');
  },
  computed: {
    ...mapGetters({vuli_push_url: 'stateVuliPushUrl', setting_result: 'stateSettingResult'}),
  },
  watch: {
    vuli_push_url: {
      immediate: true,
      handler(value) {
        const config = value || {}
        this.form.push_type = config.push_type || 'dingding'
        this.form.hook_url = config.hook_url || ''
        this.form.sign = config.sign || ''
        this.form.keywords = Array.isArray(config.keywords) ? config.keywords : []
        this.form.keyword_match_scope = config.keyword_match_scope || 'title'
      }
    }
  },
  methods: {
    addKeyword() {
      const value = (this.keywordInput || '').trim()
      if (!value) return
      if (this.form.keywords.includes(value)) {
        this.keywordInput = ''
        return
      }
      this.form.keywords.push(value)
      this.keywordInput = ''
    },
    removeKeyword(idx) {
      this.form.keywords.splice(idx, 1)
    },
    update_hook_url(){
      this.$store.dispatch('setVuliPushUrl', {
        'push_type': this.form.push_type,
        'hook_url': this.form.hook_url,
        'sign': this.form.sign,
        'keywords': this.form.keywords,
        'keyword_match_scope': this.form.keyword_match_scope
      });
    },
    check_hook_url(){
      this.$store.dispatch('checkVuliPushUrl', {
        'push_type': this.form.push_type,
        'hook_url': this.form.hook_url,
        'sign': this.form.sign,
        'keywords': this.form.keywords,
        'keyword_match_scope': this.form.keyword_match_scope
      });
    },

  },
  data(){
    return {
      keywordInput: '',
      form: {
        push_type: 'dingding',
        hook_url: '',
        sign: '',
        keywords: [],
        keyword_match_scope: 'title'
      },
      options: [
         {name: '钉钉群机器人', value: 'dingding'},
         {name: '飞书群机器人', value: 'feishu'},
         {name: '企业微信群机器人', value: 'qiyeweixin'},
         {name: '自定义WebHook', value: 'custom'},
         {name: '邮箱', value: 'mail'},

      ]
    }
  }
}
</script>
