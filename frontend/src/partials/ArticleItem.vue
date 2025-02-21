<template>
  <article class="cursor-pointer" :class="isActive==item.id ? activeClass : 'pb-5'" @click="activeItem(item.id)">
    <div class="absolute top-0 left-0 right-0 h-0.5 bg-sky-500" aria-hidden="true"></div>
      <div class="items-start border-slate-100 dark:border-slate-800" :class="isActive==item.id && item.related_vuls.length==0 ? '': 'border-b pb-5'">
        <div class="grow">
          <div class="text-xs text-slate-500 mb-1">
            <span class="text-sky-500">—</span> {{item.publish_time}}
            <div v-if="item.cve" class="float-right text-xs inline-flex font-medium bg-slate-100 text-slate-500 dark:bg-slate-700 dark:text-slate-100 rounded-full text-center px-2.5 py-1">{{item.cve}}</div>
          </div>
          <h3 class="font-aspekta text-lg font-[650] mb-1">
            <a class="inline-flex relative hover:text-sky-500 duration-150 ease-out before:scale-x-0 before:origin-center before:absolute before:inset-0 before:bg-sky-200 dark:before:bg-sky-500 before:opacity-30 before:-z-10 before:translate-y-1/4 before:-rotate-2 hover:before:scale-100 before:duration-150 before:ease-in-out" :href="'/url/'+item.tinyurl">{{item.title}}</a>
          </h3>
          <div class="md:flex">
            <div class="grow text-sm text-slate-500 dark:text-slate-400" :class="isActive==item.id ? 'break-all' : 'line-clamp-5'">
              {{item.descript}}
            </div>
            <a class="hidden lg:flex shrink-0 text-sky-500 items-center justify-center w-12 group" :href="'/url/'+item.tinyurl" tabindex="-1">
              <svg class="fill-current group-hover:translate-x-2 duration-150 ease-in-out" xmlns="http://www.w3.org/2000/svg" width="14" height="12">
                <path d="M9.586 5 6.293 1.707 7.707.293 13.414 6l-5.707 5.707-1.414-1.414L9.586 7H0V5h9.586Z" />
              </svg>
            </a>
          </div>
        </div>
      </div>
    <div class="px-1 pt-4" :class="isActive==item.id ? '' : 'hidden'">
      <!-- List -->
      <ul>
        <ArticleSubItem v-for="related_vuls in item.related_vuls" :item="related_vuls" />
      </ul>
    </div>
  </article>
</template>

<script>
import ArticleSubItem from '../partials/ArticleSubItem.vue'

export default {
  name: 'ArticleItem',
  components: {
    ArticleSubItem,
  },
  props: ['item'],
  data() {
    return {
      isActive: -1,
      activeClass: 'rounded-lg border border-slate-200 dark:border-slate-800 dark:bg-gradient-to-t dark:from-slate-800 dark:to-slate-800/30 p-5 mb-5',
    }
  },
  methods: {
    activeItem(id){
      this.isActive = this.isActive==-1 ?id : -1;
    }
  }
}
</script>
