<template>
  <div class="menu">
    <h1 class="logo"><router-link to="/">WEBZETTEL</router-link></h1>

    <ul class="desktop__menu__list">
      <li class="list_item">Заметки</li>
      <li class="list_item">Тэги</li>
      <li class="list_item">Новая заметка</li>
    </ul>

    <div class="drop_menu" v-click-outside="closeMenu">
      <img src="@/assets/img/burger_menu.svg" @click="show_menu = !show_menu" />

      <transition name="menu-slide">
        <div class="drop_menu__wrapper" v-if="show_menu">
          <ul class="menu__list">
            <li class="list_item" @click="routeTo('/minds')">Заметки</li>
            <li class="list_item" @click="routeTo('/tags')">Теги</li>
            <li class="list_item" @click="routeTo('/minds/new')">Новая заметка</li>
          </ul>
        </div>
      </transition>

    </div>
  </div>

  <div class="content">
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: "HomeWrapper", 

  data() {
    return {
      show_menu: false,
    }
  },

  methods: {
    closeMenu() {
      this.show_menu = false
    },

    routeTo(link) {
      this.$router.push(link)
      this.show_menu = false
    }
  }
}
</script>

<style lang="sass" scoped>
@import "@/assets/sass/style.sass"
</style>