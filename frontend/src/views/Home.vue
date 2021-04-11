<template>
<transition name="appear" appear>
  <div class="home" v-if="show">
    <!-- top meny -->
    <div class="home__top">
      <transition name="appear" appear>
        <div class="top__search" v-if="show">
          <div class="search_icon">
            <img src="@/assets/img/search.svg"/>
          </div>
        </div>
      </transition>


      <div class="top__title">
        <p class="pretitle">The</p>
        <p class="title">WEBZETTEL</p>
      </div>

      <div class="top__actions">
        <div class="action__button">
          <img class="open_menu" src="@/assets/img/burger_menu.svg" @click="open_menu = true" />
          <button class="try_button" @click="routeTo('/registration')" v-if="!authenticated && !loading">Использовать бесплатно</button>

          <dropdown-object :custom="true" 
                           :options="[{name: 'Аккаунт', link: `/mind/recent`},
                                      {name: 'Выйти', link: '/logout'}]"
                           v-if="authenticated && !loading && is_desktop"
                           style="max-width: 60px">
          <div class="user_avatar large">
            <div class="avatar">
              <span class="avatar__username">{{ username[0].toUpperCase() }} </span>
            </div>
          </div>
          </dropdown-object>

        </div>
      </div>
    </div>

    <div class="fly_top_divider"></div>

    <!-- sidebar meny -->
    <div class="home__sidebar">
      <ul class="sidebar__menu">
        <li><router-link to='/'>Главная</router-link></li>
        <li><a target="_blank" href="https://vonoiral.com/all/zettelkasten">Ознакомиться</a></li>
      </ul>
      <ul class="social__media">
        <li class="media__link"><img src="@/assets/img/facebook.svg" /></li>
        <li class="media__link"><img src="@/assets/img/facebook.svg" /></li>
        <li class="media__link"><img src="@/assets/img/facebook.svg" /></li>
      </ul>
    </div>

    <!-- home content -->
    <div class="home__content">
      <div class="content__text">
        <p class="pretitle">To make things behave a little nicer</p>
        <p class="title">Webzettel - способ организации мыслей. <br/> Zettelkasten – это способ структурировать информацию, чтобы ей можно было пользоваться.</p>
        <p class="subtitle">
        Суть концепции Зеттелькастен — обработка новой информации и связывание её между собой. В единую сеть. Как мозг. Brain. Network. World Wide Web.
        В очень общем приближении Зеттелькастен состоит из 2-х принципиальных шагов:<br/>
        1.Обработать информацию.<br/>
        2. Связать её с уже существующей информацией.<br/>
        Обработать — сформулировать содержание цитаты или идеи своими словами в противовес обычному копированию.
        Связать — найти общее с уже существующими в Зеттелькастене заметками. Попробуй и убедись насколько это удобно и продуктивно
        </p>
        <button class="try_button" @click="routeTo('/registration')">Попробовать бесплатно</button>
      </div>

      <div class="content__bottom">
        <div class="fly_right_divider"></div>
        <div class="bottom_block">
          <div class="block_text">
            <p class="bottom_title">Суть концепции Зеттелькастен</p>
            <p class="bottom_text">Обработка новой информации и связывание её между собой. В единую сеть.</p>
            <p class="bottom_date">20 March 2021</p>
          </div>
        </div>
      </div>
    </div>


  </div>
</transition>


<transition name="appear" appear>
  <div class="shadow_menu_wrapper" v-if="open_menu">
    <div class="close_icon" @click="open_menu = false">
      <img src="@/assets/img/close--white.svg"/>
    </div>
    <div class="shadow_menu">
      <router-link to="/login" v-if="!authenticated && !loading">Войти</router-link>
      <div class="menu_divider" v-if="!authenticated && !loading"></div>
      <router-link to="/registration" v-if="!authenticated && !loading">Зарегистрироваться</router-link>
      <div class="menu_divider" v-if="!authenticated && !loading"></div>
      <router-link to="/mind/recent" v-if="authenticated && !loading">Аккаунт</router-link>
      <div class="menu_divider" v-if="authenticated && !loading"></div>
      <a target="_blank" href="https://vonoiral.com/all/zettelkasten">Ознакомиться</a>
    </div>
  </div>
</transition>

</template>

<script>
import { mapMutations, mapState } from 'vuex'

export default {
  name: 'Home',

  data() {
    return {
      show: false,
      open_menu: false,
      loading: false,
      authenticated: false,
    }
  },

  computed: {
    ...mapState(['server', 'auth_headers', 'username']),

    is_desktop() {
      return window.screen.width > 1200 ? true : false
    }
  },

  mounted() {
    this.show = true
    this.getUser()
  },

  methods: {
    ...mapMutations(['routeTo']),

    getUser() {
      this.loading = true
      this.$axios.get(`${this.server}user/authentication/`,
        {headers: this.auth_headers})
        .then((response) => {
          this.loading = false
          this.authenticated = true
        })
        .catch((error) => {
          this.loading = false
        })
    }
  }
}
</script>


<style lang="sass" scoped>
@import "@/assets/sass/style.sass"
</style>
