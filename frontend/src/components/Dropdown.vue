<template>
  <li>
    <Tooltip v-if="vip" position="bottom">
      <template v-slot:showIcon>
        <svg  class="pr-1" width="16" height="16" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 4H4L15 44H23L12 4Z" fill="none" stroke="#0ca5e9" stroke-width="4" stroke-linejoin="round"/>
          <path d="M23 44L44 4" stroke="#0ca5e9" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </template>
      <div class="text-xs whitespace-nowrap">{{ vip_tip }}</div>
    </Tooltip>
  </li>
  <li
    class="relative"
    @mouseenter="dropdownOpen = true"
    @mouseleave="dropdownOpen = false"
    @focusin="dropdownOpen = true"
    @focusout="dropdownOpen = false"
  >
    <a
      class="text-slate-800 dark:text-slate-100 hover:text-slate-600 dark:hover:text-slate-300 flex items-center transition duration-150 ease-in-out"
      href="#0"
      aria-haspopup="true"
      aria-expanded={dropdownOpen}
      @click.prevent
    >
      {{title}}
      <svg class="w-3 h-3 fill-current text-gray-500 cursor-pointer ml-1 shrink-0" viewBox="0 0 12 12" xmlns="http://www.w3.org/2000/svg">
        <path d="M10.28 4.305L5.989 8.598 1.695 4.305A1 1 0 00.28 5.72l5 5a1 1 0 001.414 0l5-5a1 1 0 10-1.414-1.414z" />
      </svg>
    </a>
    <transition
      enter-active-class="transition ease-out duration-200 transform"
      enter-from-class="opacity-0 -translate-y-2"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition ease-out duration-200"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <ul v-show="dropdownOpen" class="origin-top-right absolute top-full right-0 w-40 bg-white dark:bg-slate-900  border-slate-200 dark:border-slate-800 dark:bg-gradient-to-t dark:from-slate-800 dark:to-slate-800/30 py-2 ml-4 rounded shadow-lg">
        <slot />
      </ul>
    </transition>
  </li>
</template>
<script>
import Tooltip from '../components/Tooltip.vue'
export default {
  name: 'Dropdown',
  components: {
    Tooltip,
  },
  props: {
    title: {
      type: String,
      default: null,
      required: true
    },
    vip: {
      type: Number,
      default: 0,
      required: true
    },
    vip_tip: {
      type: String,
      default: 'VIP',
      required: true
    },
  },
  data: function () {
    return {
      dropdownOpen: false
    }
  },
}
</script>
