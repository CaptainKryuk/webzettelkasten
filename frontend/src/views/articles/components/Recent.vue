<template>

<div class="articles__detail not_move" v-for="(article, index) in filtered_articles" :key="index">
  <detail-article :article="article" type="recent"></detail-article>
</div>

<router-view></router-view>

</template>

<script>
import { mapActions, mapMutations, mapState } from 'vuex'
import DetailArticleInList from './DetailArticleInList'

export default {
  name: 'Recent',

  components: {
    'detail-article': DetailArticleInList
  },

  mounted() {
    this.getArticles()
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
    ...mapActions(['getArticles']),
    ...mapMutations(['routeTo']),
  }
}
</script>

<style lang="sass" scoped>
@import "@/assets/sass/style.sass"
</style>