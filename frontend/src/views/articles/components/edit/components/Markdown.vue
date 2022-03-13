<template>

  <textarea rows="1"
            :placeholder="getBlockPlaceholder()"
            @input="textInput"
            :value="modelValue"
            @keydown.tab.exact="addTabSpace"
            @keydown.enter.shift="createBlock($event)"
            @keydown.enter.ctrl="createBlock($event)"
            @keydown.backspace="handleInput"
            @focus="markdownFocus"
            @blur="markdownBlur"
            @keydown.up="handleInput"
            @keydown.down="handleInput"
            @click="focusOnInput"
            ref="input"
            :id="`input_${random_number}`"
            class="markdown_textarea"
            v-show="is_focus">
            </textarea>

  <div class="textarea markdown_result"
       v-if="!is_focus"
       @click="makeInputFocus()">

       <Markdown :source="block.inner_text"></Markdown>
  </div>
</template>

<script>
import mixinAutoResize from '@/global/mixins/autoResize.js';
import inputComponentsMixin from '../mixins/InputComponentsMixin.vue'
import { mapState } from 'vuex'
import Markdown from 'vue3-markdown-it';

export default {
  name: 'markdown-com',

  mixins: [
    mixinAutoResize,
    inputComponentsMixin
  ],

  components: {
    Markdown
  },

  props: {
    'modelValue': String,
    'block': Object,
    'index': Number,
    'random_number': String | Number,
    'is_open_menu': Boolean,
  },

  emits: [
    'update:modelValue',
    'change_input_focus',
  ],

  data() {
    return {
      is_focus: false,
      test: '# Markdown'
    }
  },

  computed: {
    ...mapState(['article']),
  },

  methods: {
    getBlockPlaceholder() {
      return this.index === this.article.blocks.length - 1 && this.block.block_type === 'text' ? 'Введите "/" для вызова меню' : ''
    },

    markdownFocus(e) {
      this.is_focus = true
      this.$emit('change_input_focus', true)
      this.mixin_autoResize_resize(e)
    },

    markdownBlur(e) {
      this.is_focus = false
      this.$emit('change_input_focus', false)
    },

    makeInputFocus() {
      let input = this.$refs.input
      input.focus()
      this.is_focus = true
      input.selectionStart = 9999

      setTimeout(() => {
        input.style.height = 'auto'
        input.style.height = `${input.scrollHeight}px`
      })
    }


  }
}
</script>