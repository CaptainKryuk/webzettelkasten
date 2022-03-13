<template>

  <textarea rows="1"
            :placeholder="getBlockPlaceholder()"
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
            class="code_textarea">
            </textarea>


  <div class="row_numbered">
    <span class="number" v-for="(number, index) in line_numbers" :key="index">{{ number }}</span>
  </div>

  <div class="code_lang">
    <img :src="`/static/img/${block.code_lang}.svg`" @click="show_langs = true" />

    <div class="lang_lists">
      
      <div v-for="(lang, index) in langs" :key="index" @click="$emit('change_lang', lang)" >
        <img :src="`/static/img/${lang}.svg`" v-if="lang !== block.code_lang" />
      </div>
    </div>

  </div>
</template>

<script>
import mixinAutoResize from '@/global/mixins/autoResize.js';
import inputComponentsMixin from '../mixins/InputComponentsMixin.vue'
import { mapState } from 'vuex';

export default {
  name: "code-com",

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
    'change_lang'
  ],

  data() {
    return {
      show_langs: false,

      langs: ['python', 'sql', 'js', 'vuejs'],
    }
  },

  computed: {
    ...mapState(['article']),

    line_numbers() {
      return this.block.inner_text.split(/\r*\n/).length
    },
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
    },

    closeLangs() {
      this.show_langs = false
    },
  }
}
</script>