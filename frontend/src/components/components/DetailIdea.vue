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
    }
  },

  mounted() {
    this.getIdea()
  },

  methods: {
    getIdea() {
      this.loading = true
      axios.get(`${this.server}idea/${this.$route.params.id}/`)
        .then((response) => {
          this.idea = response.data
          this.loading = false
        })
    }
  }
}
</script>

<style lang="sass" scoped>
@import "@/assets/sass/style.sass"
</style>