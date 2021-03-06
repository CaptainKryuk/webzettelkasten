import axios from 'axios'
import { createStore } from 'vuex'
import router from './router'

export default createStore({
  state() {
    return {
      server: process.env.NODE_ENV === 'development' ? 'http://127.0.0.1:8000/api/v1/' : 'https://api.webzettel.com/api/v1/',
      media_server: process.env.NODE_ENV === 'development' ? 'http://127.0.0.1:8000' : 'https://api.webzettel.com',

      email: localStorage.getItem('email'),
      id: localStorage.getItem('id'),
      auth_headers: {Authorization: 'JWT ' + localStorage.getItem("token")},

      username: localStorage.getItem('username'),

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
    UPDATE_USERNAME(state, username) {
      localStorage.setItem('username', username)
      state.username = username
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
        // * block was added to the center
        state.article.blocks.splice(args.index + 1, 0, args.data)
        
        state.article.blocks.forEach((block, index) => {
          let increase_next_blocks = false;
          if (block.order_number === args.data.order_number) {
            increase_next_blocks = true
          }

          if ((block.order_number >= args.data.order_number) && (block.id !== args.data.id) && increase_next_blocks) {
            block.order_number += 1
          }
        })
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