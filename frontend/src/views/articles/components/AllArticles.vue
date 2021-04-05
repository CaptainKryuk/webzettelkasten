<template>

<div class="all_list_articles">
  <div class="articles__detail" 
       v-for="(article, index) in articles" 
       :key="article.id" 
       :drag_index="article.order_number"
       :drag_id="article.id">
    <detail-article :article="article" type='all'></detail-article>
  </div>
</div>
<router-view></router-view>

</template>

<script>
import { mapActions, mapMutations, mapState } from 'vuex'
import DetailArticleInList from './DetailArticleInList'
import DragAndDropMixin from './edit/mixins/DragAndDropMixin'

export default {
  name: 'Recent',

  components: {
    'detail-article': DetailArticleInList
  },

  mixins: [DragAndDropMixin],

  mounted() {
    this.getArticles('all')
    setTimeout(() => {
      this.setupDragAndDrop('all_list_articles', 'articles__detail')
    }, 100)

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
    ...mapMutations(['routeTo', 'ASSIGN_ARTICLES']),

    updateMovedObject() {
      this.$axios.put(`${this.server}articles/${this.active_id}/`,
        {order_number: this.new_order_number},
        {headers: this.auth_headers})
        .then((response) => {
          this.getArticles('all')          
        })
    },
  }
}
</script>

<style lang="sass" scoped>
@import "@/assets/sass/style.sass"
</style>