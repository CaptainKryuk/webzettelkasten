<template>
<transition name="appear" appear>
  <div :class="['edit_article_block', no_content ? 'no_content': '']" 
       v-if="!article_loading && Object.keys(article).length">
    
    <!-- <textarea v-model="test"></textarea> -->
    <div class="block_title">

      <!-- // * add tag -->
      <tag-list :article="article" @updateTags="article.tags = $event"></tag-list>

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
                  @focus="is_title_focussed = true"
                  @blur="is_title_focussed = false"
                  rows="1" />
      </div>

    </div>

    <div class="article_blocks">
      <editor v-for="(block, index) in article.blocks" 
              :key="block.id" 
              :block="block" 
              :index="index"
              :drag_index="block.order_number"
              :drag_id="block.id"
              class='detail_block_wrapper'></editor>
    </div>

    <!-- this label fit bottom of page and when click on this area last input in article blocks makes focussed  -->
    <label class="focus_label" @click="focusOnBlock()"> </label>


  </div>
</transition>
</template>

<script>
import { mapState } from 'vuex'
import mixinAutoResize from "@/global/mixins/autoResize.js"
import EditBlock from './edit/EditBlock'
import ListFunctionsMixinVue from './edit/mixins/ListFunctionsMixin.vue'
import TagList from './TagList'
import DragAndDropMixin from './edit/mixins/DragAndDropMixin'

export default {
  name: 'EditWrapper',

  mixins: [mixinAutoResize, ListFunctionsMixinVue, DragAndDropMixin],

  components: {
    'editor': EditBlock,
    'tag-list': TagList
  },

  data() {
    return {
      selected_block: null,
      is_title_focussed: false,
      test: ''
    }
  },

  watch: {
    'article.title': {
      handler() {
        this.debouncedUpdateArticle()
      }
    },

    'fullPath': {
      handler() {
        this.setupTitle()
      }
    }
  },

  computed: {
    ...mapState(['server', 'auth_headers', 'article', 'article_loading']),

    no_content() {
      if ((this.article.title && this.article.title.length) 
          || (this.article.blocks && this.article.blocks[0].inner_text && this.article.blocks[0].inner_text.length)
          || (this.article.blocks && this.article.blocks.length > 1)) {
          return false
      }
      return true
    },

    fullPath() {
      return this.$route.fullPath
    }

  },

  created() {
    this.debouncedUpdateArticle = _.debounce(this.updateArticle, 500)
  },

  mounted() {
    this.setupTitle()
    setTimeout(() => {
      this.setupDragAndDrop('article_blocks', 'detail_block')
    }, 300)
    
  },

  methods: {
    setupTitle() {
      setTimeout(() => {
        let input = this.$refs.title_input
        if (input) {
          input.style.height = 'auto'
          input.style.height = `${input.scrollHeight}px`
        }
      }, 200)
    },

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
            textarea.focus()
          }
        }
      }
    },

    updateArticle() {
      this.$axios.put(`${this.server}articles/${this.$route.params.id}/`,
        this.article,
        {headers: this.auth_headers})
    },

    updateMovedObject() {
      this.$axios.put(`${this.server}block/${this.active_id}/`,
        {order_number: this.new_order_number},
        {headers: this.auth_headers})
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