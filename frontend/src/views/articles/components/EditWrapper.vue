k<template>
  <div class="edit_article_block">
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
                  @input="mixin_autoResize_resize" 
                  placeholder="Придумайте название"
                  @keydown.enter.exact.prevent="endEditTitle()"
                  @keydown.down="endEditTitle()"
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

export default {
  name: 'EditWrapper',

  mixins: [mixinAutoResize],

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
  },

  mounted() {
    document.execCommand('defaultParagraphSeparator', false, 'p')
  },

  methods: {

    focusOnBlock(type='last') {
      let input_blocks = document.querySelectorAll('.block_input')
      if (type === 'last') {
        input_blocks[input_blocks.length - 1].focus()
      } else {
        input_blocks[0].focus()
      }
    },
    
    onInput(event) {
      const turndown = new TurndownService({
        emDelimiter: '_',
        linkStyle: 'inlined',
        headingStyle: 'atx'
      })
      this.$emit('input', turndown.turndown(event.target.innerHTML))
    },


    endEditTitle() {
      this.focusOnBlock('first')
    },
  }
}
</script>

<style lang="sass" scoped>
@import "@/assets/sass/style.sass"
</style>