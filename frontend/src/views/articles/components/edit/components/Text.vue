<template>
  <div class="textarea text_textare"
      onclick="test()"
       contenteditable="true"
       :value="test_value"
       v-html="test_value"
       v-once
       :id="`input_${random_number}`"
       @input="textInput"
       ref="input"
       @keydown.tab.exact="addTabSpace"
       @keydown.enter.exact="handleInput"
       @keydown.enter.shift="createBlock($event)"
       @keydown.enter.ctrl="createBlock($event)"
       @keydown.backspace="handleInput"
       @focus="$emit('change_input_focus', true)"
       @blur="$emit('change_input_focus', false)"
       @keydown.up="handleInput"
       @keydown.down="handleInput"
       @click="focusOnInput"></div>
</template>

<script>
import mixinAutoResize from '@/global/mixins/autoResize.js';
import inputComponentsMixin from '../mixins/InputComponentsMixin.vue'
import { mapState } from 'vuex';


function test() {
  console.log('test')
};

export default {
  name: "text-com",

  mixins: [
    mixinAutoResize,
    inputComponentsMixin
  ],

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
      test_value: `hello <a href="/" onclick="document.location = 'https://google.com'" target="_blank">link</a> there`
      // test_value: 'hello <div contenteditable="false" style="display: inline-block;"><a href="/">link</a></div> there'
    }
  },

  computed: {
    ...mapState(['article']),
  },

  methods: {
    getBlockPlaceholder() {
      return this.index === this.article.blocks.length - 1 && this.block.block_type === 'text' ? 'Введите "/" для вызова меню' : ''
    },

    test() {
      console.log('click')
    },

    focusOnInput(e) {
      // * need for ios apple devices
      if (window.screen.width < 1200) {
        e.target.focus()
      }
    }
  }
}
</script>