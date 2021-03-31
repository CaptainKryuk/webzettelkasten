<template>

<div style="display: flex;" v-for="(a, index) in articles" :key="index">
  <span>{{ a.title || 'no title'}}</span>
  <router-link :to="`/mind/article/${a.id}`">to ar</router-link>
</div>
</template>

<script>
import { mapState } from 'vuex'
export default {
  name: 'Recent',

  data() {
    return {
      articles: []
    }
  },

  mounted() {
    this.getArticles()
  },

  computed: {
    ...mapState(['server', 'auth_headers'])
  },

  methods: {
    getArticles() {
      this.$axios.get(`${this.server}articles?filter=last`,
        {headers: this.auth_headers})
        .then((response) => {
          this.articles = response.data
        })
    }
  }
}
</script>