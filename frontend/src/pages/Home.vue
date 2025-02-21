<template>
  <div class="min-h-screen flex">

    <!-- Main content -->
    <main class="grow overflow-hidden">
      <div class="flex flex-col min-h-screen overflow-hidden supports-[overflow:clip]:overflow-clip">

        <Header />

        <!-- Content -->
        <div class="w-full max-w-[1072px] mx-auto grow md:flex space-y-8 md:space-y-0 md:space-x-8 pb-16 pt-20 md:pb-20 md:pt-28">

          <!-- Middle area -->
          <div class="grow px-6 md:min-w-[700px]">
            <div class="max-w-[700px]">
              <div class="space-y-10">

                <ArticlesList />

              </div>
            </div>
          </div>

          <!-- Right sidebar -->
          <aside class="md:w-[240px] lg:w-[300px] shrink-0 px-6">
            <div class="space-y-6">
              <WidgetSearch />
              <WidgetUpdate />
              <WidgetSponsor />
              <WidgetAds />
              <WidgetLogos />
              <WidgetLinks />
              <Backtop />

            </div>
          </aside>

        </div>

        <Footer />

      </div>
    </main>

  </div>
</template>

<script>
import { inject } from 'vue';

import SideNavigation from '../partials/SideNavigation.vue'
import Header from '../partials/Header.vue'
import ArticlesList from '../partials/ArticlesList.vue'
import WidgetUpdate from '../partials/WidgetUpdate.vue'
import WidgetSponsor from '../partials/WidgetSponsor.vue'
import WidgetAds from '../partials/WidgetAds.vue'
import WidgetLogos from '../partials/WidgetLogos.vue'
import WidgetLinks from '../partials/WidgetLinks.vue'
import WidgetSearch from '../partials/WidgetSearch.vue'
import Footer from '../partials/Footer.vue'
import Backtop from '../components/Backtop.vue'

import { useHead } from '@vueuse/head'

export default {
  name: 'Home',
  components: {
    SideNavigation,
    Header,
    ArticlesList,
    WidgetSponsor,
    WidgetUpdate,
    WidgetAds,
    WidgetLogos,
    WidgetLinks,
    WidgetSearch,
    Footer,
    Backtop,
  },
  setup() {
    const globalConfig = inject('globalConfig');
    const pageKeywords = '';
    useHead({
      title: '最新漏洞',
      titleTemplate: '%s | ' + globalConfig.siteTitle,
      meta: [
        {
          name: 'description',
          content: globalConfig.siteDescript
        },
        {
          name: 'keywords',
          content: globalConfig.siteKeywords + pageKeywords
        }
      ]
    });
  }
}
</script>
