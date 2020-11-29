<template>
  <div class="spinner large" v-if="loading"></div>

  <div class="detail_idea" v-if="!loading && Object.keys(idea).length">
    <h2 class="idea_title">{{ idea.title }}</h2>
    <p class="base_name">{{ idea.base_name }}</p>

    <!-- <p class="text">{{ idea.text }}</p> -->

      <div v-html="markdown_text"></div>
  </div>

  <router-link to="update">Изменить</router-link>
</template>

<script>
import marked from 'marked'
import { mapState } from 'vuex'
import axios from 'axios'

export default {
  name: "DetailIdea",

  data() {
    return {
      idea: {},
      loading: false
    }
  },

  computed: {
    ...mapState(['server']),
    
    markdown_text: function() {
      return marked(this.idea.text);
    },

    code_selectors() {

    }
  },

  mounted() {
    this.getIdea()
    this.changeSelectors()
  },

  methods: {
    getIdea() {
      this.loading = true
      axios.get(`${this.server}idea/${this.$route.params.id}/`)
        .then((response) => {
          this.idea = response.data
          this.loading = false
        })
    },

    changeSelectors() {
      return setTimeout(() => {
        // style dict
        let img_dict = {
          'language-js': '/static/img/js.svg',
          'language-css': '/static/img/css.svg',
          'language-python': '/static/img/python.svg',
          'language-html': '/static/img/html.svg',
          'language-vuejs': '/static/img/vuejs.svg',
        }

        // get all <code></code>
        let code_elements = document.querySelectorAll('code')
        code_elements.forEach((code) => {

          // get parent
          let code_parent = code.parentElement
          
          // create new img
          let new_element = document.createElement('img')

          code_parent.style.margin = '0 0 40px 0'

          new_element.src = img_dict[code.classList]
          new_element.style.display = 'block'
          new_element.style.width = '30px'
          new_element.style.height = '30px'
          new_element.style.margin = '20px 0 10px 0'
          new_element.style.position = 'relative'
          new_element.style.left = '-5px'

          code_parent.insertBefore(new_element, code)
        })
      }, 500)
    }
  }
}
</script>

<style lang="sass" scoped>
@import "@/assets/sass/style.sass"
</style>