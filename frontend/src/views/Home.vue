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
          <img class="open_menu" src="@/assets/img/burger_menu.svg" />
          <button class="try_button" @click="routeTo('/registration')">Использовать бесплатно</button>
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

    <div class="fly_right_divider"></div>

    <!-- home content -->
    <div class="home__content">
      <div class="content__text">
        <p class="pretitle">To make things behave a little nicer</p>
        <p class="title">Webzettel - способ организации мыслей. <br/> Zettelkasten – это способ структурировать информацию, чтобы ей можно было пользоваться.</p>
        <p class="subtitle">
        Cуть концепции Зеттелькастен — обработка новой информации и связывание её между собой. В единую сеть. Как мозг. Brain. Network. World Wide Web.
        В очень общем приближении Зеттелькастен состоит из 2-х принципиальных шагов:<br/>
        1.Обработать информацию.<br/>
        2. Связать её с уже существующей информацией.<br/>
        Обработать — сформулировать содержание цитаты или идеи своими словами в противовес обычному копированию.
        Связать — найти общее с уже существующими в Зеттелькастене заметками. Попробуй и убедись насколько это удобно и продуктивно
        </p>
        <button class="try_button" @click="routeTo('/registration')">Попробовать бесплатно</button>
      </div>

      <div class="content__bottom">
        <div class="bottom_block">
          <div class="block_text">
            <p class="bottom_title">Ascendancy Classes</p>
            <p class="bottom_text">There are 19 Ascendancy classes, each with its own additional Ascendancy Skill Tree to master. </p>
            <p class="bottom_date">24 January 2020</p>
          </div>
        </div>
      </div>
    </div>


  </div>
</transition>

</template>

<script>
import { mapMutations } from 'vuex'

export default {
  name: 'Home',

  data() {
    return {
      show: false
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
