import axios from 'axios'
import { createStore } from 'vuex'
import router from './router'

export default createStore({
  state() {
    return {
      server: process.env.NODE_ENV === 'development' ? 'http://127.0.0.1:8000/api/v1/' : 'http://213.108.252.208:4000/api/v1/'
    }
  },


  actions: {
    deleteIdea({ commit, state }, id) {
      return new Promise((resolve, reject) => {
        axios.delete(`${state.server}idea/${id}/`)
          .then((response) => {
            resolve()
          })
      })
    }
  },

  mutations: {
    routeLink(state, link) {
      router.push(link)
    }
  },

  getters: {}
})