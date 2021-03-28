<template>
<transition name="appear" appear>
  <div class="articles" v-if="show">
    <div class="articles__top">
      <div class="top__text">
        <h1>Все статьи и мысли</h1>
        <img src="@/assets/img/plus.svg" @click="routeTo('/mind/new')" />
      </div>
      <div class="top__menu">
        <!-- desctop elements -->
        <div class="search_menu">
          <textinput v-model="search" placeholder="Поиск по заголовкам и тексту" icon="/static/img/search.svg"  />
        </div>

        <!-- user icon -->

        <!-- mobile button -->
        <div class="menu_icon">
          <img src="@/assets/img/burger_menu.svg" @click="show_menu = true" />
        </div>

        <transition name="appear" appear>
          <div class="shadow_menu_wrapper" v-if="show_menu">
            <div class="close_icon" @click="show_menu = false">
              <img src="@/assets/img/close--white.svg"/>
            </div>
            <div class="shadow_menu">
              <router-link to="/">Главная</router-link>
              <div class="menu_divider"></div>
              <router-link to="/mind/new">Добавить мысль</router-link>
              <div class="menu_divider"></div>
              <router-link to="/logout">Выйти</router-link>
            </div>
          </div>
        </transition>


      </div>
    </div>


    <div class="articles__content">
      <div class="content__search">
        <textinput v-model="search" placeholder="Поиск по заголовкам и тексту" icon="/static/img/search.svg" />
      </div>


      <div class="pages_menu">
        <div v-for="(link, index) in links" :key="index" 
            :class="[$route.fullPath.includes(link.filter) ? 'selected' : '', 'menu__item']" @click="routeTo(link.url)">
          <p>{{ link.name }}</p>
        </div>
      </div>
    </div>
  </div>
</transition>

</template>

<script>
import { mapMutations } from 'vuex'
export default {
  name: 'ArticlesWrapper',

  data() {
    return {
      search: '',
      show_menu: false,
      show: false,
      links: [
        {filter: 'recent', url: '/mind/recent', name: 'Последнее'},
        {filter: 'articles', url: '/mind/articles', name: 'Все'},
        {filter: 'tags', url: '/mind/tags', name: 'Тэги'},
        {filter: 'links', url: '/mind/links', name: 'Ссылки'}
      ]
    }
  },

  mounted() {
    this.show = true
  },

  methods: {
    ...mapMutations(['routeTo'])
  }
  
}
</script>

<style lang="sass" scoped>
@import "@/assets/sass/style.sass"
</style>
