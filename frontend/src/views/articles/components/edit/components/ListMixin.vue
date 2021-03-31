<template>
  <div v-html="modelValue" 
       :value="modelValue"
       v-once
       contenteditable
       class="textarea"
       :id="`input_${id_number}`"
       @input="handleInput"
       @keydown.enter.exact="$emit('keydown_enter_exact', $event)"
       @keydown.enter.shift="$emit('keydown_enter_shift', $event)"
       @keydown.enter.ctrl="$emit('keydown_enter_ctrl', $event)"
       @keydown.backspace="$emit('keydown_backspace', $event)"
       @keydown.up="$emit('keydown_up', $event)"
       @keydown.down="$emit('keydown_down', $event)"
       @focus="$emit('focus')"
       @blur="$emit('blur')"
       ></div>
</template>

<script>
import mixinAutoResize from "@/global/mixins/autoResize.js";

export default {
  name: 'ListMixin',

  mixins: [mixinAutoResize],
  props: ['modelValue', 'id_number'],
  emits: ['keydown_enter_exact', 
          'keydown_enter_shift', 
          'keydown_enter_ctrl',
          'keydown_backspace', 
          'keydown_up', 
          'keydown_down',
          'focus',
          'blur',
          'update:modelValue'],

  watch: {
    modelValue: {
      handler(newValue) {
        if (document.activeElement === document.querySelector(`#input_${this.id_number}`)) {
          return;
        }
        document.querySelector(`#input_${this.id_number}`).innerHTML = newValue
      }
    },

    id_number: {
      handler(newValue) {
        document.querySelector(`#input_0`).id = `input_${newValue}`
      }
    }
  },

  methods: {
    handleInput(e) {
      this.mixin_autoResize_resize(e)
      this.$emit('update:modelValue', e.target.innerHTML)
    }
  }

  
}
</script>

<style lang="sass" scoped>
@import "@/assets/sass/style.sass"
</style>