<template>
  <!-- Global notification live region, render this permanently at the end of the document -->
  <div aria-live="assertive" class="pointer-events-none fixed inset-0 flex items-end px-4 py-6 sm:items-start sm:p-6 z-50">
    <div class="flex w-full flex-col items-center space-y-4 sm:items-end">
      <!-- Notification panel, dynamically insert this into the live region when it needs to be displayed -->
      <transition enter-active-class="transform ease-out duration-300 transition" enter-from-class="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-2" enter-to-class="translate-y-0 opacity-100 sm:translate-x-0" leave-active-class="transition ease-in duration-100" leave-from-class="opacity-100" leave-to-class="opacity-0">
        <div v-if="showNotification" class="pointer-events-auto w-full max-w-sm overflow-hidden rounded-lg bg-white shadow-lg ring-1 ring-black ring-opacity-5">
          <div class="p-4">
            <div class="flex items-start">
              <div class="flex-shrink-0">
                <XCircleIcon v-if="type=='error'" class="h-6 w-6 text-red-400" aria-hidden="true" />
                <InformationCircleIcon v-else-if="type=='info'" class="h-6 w-6 text-blue-400" aria-hidden="true" />
                <ExclamationCircleIcon v-else-if="type=='warn'" class="h-6 w-6 text-yellow-400" aria-hidden="true" />
                <CheckCircleIcon v-else class="h-6 w-6 text-green-400" aria-hidden="true" />
              </div>
              <div class="ml-3 w-0 flex-1 pt-0.5">
                <p v-if="title" class="text-sm font-medium text-gray-900">{{ title }}</p>
                  <p class="mt-1 text-sm text-gray-500">{{ message }}</p>
              </div>
              <div class="ml-4 flex flex-shrink-0">
                <button type="button" @click="close" class="inline-flex rounded-md bg-white text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">
                  <span class="sr-only">Close</span>
                  <XMarkIcon class="h-5 w-5" aria-hidden="true" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
import { ref, watch, defineEmits, defineComponent} from 'vue'
import { CheckCircleIcon, InformationCircleIcon, ExclamationCircleIcon, XCircleIcon } from '@heroicons/vue/24/outline'
import { XMarkIcon } from '@heroicons/vue/20/solid'

export default {
  name: 'Notification',
  components: {
    CheckCircleIcon, InformationCircleIcon, ExclamationCircleIcon, XCircleIcon,
    XMarkIcon
  },
  props: {
    type: {
      type: String,
      default: 'ok',
      required: false,
    },
    title: {
      type: String,
      default: null,
      required: false
    },
    message: {
      type: String,
      default: null,
      required: true
    },
    show: {
      type: Boolean,
      default: false,
      required: true
    }
  },
  emits: ["closeNoti"],
  methods: {
    close(){
      this.$emit('closeNoti')
    }
  },
  setup(props, context) {
    const showNotification = ref(props.show);
    watch(() => props.show, (newValue) => {
      showNotification.value = newValue;
    });
    return {
      showNotification
    }
  },
}
</script>
