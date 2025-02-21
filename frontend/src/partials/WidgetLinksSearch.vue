<template>
  <section>
    <form class="w-full max-w-[276px]">
      <div class="flex flex-wrap">
        <div class="w-full">
          <label class="block text-sm sr-only" for="search">Search</label>
          <div class="relative flex items-center">
            <input id="searchInput" name="keyword" type="search" class="form-input py-1 w-full pl-10"  @input="getSearchResult" :value=keyword />
            <div class="absolute inset-0 right-auto flex items-center justify-center">
              <svg class="w-4 h-4 shrink-0 mx-3" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg">
                <path class="fill-slate-400" d="M7 14c-3.86 0-7-3.14-7-7s3.14-7 7-7 7 3.14 7 7-3.14 7-7 7zM7 2C4.243 2 2 4.243 2 7s2.243 5 5 5 5-2.243 5-5-2.243-5-5-5zm8.707 12.293a.999.999 0 11-1.414 1.414L11.9 13.314a8.019 8.019 0 001.414-1.414l2.393 2.393z"></path>
              </svg>
            </div>
          </div>
        </div>
      </div>
    </form>
  </section>
</template>

<script>
import { mapGetters, } from 'vuex';

export default {
  name: 'WidgetLinksSearch',
  computed: {
    ...mapGetters({keyword: 'searchKeyword'})
  },
  methods: {
    getSearchResult(){
      const search_input = document.getElementById('searchInput');
      this.$store.dispatch('searchLinks', search_input.value);
    }
  }
}
</script>
