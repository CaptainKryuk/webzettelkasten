import { createRouter, createWebHistory } from 'vue-router'
import axios from 'axios'
import store from '@/store'

const routes = [
  {
    path: '',
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/mind',
    component: () => import('@/views/articles/ArticlesWrapper.vue'),
    beforeEnter (to, from, next) {
      axios.get(store.state.server + 'user/authentication/',
        {headers: store.state.auth_headers})
        .then(function () {
          next()
        })
        .catch(function () {
        })
    },
    children: [
      {
        path: '',
        redirect: '/mind/recent'
      },
      {
        path: 'recent',
        name: 'Recent',
        component: () => import('@/views/articles/components/Recent.vue'),
        children: [
          {
            path: ':id/delete',
            component: () => import('@/views/articles/components/DeleteArticle.vue')
          }
        ]
      },
      {
        path: 'articles',
        name: 'Articles',
        component: () => import('@/views/articles/components/AllArticles.vue'),
        children: [
          {
            path: ':id/delete',
            component: () => import('@/views/articles/components/DeleteArticle.vue')
          }
        ]
      },
      {
        path: 'tags',
        name: 'Tags',
        component: () => import('@/views/articles/components/Tags.vue')
      },
      {
        path: 'links',
        name: 'Links',
        component: () => import('@/views/articles/components/Links.vue')
      },
    ]
  },
  {
    path: '/mind/new',
    beforeEnter (to, from, next) {
      axios.post(store.state.server + 'articles/',
        {},
        {headers: store.state.auth_headers})
        .then(function (response) {
          next(`/mind/article/${response.data.id}`)
        })
        .catch(function (error) {
          next('/404')
        })
    },
  },
  {
    path: '/mind/article/:id',
    component: () => import('@/views/articles/components/UpdateArticle.vue'),
    name: 'NewArticle'
  },
  {
    path: '/registration',
    name: 'Registration',
    component: () => import('@/views/account/Registration.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/account/Login.vue')
  },
  { 
    path: "/logout", 
    component: () => import("@/views/account/Logout.vue") 
  },
]

const router = createRouter({
  mode: 'history',
  history: createWebHistory(),
  routes
})

export default router