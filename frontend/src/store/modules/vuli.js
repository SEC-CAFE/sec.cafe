import axios from 'axios';

const state = {
  vuls: [],
  keyword: '',
  order: '',
  source_limit: 0,
};

const getters = {
  stateVuls: state => state.vuls,
  searchVul: state => state.keyword,
  stateOrder: state => state.order,
  stateSourceLimit: state => state.source_limit,
};

const actions = {
  async getVuls({commit}, start) {
    let urlParams = new URLSearchParams(window.location.search);
    let keyword = urlParams.get('vul');
    let order= urlParams.get('order');
    let source_limit = urlParams.get('source_limit');

    if (!keyword){keyword=''}
    if (!source_limit){source_limit=0}else{source_limit=1}
    let params = {start: `${start}`, keyword: `${keyword}`, order: `${order}`, source_limit: `${source_limit}`}
    let {data} = await axios.post('/api/vuli/new', params);
    await commit('setVuls', data.data);
    await commit('setKeyword', keyword);
    await commit('setOrder', order);
    await commit('setSourceLimit', source_limit);
  }
};

const mutations = {
  setVuls(state, data) {
    state.vuls = data;
  },
  setKeyword(state, data) {
    state.keyword = data;
  },
  setOrder(state, data) {
    state.order = data;
  },
  setSourceLimit(state, data) {
    state.source_limit = data;
  }
};

export default {
  state,
  getters,
  actions,
  mutations
};
