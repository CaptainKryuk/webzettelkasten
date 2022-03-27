<template>
  <div v-html="test_value" 
       :value="test_value"
       v-once
       contentEditable="false"
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
       @blur="$emit('change_input_focus', false)"></div>
</template>

<script>
import mixinAutoResize from "@/global/mixins/autoResize.js";
import inputComponentsMixin from '../mixins/InputComponentsMixin.vue'
import { mapState } from 'vuex';

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

  data() {
    return {
      test_value: 'Hello <a href="/">link</a>'
    }
  },

  computed: {
    ...mapState(['block_sizes'])
  },

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

  }

  
}
</script>