<template>
<transition name="appear" appear>
  <div class="new_article">
    <!-- // * desktop menu sidebar -->
    <div class="new_article__sidebar desktop">
      <div class="sidebar_top">
        <div class="icon">
          <img src="@/assets/img/home.svg" />
        </div>
        <div class="icon">
          <img src="@/assets/img/close.svg" />
        </div>
      </div>

      <div v-for="(art, index) in articles" :key="index" class="sidebar_articles">
        <div class="article_link">
          <router-link :to="`/mind/article/${$route.params.id}`">{{ art.name }}</router-link>
        </div>
      </div>
    </div>

    <!-- //* mobile floating menu -->
    <transition name="appear" appear>
      <div class="shadow_wrapper" @click="show_menu = false" v-if="show_menu" ></div>
    </transition>

    <transition name="floating" appear>
      <div class="new_article__sidebar" v-if="show_menu">
        <div class="sidebar_top">
          <div class="icon" @click="routeTo('/')">
            <img src="@/assets/img/home.svg" />
          </div>
          <div class="icon" @click="show_menu = false">
            <img src="@/assets/img/close.svg" />
          </div>
        </div>

        <div v-for="(art, index) in articles" :key="index" class="sidebar_articles">
          <div class="article_link">
            <router-link :to="`/mind/article/${$route.params.id}`">{{ art.name }}</router-link>
          </div>
        </div>

        <div class="article_link selected" v-if="!articles.length">
          <div class="icon">
            <img src="@/assets/img/fire--gray.svg" />
          </div>
          <p class="text">Добавьте статьи</p>
        </div>
      </div>
    </transition>

    <!-- //* top menu -->
    <div class="new_article__menu">
      <div class="article_info">
        <div class="icon desktop">
          <img src="@/assets/img/arrow--left.svg"/>
        </div>
        <div class="icon desktop">
          <img src="@/assets/img/change_menu.svg"/>
        </div>

        <div class="icon">
          <img src="@/assets/img/burger_menu.svg"  @click="show_menu = true" />
        </div>
        <p :class="['article_name', !article.name ? 'blank_name' : '']">
          {{ article.name ? acticle.name : 'Введите название статьи' }}
        </p>
      </div>

      <div class="article_actions">
        <div class="icon action">
          <img src="@/assets/img/search.svg"/>
        </div>
        <div class="icon action">
          <img src="@/assets/img/plus.svg" />
        </div>
        <div class="user_avatar">
          <div class="avatar">
            <span class="avatar__username">{{ username[0].toUpperCase() }} </span>
          </div>
        </div>
      </div>
    </div>


    <!-- //* article content -->
    <div class="new_article__content">
      <edit-block></edit-block>
    </div>


  </div>
</transition>
</template>

<script>
import axios from 'axios'
import { mapActions, mapMutations, mapState } from 'vuex'
import EditWrapper from './EditWrapper'

export default {
  name: 'NewArticle',

  components: {
    'edit-block': EditWrapper
  },

  data() {
    EditWrapper
    return {
      article: {},
      show_menu: false
    }
  },

  computed: {
    ...mapState(['server', 'username', 'articles', 'id'])
  },

  mounted() {
    this.getArticle(this.$route.params.id)
  },

  methods: {
    ...mapMutations(['routeTo']),
    ...mapActions(['getArticle'])
  }
}
</script>

<style lang="sass" scoped>
@import "@/assets/sass/style.sass"
</style>
