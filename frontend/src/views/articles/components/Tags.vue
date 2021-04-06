<template>

<div class="tags_articles_block" v-for="(tag, index) in Object.keys(tags)" :key="index">
  <div class="tag">
    <h2># {{ tag }}</h2>
  </div>
  <div class="tags_articles">
    <div class="detail_tags_article" v-for="(a, index) in tags[tag]" :key="index" @click="routeTo(`/mind/article/${a.id}`)">
      <div class="img">
        <img src="@/assets/img/vector.svg" />
      </div>
      <span class="title">{{ a.title }}</span>
      <span class="base_name">{{ a.base_name }}</span>
    </div>
  </div>
</div>
</template>

<script>
import { mapActions, mapMutations, mapState } from 'vuex'

export default {
  name: 'Tags',

  data() {
    return {
      tags: {}
    }
  },

  mounted() {
    this.getTags()
  },

  computed: {
    ...mapState(['server', 'auth_headers', 'articles', 'articles_search']),

    filtered_articles() {
      if (this.articles_search.length) {
        return this.articles.filter((a) => a.title.includes(this.articles_search))
      }
      return this.articles
    }
  },

  methods: {
    ...mapMutations(['routeTo']),

    getTags() {
      this.$axios.get(`${this.server}articles/tags_articles/`,
        {headers: this.auth_headers})
        .then((response) => {
          this.tags = response.data
        })
    }
  }
}
</script>

<style lang="sass" scoped>
@import "@/assets/sass/style.sass"
</style>