c<template>

<div class="articles__detail" v-for="(article, index) in articles" :key="index">
  <div class="article__icon move">
    <div class="img">
      <img src="@/assets/img/move.svg" />
    </div>
  </div>

  <div class="article__icon">
    <div class="img">
      <img src="@/assets/img/book.svg" />
    </div>
  </div>

  <div class="article__content">
    <p class="a_title" @click="routeTo(`/mind/article/${article.id}`)">{{ article.title || 'blank' }}</p>
    <p class="a_data">{{ article.base_name }}</p>
  </div>

  <div class="article__icon">
    <div class="img">
      <!-- <img src="@/assets/img/more.svg" /> -->
      <dropdown-object icon="more" :is_icon="true" :options="[{name: 'Удалить', link: `/mind/recent/${article.id}/delete`}]"></dropdown-object>
    </div>
  </div>
</div>

<router-view></router-view>

</template>

<script>
import { mapActions, mapMutations, mapState } from 'vuex'
export default {
  name: 'Recent',

  mounted() {
    this.getArticles()
  },

  computed: {
    ...mapState(['server', 'auth_headers', 'articles'])
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