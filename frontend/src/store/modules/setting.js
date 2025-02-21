import axios from 'axios';

const state = {
  vuli_push_url: {},
  setting_result: ''
};

const getters = {
  stateVuliPushUrl: state => state.vuli_push_url,
  stateSettingResult: state => state.setting_result
};

const actions = {
  async getVuliPushUrl({commit}) {
    let {data} = await axios.post('/api/settings/get_vuli_push_url');
    await commit('setVuliPushUlr', data);
  },
  async setVuliPushUrl({commit}, item) {
    await commit('setSettingResult', '');
    let params = {push_type: `${item.push_type}`, hook_url: `${item.hook_url}`, sign: `${item.sign}`}
    await commit('setVuliPushUlr', params);
    let {data} = await axios.post('/api/settings/set_vuli_push_url', params);
    await commit('setSettingResult', data);
  },
  async checkVuliPushUrl({commit}, item) {
    await commit('setSettingResult', {'type': '', 'msg': '正在发起请求，请稍候...'});
    let params = {push_type: `${item.push_type}`, hook_url: `${item.hook_url}`, sign: `${item.sign}`}
    await commit('setVuliPushUlr', params);
    let {data} = await axios.post('/api/settings/check_vuli_push_url', params);
    await commit('setSettingResult', data);
  }
};

const mutations = {
  setVuliPushUlr(state, data) {
    state.vuli_push_url = data;
  },
  setSettingResult(state, data) {
    state.setting_result = data;
  }
};

export default {
  state,
  getters,
  actions,
  mutations
};
