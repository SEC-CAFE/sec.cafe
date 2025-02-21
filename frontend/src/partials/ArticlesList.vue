<template>
  <section>
    <div class="flex flex-wrap mb-3 items-center">
      <h2 class="font-aspekta text-xl font-[650]">最新漏洞</h2>
      <a class="" href="/feed/vuli" target="_blank">
        <Tooltip position="bottom" canclick="true">
          <div class="text-xs whitespace-nowrap">RSS订阅</div>
          <template v-slot:showIcon>
              <RssIcon class="h-5 w-5 text-sky-500 mt-1 ml-1" aria-hidden="true" />
          </template>
        </Tooltip>
      </a>
      <div v-if="searchVul" @click="deleteSearchKeyword" class="h-fit	ml-3 cursor-pointer float-right text-xs inline-flex font-medium bg-slate-100 text-slate-500 dark:bg-slate-700 dark:text-slate-100 rounded-full text-center px-2.5 py-1">
          <XMarkIcon class="h-4 w-4 text-slate-500 dark:text-slate-100" aria-hidden="true" />{{ searchVul }}
        </div>
      <div class="ml-auto flex items-center">
        <span class="text-sm">条件筛选</span><VuliFilter align="right" />
        <a href="/spider" target="_blank" class="ml-1">
          <Tooltip position="bottom"  canclick="true">
            <div class="text-xs whitespace-nowrap">情报源及爬虫说明</div>
            <template v-slot:showIcon>
              <InformationCircleIcon class="h-5 w-5 text-sky-500" aria-hidden="true" />
            </template>
          </Tooltip>
        </a>
        <a href="/settings" target="_blank" class="ml-1">
          <Tooltip position="bottom"  canclick="true">
            <div class="text-xs whitespace-nowrap">订阅</div>
            <template v-slot:showIcon>
              <StarIcon class="h-5 w-5 text-sky-500" aria-hidden="true" />
            </template>
          </Tooltip>
        </a>
      </div>
    </div>

    <!-- Filters -->
    <!--
    <ul class="flex flex-wrap text-sm border-b border-slate-100 dark:border-slate-800">
      <li class="px-3 -mb-px">
        <a class="block py-3 font-medium text-slate-800 dark:text-slate-100 border-b-2 border-sky-500" href="#0">最新漏洞</a>
      </li>
      <li class="px-3 -mb-px">
        <a class="block py-3 text-slate-500 hover:text-slate-600 dark:text-slate-400 dark:hover:text-slate-300" href="#0">热点漏洞</a>
      </li>
    </ul>
    -->

    <!-- Articles list -->
    <div>
        <ArticleItem v-for="item in items" :key="item.id" :item="item" />
    </div>

  </section>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import { RssIcon } from '@heroicons/vue/24/solid'
import { InformationCircleIcon } from '@heroicons/vue/24/outline'
import { XMarkIcon } from '@heroicons/vue/24/outline'
import { StarIcon } from '@heroicons/vue/24/outline'
import ArticleItem from '../partials/ArticleItem.vue'
import Tooltip from '../components/Tooltip.vue'
import VuliFilter from '../components/VuliFilter.vue'


export default {
  name: 'ArticlesList',
  components: {
    ArticleItem,
    Tooltip,
    VuliFilter,
    RssIcon,
    InformationCircleIcon,
    XMarkIcon,
    StarIcon
  },
  created: function() {
    return this.$store.dispatch('getVuls', 1);
  },
  computed: {
    ...mapGetters({items: 'stateVuls', searchVul: 'searchVul'}),
  },
  methods: {
    deleteSearchKeyword(){
      const currentRoute = this.$route;
      const newQuery = { ...currentRoute.query };
      delete newQuery['vul'];
      const newPath = `${currentRoute.path}?${new URLSearchParams(newQuery).toString()}`;
      window.location.replace(newPath);
  }
  }
}
</script>
