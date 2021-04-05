import axios from 'axios'
import { createStore } from 'vuex'
import router from './router'

export default createStore({
  state() {
    return {
      server: process.env.NODE_ENV === 'development' ? 'http://127.0.0.1:8000/api/v1/' : 'http://213.108.252.201:4000/api/v1/',
      media_server: process.env.NODE_ENV === 'development' ? 'http://127.0.0.1:8000' : 'http://213.108.252.201:4000',

      email: localStorage.getItem('email'),
      id: localStorage.getItem('id'),
      auth_headers: {Authorization: 'JWT ' + localStorage.getItem("token")},

      username: 'mail',

      articles: [],
      article: {},

      articles_search: '',
      article_loading: false
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
    },

    getArticles({ commit, state }, type) {
      // 
      
      axios.get(`${state.server}articles/${type === 'all' ? 'all_articles/' : ''}`,
        {headers: state.auth_headers})
        .then((response) => {
          commit('ASSIGN_ARTICLES', response.data)
        })
    },

    getArticle({ commit, state }, id) {
      if (id) {
        state.article_loading = true
        return new Promise((resolve, reject) => {
          axios.get(`${state.server}articles/${id}/`,
            {headers: state.auth_headers})
            .then((response) => {
              commit('ASSIGN_ARTICLE', response.data)
            })
        })
      }
    }
  },

  mutations: {
    DELETE_ARTICLE(state, id) {
      state.articles.forEach((article, index) => {
        if (Number(article.id) === Number(id)) {
          state.articles.splice(index, 1)
        }
      })
    },

    ASSIGN_ARTICLES(state, data) {
      state.articles = data
    },

    UPDATE_ARTICLES_SEARCH(state, value) {
      state.articles_search = value
    },

    UPDATE_EMAIL(state, email) {
      localStorage.setItem('email', email)
      state.email = email
    },
    UPDATE_ID(state, id) {
      localStorage.setItem('id', id)
      state.id = id
    },
    UPDATE_AUTH_HEADERS(state, token) {
      localStorage.setItem('token', token)
      state.auth_headers = {Authorization: 'JWT ' + token}
    },
    
    // * articles functions
    ASSIGN_ARTICLE(state, data) {
      state.article = data
      setTimeout(() => {
        state.article_loading = false
      }, 100)
    },
    routeTo(state, link) {
      router.push(link)
    },

    ADD_NEW_BLOCK(state, args) {
      // * if we add new block to the center -> add it after passed index
      if (args.index === state.article.blocks.length - 1) {
        state.article.blocks.push(args.data)
      } else {
        state.article.blocks.splice(args.index + 1, 0, args.data)
      }
    },

    DELETE_BLOCK(state, id) {
      for (let i=0; i < state.article.blocks.length; i++) {
        if (Number(state.article.blocks[i].id) === Number(id)) {
          state.article.blocks.splice(i, 1)
        }
      } 
    }
  },

  getters: {}
})