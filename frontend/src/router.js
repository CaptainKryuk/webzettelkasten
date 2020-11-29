import { createRouter, createWebHistory } from 'vue-router'
import axios from 'axios'
import store from '@/store'

const routes = [
  {
    path: '',
    component: () => import('@/components/HomeWrapper.vue'),
    children: [
      {
        path: '',
        redirect: '/minds'
      },
      {
        path: 'minds',
        component: () => import('@/components/components/Home.vue')
      },
      {
        path: 'tags',
        component: () => import('@/components/components/Tags.vue')
      },

      {
        path: '/minds/new',
        beforeEnter: (to, from, next) => {
          axios.post(`${store.state.server}idea/`)
            .then((response) => {
              next(`/minds/${response.data.id}/update`)
            })
        }
      },
      {
        path: '/minds/:id',
        component: () => import('@/components/components/DetailIdea.vue'),
      },
      {
        path: '/minds/:id/update',
        component: () => import('@/components/components/UpdateIdea.vue'),
      }
    ]
  }
]

const router = createRouter({
  mode: 'history',
  history: createWebHistory(),
  routes
})

export default router