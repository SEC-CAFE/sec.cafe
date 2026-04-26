<template>
  <section v-if="showYearlySponsors && yearlySponsors.length > 0">
    <h2 class="font-aspekta text-xl font-[650] mb-5">年度赞助商</h2>

    <!-- Cards -->
    <div class="grid sm:grid-cols-2 md:grid-cols-1 lg:grid-cols-2 gap-2">
      <a v-for="item in yearlySponsors" :key="item.name" :href="item.href" class="rounded border border-slate-200 dark:border-slate-800 dark:bg-gradient-to-t dark:from-slate-800 dark:to-slate-800/30 hover:rotate-0 transition-transform duration-700 hover:duration-100 ease-in-out p-2">
        <img :src="item.logo" :alt="item.name">
      </a>
    </div>

  </section>
</template>

<script>
import { computed, inject } from 'vue'
import sponsorConfig from '../config/sponsor.config'

export default {
  name: 'WidgetLogos',
  setup() {
    const globalConfig = inject('globalConfig')
    const yearlySponsors = computed(() => sponsorConfig.yearlySponsors || [])
    const showYearlySponsors = computed(() => !!globalConfig.showYearlySponsors)
    return { yearlySponsors, showYearlySponsors }
  }
}
</script>
