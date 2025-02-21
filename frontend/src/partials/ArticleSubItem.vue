<template>
  <li class="flex items-center py-1">
    <svg class="w-3 h-3 fill-current text-sky-500 mr-3 mt-1.5 shrink-0" viewBox="0 0 12 12" xmlns="http://www.w3.org/2000/svg">
      <path d="M10.28 2.28L3.989 8.575 1.695 6.28A1 1 0 00.28 7.695l3 3a1 1 0 001.414 0l7-7A1 1 0 0010.28 2.28z"></path>
    </svg>
    <div class="text-sm">
      <a :href="'/url/'+item.url">{{item.title}}</a><span v-if="item.source.name" class="pl-1 text-xs text-slate-400 dark:text-slate-500">{{item.source.name}}</span>
    </div>

  </li>
</template>

<script>
export default {
  name: 'ArticleSubItem',
  props: ['item'],
}
</script>
