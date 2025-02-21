import { createStore } from "vuex";

import vuli from './modules/vuli';
import auth from './modules/auth';
import setting from './modules/setting';
import links from './modules/links';

export default createStore({
  modules: {
    vuli,
    auth,
    setting,
    links
  }
});
