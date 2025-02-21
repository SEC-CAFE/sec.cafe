<template>
  <button class="fixed z-1 w-10 h-10 pl-2.5 pt-2.5 bottom-40 inline-flex text-sky-500 rounded-full border border-slate-200 dark:border-slate-800 dark:bg-gradient-to-t dark:from-slate-800 dark:to-slate-800/30" :class="isHide? 'isHide hidden': 'isShow', firstShow? '': 'hidden'"  @click="backTop()">

    <span class="sr-only">BackTop</span>
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 32 32" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 stroke-2">
      <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l7.5-7.5 7.5 7.5m-15 6l7.5-7.5 7.5 7.5" />
    </svg>


  </button>

</template>


<script>
export default {
  name: 'WidgetBacktop',
  data(){
    return {
      firstShow: false,//初始化隐藏组件
      isHide: false,
      scrollFLag: true,
    }
  },
  created() {
    document.addEventListener('scroll', () => {
      let scroll = document.documentElement.scrollTop;
      if(scroll > 200){
        this.isHide = false
        this.firstShow = true
      }else{
        this.isHide = true
      }
    })
  },
  methods: {
    backTop() {
      if(this.scrollFLag){
        this.scrollFLag = false
        //屏幕高度
        let scroll = document.documentElement.scrollTop;
        let scrolltimer = setInterval(()=> {
          scroll -= 50
          document.documentElement.scrollTop = Math.max(scroll, 0)
          if( scroll <= 0){
            clearInterval(scrolltimer)
          }
        }, 10)
        this.scrollFLag = true
      }
    }
  }
}
</script>
<style>
  .isShow{
   animation: back-top-move 0.5s forwards linear, back-top-yurayura 2s 0.6s forwards linear infinite;
  }
  .isHide{
   animation: back-top-hide 0.5s forwards linear;
  }
</style>
