k<template>
  <div :class="['edit_article_block', no_content ? 'no_content': '']">
    <div class="block_title">

      <!-- // * add tag -->
      <div class="add_tag_block">
        <div class="icon">
          <img src="@/assets/img/plus.svg" />
        </div>
        <p class="text">Добавить тэг</p>
      </div>

      <!-- // * change title -->
      <div class="title_input">
        <textarea v-model="article.title" 
                  ref='title_input'
                  @input="mixin_autoResize_resize" 
                  placeholder="Придумайте название"
                  @keydown.enter.exact.prevent="endEditTitle"
                  @keydown.enter.ctrl.prevent="endEditTitle"
                  @keydown.enter.shift.prevent="endEditTitle"
                  @keydown.down="endEditTitle"
                  rows="1" />
      </div>

    </div>

    <div class="article_blocks">
      <editor v-for="(block, index) in article.blocks" :key="block.id" :block="block" :index="index"></editor>
    </div>

    <!-- this label fit bottom of page and when click on this area last input in article blocks makes focussed  -->
    <label class="focus_label" @click="focusOnBlock()"> </label>


  </div>
</template>

<script>
import { mapState } from 'vuex'
import mixinAutoResize from "@/global/mixins/autoResize.js"
import EditBlock from './edit/EditBlock'
import ListFunctionsMixinVue from './edit/mixins/ListFunctionsMixin.vue'

export default {
  name: 'EditWrapper',

  mixins: [mixinAutoResize, ListFunctionsMixinVue],

  components: {
    'editor': EditBlock
  },

  data() {
    return {
      selected_block: null,
    }
  },

  computed: {
    ...mapState(['server', 'article']),

    no_content() {
      if ((this.article.title && this.article.title.length) 
          || (this.article.blocks && this.article.blocks[0].inner_text && this.article.blocks[0].inner_text.length)
          || (this.article.blocks && this.article.blocks.length > 1)) {
        console.log(1)
        // if (this.article.title.length || this.article.blocks[0].inner_text.length ) {
          // console.log(2)
          return false
        // }
      }
      return true
    },
  },

  methods: {

    focusOnBlock(type='last') {
      let input_blocks = document.querySelectorAll('.block_input')
      if (type === 'last') {
        input_blocks[input_blocks.length - 1].focus()
      } else {
        let textarea;
        let is_div = false

        textarea = input_blocks[0].querySelector('textarea') 
        if (!textarea) {
          textarea = input_blocks[0].querySelector('.textarea')
          is_div = true
        }

        if (textarea) {
          if (is_div) {
            this.setListCaret(textarea, 'start')
          } else {
            textarea.selectionStart =  0
            textarea.selectionEnd = 0
            // textarea.selectionStart = this.$refs.title_input.selectionStart
            // textarea.selectionEnd = this.$refs.title_input.selectionStart
            textarea.focus()
          }
        }
      }
    },


    endEditTitle(e) {
      e.preventDefault()
      this.focusOnBlock('first')
    },
  }
}
</script>

<style lang="sass" scoped>
@import "@/assets/sass/style.sass"
</style>