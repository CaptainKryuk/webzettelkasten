<template>
<transition name="appear" appear>
  <div class="new_article" v-if="show">

    <!-- // * desktop menu -->
    <div class="new_article__sidebar desktop">
      <div class="sidebar_top">
        <div class="icon" @click="routeTo('/mind')">
          <img src="@/assets/img/home.svg" />
        </div>
        <div class="icon">
          <img src="@/assets/img/close.svg" />
        </div>
      </div>

      <div v-for="(art, index) in articles" :key="index" class="sidebar_articles">
        <div :class="['article_link', String(art.id) === String($route.params.id) ? 'selected' : '']" @click="goToArticle(art.id)">
          <p>{{ art.title || "Без названия" }}</p>
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
          <div class="icon" @click="routeTo('/mind')">
            <img src="@/assets/img/home.svg" />
          </div>
          <div class="icon" @click="show_menu = false">
            <img src="@/assets/img/close.svg" />
          </div>
        </div>

        <div v-for="(art, index) in articles" :key="index" class="sidebar_articles">
          <div :class="['article_link', String(art.id) === String($route.params.id) ? 'selected' : '']" @click="goToArticle(art.id)">
            <p>{{ art.title || "Без названия" }}</p>
          </div>
        </div>

        <div class="article_link selected" v-if="!articles.length" @click="createNewArticle()">
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
        <div class="icon desktop" @click="routeTo('/mind')">
          <img src="@/assets/img/arrow--left.svg"/>
        </div>
        <div class="icon desktop">
          <img src="@/assets/img/change_menu.svg"/>
        </div>

        <div class="icon mobile">
          <img src="@/assets/img/burger_menu.svg"  @click="show_menu = true" />
        </div>
        <p :class="['article_name', !article.title ? 'blank_name' : '']">
          {{ article.title && article.title.length ? article.title : 'Введите название статьи' }}
        </p>
      </div>

      <div class="article_actions">
        <div class="icon action">
          <img src="@/assets/img/search.svg"/>
        </div>
        <div class="icon action" @click="createNewArticle()">
          <img src="@/assets/img/plus.svg" />
        </div>
        <div class="avatar_wrapper">
          <dropdown-object :custom="true" :options="[{name: 'Выйти', link: `/logout`}]">
          <div class="user_avatar">
            <div class="avatar">
              <span class="avatar__username">{{ username[0].toUpperCase() }} </span>
            </div>
          </div>
          </dropdown-object>
        </div>

      </div>
    </div>


    <!-- //* article content -->
    <div class="new_article__content">
      <edit-wrapper></edit-wrapper>
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
    'edit-wrapper': EditWrapper
  },

  data() {
    EditWrapper
    return {
      show_menu: false,
      show: false
    }
  },

  watch: {
    'fullPath': {
      handler() {
        this.getArticle(this.$route.params.id)
      }
    }
  },

  computed: {
    ...mapState(['server', 'username', 'articles', 'id', 'article']),

    fullPath() {
      return this.$route.fullPath
    }
  },

  mounted() {
    this.show = true
    this.getArticle(this.$route.params.id)
    this.getArticles()
  },

  methods: {
    ...mapMutations(['routeTo']),
    ...mapActions(['getArticle', 'getArticles']),

    createNewArticle() {
      this.show_menu = false
      this.routeTo('/mind/new')
    },

    goToArticle(id) {
      this.show_menu = false
      this.routeTo(`/mind/article/${id}`)
    }
  }
}
</script>

<style lang="sass" scoped>
@import "@/assets/sass/style.sass"
</style>
