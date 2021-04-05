<template>
<section>
  <div v-click-outside="closeDropdown" class="dropdown-object">
    <img :src="`/static/img/${icon}.svg`" 
         v-if="is_icon"
         class="icon" 
         @click="show_fold = true"  />

    <p class="dropdown-object__title" v-if="is_text" @click="show_fold = true">
      {{ title }}
      <span><img :src="`/static/img/arrow-${show_fold ? 'up': 'down'}.svg`" /></span>
    </p>

    <div v-if="custom" @click="show_fold = true">
      <slot></slot>
    </div>

    <div v-if="show_fold" class="fold">
      <div class="option" v-for="(option, index) in options" :key="index" @click="routeLink(option.link)">
        <p class="option__text">{{ option.name }}</p>
      </div>
    </div>
  </div>
</section>
</template>

<script>``
export default {
  name: 'dropdown-object', 

  props: {
    'icon': String,
    'is_icon': {
      type: Boolean,
      default: false
    },
    'is_text': {
      type: Boolean,
      default: false
    },
    'title': String,
    'options': Array,
    // if custom create custom
    'custom': {
      type: Boolean,
      default: false
    }
  },

  data() {
    return {
      show_fold: false
    }
  },

  methods: {
    closeDropdown() {
      this.show_fold = false
    },

    routeLink(link) {
      this.$router.push(link)
      this.show_fold = false
    }
  }
}
</script>

<style scoped lang="sass">
@import "@/assets/sass/style.sass"
</style>