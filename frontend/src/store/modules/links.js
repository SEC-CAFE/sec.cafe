import axios from 'axios';

const state = {
  links: [],
  o_links: [],
  keyword: '',
  type: 'src',
};

const getters = {
  stateLinks: state => state.links,
  searchKeyword: state => state.keyword,
  stateType: state => state.type
};

const actions = {
  async getLinks({commit}, start) {
    let urlParams = new URLSearchParams(window.location.search);
    let keyword = urlParams.get('keyword');
    let type = urlParams.get('type');

    //if (!keyword){keyword=''}
    if (!type){type='src'}
    //let params = {keyword: `${keyword}`, type: `${type}`}
    let params = {type: `${type}`}

    let {data} = await axios.post('/api/links/query', params);
    await commit('setOLinks', data.data);
    await commit('setType', type);
    //await commit('setKeyword', keyword);
    await commit('searchLinks', keyword);
  },
  async searchLinks({commit}, keyword) {
    await commit('searchLinks', keyword);
  }
};

const mutations = {
  setOLinks(state, data) {
    state.o_links = data;
  },
  searchLinks(state, keyword) {
    if (!keyword){
      state.links = state.o_links;
    }else{
      keyword = String(keyword).trim();
      keyword = keyword.toLowerCase();
      let new_data = []
      state.o_links.forEach(function(item, index) {
        let name = item['name'].toLowerCase();
        let short_name = item['short_name'].toLowerCase();
        if (name.indexOf(keyword) != -1 || short_name.indexOf(keyword) != -1){
          new_data.push(item)
        }
      });
      state.links = new_data;
    }
    state.keyword = keyword;

  },
  setKeyword(state, data) {
    state.keyword = data;
  },
  setType(state, data) {
    state.type = data;
  }
};

export default {
  state,
  getters,
  actions,
  mutations
};
