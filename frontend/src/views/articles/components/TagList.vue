<template>
<div class="tag_manage">
  <div class="tag_list" v-if="article.tags && article.tags.length">
    <div :class="['tag']" v-for="(tag, index) in article.tags" :key="index" @click="deleteTag(index)">
      <span class="pre_tag_block" :style="`background: ${tag.color}`"></span>
      {{ tag.name }}
    </div>

    <img src="@/assets/img/plus.svg" @click="openMenu()" />
  </div>

  <div class="add_tag_block" @click="openMenu()" v-if="!show_add && article.tags && !article.tags.length">
    <div class="icon">
      <img src="@/assets/img/plus.svg" />
    </div>
    <p class="text">Добавить тэг</p>
  </div>


  <!-- input -->
  <div v-if="show_add" class="tag_input" v-click-outside="closeMenu">
    <form @submit.prevent="addTag()">
      <input v-model="new_tag.name"
            ref="tag_input" 
            @focus="show_menu = true"   />
    </form>


    <transition name="appear" appear>
      <div class="fold_tags" v-if="show_menu">
        <div v-for="(tag, index) in default_tags" :key="index" class="default_tag" @click="addTag(tag)">
          <span class="pre_tag_block" :style="`background: ${tag.color}`"></span>
          <p>{{ tag.name }}</p>
        </div>
      </div>
    </transition>

  </div>
</div>

</template>

<script>
import { mapState } from 'vuex'
export default {
  name: 'TagList',

  data() {
    return {
      show_add: false,
      show_menu: false,

      new_tag: {
        name: '',
        color: ''
      },

      default_tags: [{name: 'Programming', color: '#27AE60'}, {name: 'Python', color: '#EB5757'}, {name: 'JS', color: '#2D9CDB'}]
    }
  },

  props: ['article'],

  computed: {
    ...mapState(['server', 'auth_headers', ])
  },

  methods: {
    openMenu() {
      this.show_add = true
      setTimeout(() => {
        this.$refs.tag_input.focus()
      })
    },

    addTag(tag) {
      this.$axios.post(`${this.server}articles/${this.$route.params.id}/add_tag/`,
        tag ? tag : this.new_tag,
        {headers: this.auth_headers})
        .then((response) => {
          this.new_tag.name = ''
          this.$emit('updateTags', [...response.data])
        })
    },

    deleteTag(index) {
      this.$axios.put(`${this.server}articles/${this.$route.params.id}/delete_tag/`,
        {name: this.article.tags[index].name},
        {headers: this.auth_headers})
        .then(() => {
          let new_tags = Object.assign(this.article.tags)
          new_tags.splice(index, 1)
          this.$emit('updateTags', new_tags)
          if (!new_tags.length) {
            this.show_add = false
          }
        })
    },

    closeMenu() {
      this.show_menu = false
      // this.show_add = false
    }
  }
}
</script>

<style lang="sass" scoped>
@import "@/assets/sass/style.sass"
</style>