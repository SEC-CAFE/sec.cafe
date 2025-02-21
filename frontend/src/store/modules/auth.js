import axios from 'axios';
import { defineStore } from 'pinia';

function deleteStorage(){
  localStorage.removeItem('sec_cafe_user');
}
function userStorageFormat() {
  let settings = localStorage.getItem('sec_cafe_user');
  try {
    if (settings) {
      let user = JSON.parse(settings);
      let token_obj = user.access_token;
      if (token_obj){
        if (Date.parse(token_obj.expire_time) < new Date()){
          deleteStorage();
        }
      }else{
        deleteStorage();
      }

      if (Date.parse(user.vip.expire_time) < new Date()){
        user.type = 0
      }
      return user
    }
    else localStorage.removeItem('sec_cafe_user');;
  } catch (e) {
    deleteStorage();
  }

  return {};
}
function setLoginedUserToStorage(user) {
  let settings = userStorageFormat();
  settings.uid = user.id;
  settings.name = user.username;
  settings.nickname = user.nickname;
  settings.vip = {type: user.vip_type, expire_time: user.vip_expire_time};
  settings.lab = user.lab;
  settings.api_token = user.api_token;
  settings.access_token = {'token': user.access_token, 'expire_time': user.access_token_expire_time};
  localStorage.setItem('sec_cafe_user', JSON.stringify(settings));
}

const state = {
  login_urls: {},
  logined_user: {},
};

const getters = {
  stateLoginUrls: state => state.login_urls,
  logined_user: userStorageFormat,
};

const actions = {
  async getLoginUrls({commit}) {
    let {data} = await axios.get('/api/auth/third_login');
    await commit('setLoginUrls', data);
  },
  async apiCallback({commit}) {
    let urlParams = new URLSearchParams(window.location.search);
      const code = urlParams.get('code')
    let {data} = await axios.get('/api/auth/github_callback?code='+`${code}`);
    await commit('setLoginedUser', data);
    let redirect = localStorage.getItem('sec_cafe_redirect')
    if (redirect){
      window.location.replace(redirect);
      localStorage.removeItem('sec_cafe_redirect');
    }else{
      window.location.replace('/');
    }

  },
  async getMe({commit}, params) {
    const headers = {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + params.access_token,
      'Req-Auth': true,
    };
    let {data} = await axios.post('/api/auth/me', params, { headers })
    await commit('setLoginedUser', data);
  },
  async getLoginedUser({commit}) {
    let {data} = userStorageFormat();
    await commit('setLoginedUser', data);
  },
  async logOut({commit}) {
    let user = null;
    commit('logout', user);
  }
};

const mutations = {
  setLoginUrls(state, data) {
    state.login_urls = data;
  },
  setLoginedUser(state, data) {
    state.logined_user = data;
    setLoginedUserToStorage(data);
  },
  logout(state, data) {
    deleteStorage();
  }
};

export default {
  state,
  getters,
  actions,
  mutations
};

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: {},
    isLoggedIn: false,
  }),
  actions: {
    checkUser() {
      this.user = userStorageFormat()
      if (this.user.name) this.isLoggedIn = true;
    }
  },
});
