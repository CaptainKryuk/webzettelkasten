<template>
  <div class="article__icon" v-if="type === 'all'">
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
    <p :class="['a_title', article.title && !article.title.length ? 'no_title': '']" 
       @click="routeTo(`/mind/article/${article.id}`)">
       <span class="text">
         {{ article.title || "Добавьте название" }}
       </span>
       
       <span class="tag_list">
         <span v-for="(tag, index) in article.tags" :key="index" class="tag">
           <span class="pre_tag_block" :style="`background: ${tag.color}`"></span>
           <span>{{ tag.name }}</span>
         </span>
       </span>
    </p>
    <p class="a_data">{{ article.hm_modified }} · {{ article.hm_created }}</p>
  </div>

  <div class="article__icon">
    <div class="img">
      <!-- <img src="@/assets/img/more.svg" /> -->
      <dropdown-object icon="more" :is_icon="true" :options="[{name: 'Удалить', link: `/mind/${type === 'recent' ? 'recent' : 'articles'}/${article.id}/delete`}]"></dropdown-object>
    </div>
  </div>
</template>

<script>
import { mapMutations } from 'vuex'
export default {
  name: 'DetailArticleInList',

  props: ['article', 'type'],

  methods: {
    ...mapMutations(['routeTo'])
  }
}
</script>

<style lang="sass" scoped>
@import "@/assets/sass/style.sass"
</style>