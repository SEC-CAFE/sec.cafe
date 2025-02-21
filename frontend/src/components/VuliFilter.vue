<template>
  <div class="relative inline-flex">
    <button
      ref="trigger"
      class="btn p-0 mx-1 border-slate-200 hover:border-slate-300 text-slate-500 hover:text-slate-600"
      aria-haspopup="true"
      @click.prevent="dropdownOpen = !dropdownOpen"
      :aria-expanded="dropdownOpen"
    >
      <span class="sr-only">Filter</span><wbr />
      <svg class="w-4 h-4 fill-current" viewBox="0 0 16 16">
        <path d="M9 15H7a1 1 0 010-2h2a1 1 0 010 2zM11 11H5a1 1 0 010-2h6a1 1 0 010 2zM13 7H3a1 1 0 010-2h10a1 1 0 010 2zM15 3H1a1 1 0 010-2h14a1 1 0 010 2z" />
      </svg>
    </button>
    <transition
      enter-active-class="transition ease-out duration-200 transform"
      enter-from-class="opacity-0 -translate-y-2"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition ease-out duration-200"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div v-show="dropdownOpen" class="origin-top-right z-10 absolute top-full min-w-40 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 pt-1.5 rounded shadow-lg overflow-hidden mt-1" :class="align === 'right' ? 'right-0' : 'left-0'">
        <div ref="dropdown" class="w-40">
          <div class="text-xs font-semibold text-slate-400 uppercase pt-1.5 pb-2 px-4">Filters</div>
          <ul class="mb-4">
            <li class="py-1 px-3">
              <label class="flex items-center">
                <input v-if="stateSourceLimit" type="checkbox" class="form-checkbox" ref="source_limit" checked="checked"/>
                <input v-else type="checkbox" class="form-checkbox" ref="source_limit"/>
                <span class="text-sm font-medium ml-2">来源>1的漏洞</span>
              </label>
            </li>
            <li class="py-1 px-3">
              <label class="flex items-center">
                <input v-if="stateOrder" type="checkbox" class="form-checkbox" ref="order_time" checked="checked"/>
                <input v-else type="checkbox" class="form-checkbox" ref="order_time"/>
                <span class="text-sm font-medium ml-2">按更新时间排序</span>
              </label>
            </li>
          </ul>
          <div class="py-2 px-3 border-t border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900">
            <ul class="flex items-center justify-between">
              <li>
                <button class="btn-xs bg-white dark:bg-slate-800 border-slate-200 hover:border-slate-300 text-slate-500 hover:text-slate-600" @click="clear()">清除</button>
              </li>
              <li>
                <button class="btn-xs bg-sky-500 hover:bg-sky-600 text-white" @click="update_filter()" @focusout="dropdownOpen = false">确认</button>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'VuliFilter',
  props: ['align'],
  setup() {

    const dropdownOpen = ref(false)
    const trigger = ref(null)
    const dropdown = ref(null)

    // close on click outside
    const clickHandler = ({ target }) => {
      if (!dropdownOpen.value || dropdown.value.contains(target) || trigger.value.contains(target)) return
      dropdownOpen.value = false
    }

    // close if the esc key is pressed
    const keyHandler = ({ keyCode }) => {
      if (!dropdownOpen.value || keyCode !== 27) return
      dropdownOpen.value = false
    }

    onMounted(() => {
      document.addEventListener('click', clickHandler)
      document.addEventListener('keydown', keyHandler)
    })

    onUnmounted(() => {
      document.removeEventListener('click', clickHandler)
      document.removeEventListener('keydown', keyHandler)
    })

    return {
      dropdownOpen,
      trigger,
      dropdown,
    }
  },
  computed: {
    ...mapGetters({stateOrder: 'stateOrder', stateSourceLimit: 'stateSourceLimit'}),
  },
  methods: {
    clear(){
      this.$refs.source_limit.checked = false;
      this.$refs.order_time.checked = false;
    },
    update_filter(){
      this.dropdownOpen = false;
      const source_limit = this.$refs.source_limit.checked;
      const order_time = this.$refs.order_time.checked;

      const currentRoute = this.$route;
      const newQuery = { ...currentRoute.query };
      if (!source_limit) {delete newQuery['source_limit'];} else { newQuery['source_limit'] = 1;}
      if (!order_time) {delete newQuery['order'];} else { newQuery['order'] = 'update_time';}

      const newPath = `${currentRoute.path}?${new URLSearchParams(newQuery).toString()}`;
      window.location.replace(newPath);
    }
  }
}
</script>
