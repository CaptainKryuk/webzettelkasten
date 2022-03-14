<template>
  <div v-html="modelValue" 
       :value="modelValue"
       v-once
       contenteditable
       class="textarea"
       :id="`input_${random_number}`"
       ref="input"
       @input="handleTextInput"
       @keydown.enter.exact="handleInput"
       @keydown.enter.shift="createBlock($event)"
       @keydown.enter.ctrl="createBlock($event)"
       @keydown.backspace="handleInput"
       @keydown.up="handleInput"
       @keydown.down="handleInput"
       @focus="$emit('change_input_focus', true)"
       @blur="$emit('change_input_focus', false)"
       ></div>
</template>

<script>
import mixinAutoResize from "@/global/mixins/autoResize.js";
import inputComponentsMixin from '../mixins/InputComponentsMixin.vue'

export default {
  name: 'ListMixin',

  mixins: [
    mixinAutoResize,
    inputComponentsMixin,
  ],


  props: {
    'modelValue': String,
    'block': Object,
    'index': Number,
    'random_number': String | Number,
  },

  emits: [
    'update:modelValue',
    'change_input_focus'
  ],

  watch: {
    modelValue: {
      handler(newValue) {
        if (document.activeElement === document.querySelector(`#input_${this.random_number}`)) {
          return;
        }
        document.querySelector(`#input_${this.random_number}`).innerHTML = newValue
      }
    },

    random_number: {
      handler(newValue) {
        document.querySelector(`#input_0`).id = `input_${newValue}`
      }
    }
  },

  methods: {
    handleTextInput(e) {
      this.mixin_autoResize_resize(e)
      this.$emit('update:modelValue', e.target.innerHTML)
    } 
  }

  
}
</script>