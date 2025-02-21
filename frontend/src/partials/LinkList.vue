<template>
  <section>
    <div class="flex flex-wrap mb-3 items-center">
      <h2 class="font-aspekta text-xl font-[650]">安全导航</h2>
      <div v-if="keyword" @click="deleteSearchKeyword" class="h-fit	ml-3 cursor-pointer float-right text-xs inline-flex font-medium bg-slate-100 text-slate-500 dark:bg-slate-700 dark:text-slate-100 rounded-full text-center px-2.5 py-1">
          <XMarkIcon class="h-4 w-4 text-slate-500 dark:text-slate-100" aria-hidden="true" />{{ keyword }}
      </div>
      <div class="ml-auto flex items-center">
        <a href="https://github.com/SEC-CAFE/sec.cafe/issues/new?template=add-new-link.md&title=%5BNew+Link%5D%20name" target="_blank" class="ml-1">
          <Tooltip position="bottom"  canclick="true">
            <div class="text-xs whitespace-nowrap">添加导航</div>
            <template v-slot:showIcon>
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="#38BDF8" class="size-6">
                <path  stroke-linecap="round" stroke-linejoin="round" d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
              </svg>
            </template>
          </Tooltip>
        </a>
      </div>
    </div>

    <!-- Filters -->
    <ul class="flex flex-wrap text-sm border-b border-slate-100 dark:border-slate-800">
      <li class="pr-3 -mb-px">
        <a class="block py-3" :class="type=='src' ? activeClass : noActiveClass" href="#0" @click="update_filter('src')">SRCs</a>
      </li>
      <li class="px-3 -mb-px">
        <a class="block py-3 " :class="type=='vuldb' ? activeClass : noActiveClass" href="#0" @click="update_filter('vuldb')">Vuldbs</a>
      </li>
    </ul>

    <div class="pt-5">
        <LinkItem v-for="item in items" :key="item.id" :item="item" />
    </div>

  </section>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import { XMarkIcon } from '@heroicons/vue/24/outline'
import LinkItem from '../partials/LinkItem.vue'
import Tooltip from '../components/Tooltip.vue'


export default {
  name: 'LinkList',
  components: {
    LinkItem,
    Tooltip,
    XMarkIcon,
  },
  data() {
    return {
      activeClass: 'font-medium text-slate-800 dark:text-slate-100 border-b-2 border-sky-500',
      noActiveClass: 'text-slate-500 hover:text-slate-600 dark:text-slate-400 dark:hover:text-slate-300'
    }
  },
  created: function() {
    return this.$store.dispatch('getLinks', 1);
  },
  computed: {
    ...mapGetters({items: 'stateLinks', keyword: 'searchKeyword', type: 'stateType'}),
  },
  methods: {
    update_filter(_type){
      const currentRoute = this.$route;
      const newQuery = { ...currentRoute.query };
      if (!_type) {delete newQuery['type'];} else { newQuery['type'] = _type;}

      const newPath = `${currentRoute.path}?${new URLSearchParams(newQuery).toString()}`;
      window.location.replace(newPath);
    }
  }
}
</script>
