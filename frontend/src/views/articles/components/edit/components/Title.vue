<template>
  <textarea rows="1"
            placeholder="Заголовок"
            @input="textInput"
            :value="modelValue"
            @keydown.tab.exact="addTabSpace"
            @keydown.enter.exact="handleInput"
            @keydown.enter.shift="createBlock($event)"
            @keydown.enter.ctrl="createBlock($event)"
            @keydown.backspace="handleInput"
            @focus="$emit('change_input_focus', true)"
            @blur="$emit('change_input_focus', false)"
            @keydown.up="handleInput"
            @keydown.down="handleInput"
            @click="focusOnInput"
            ref="input"
            :id="`input_${random_number}`"
            class="title_textarea h1"
            style="height: 39px">
            </textarea>
</template>

<script>
import mixinAutoResize from '@/global/mixins/autoResize.js';
import inputComponentsMixin from '../mixins/InputComponentsMixin.vue'
import { mapState } from 'vuex';

export default {
  name: "title-com",

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

  computed: {
    ...mapState(['article']),
  },

  methods: {
    getBlockPlaceholder() {
      return this.index === this.article.blocks.length - 1 && this.block.block_type === 'text' ? 'Введите "/" для вызова меню' : ''
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