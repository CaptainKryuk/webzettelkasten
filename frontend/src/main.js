import { createApp } from 'vue';
import App from './App.vue';
import store from './store'
import router from './router'
import axios from 'axios'

import contenteditable from 'vue-contenteditable'


// axios initialization
import service from './axios'

const app = createApp(App).use(store).use(router)

// register global all utils in utils folder
import inputs from './global/index'

let components = [...inputs]
components.forEach(component => {
  app.component(component.name, component)
})

app.config.globalProperties.$axios = axios

// app.use(contenteditable)

app.component(contenteditable.name, contenteditable)

// directives
app.directive('click-outside', {
  beforeMount(el, binding) {
    el.clickOutsideEvent = function (event) {
      // here I check that click was outside the el and his childrens
      if (el==event.target) {
        // Если кликнули на элемент на котором записана директива
      }
      
      if (el.contains(event.target)) {
        // если кликнули на элемент, который находится внутри директивы
      }
      if (!(el===event.target || el.contains(event.target))) {
        // вызов функции, переданной через имя в директиву
        binding.value()
      }
    };
    document.body.addEventListener('click', el.clickOutsideEvent)
  },
  unmounted: function (el) {
    document.body.removeEventListener('click', el.clickOutsideEvent)
  }
})

app.mount('#app');
