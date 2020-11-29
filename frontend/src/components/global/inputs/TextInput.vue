<template>
  <section>
    <div class="input" :style="`width: ${width && width.length ? width : '100%'}`">
      <label for="input">
        <p class="input__name" v-if="field_name">{{ field_name }} <span style="color: red" v-if="required">*</span></p>

        <p class="error" v-if="error">{{ error }}</p>

        <div class="input__textinput">
          <img v-if="icon" :src="icon">
          <input type="text"
                :value="modelValue"
                class="inside_input"
                id="input"
                @input="$emit('update:modelValue', $event.target.value)" 
                :required="required"
                :placeholder="placeholder" />
        </div>
        <small class="hint">{{ hint }}</small>
      </label>

    </div>
  </section>
</template>

<script>
export default {
	name: 'textinput',

  props: {
    "modelValue": String,
    "field_name": String,
    "width": String,
    "placeholder": String,
    'icon': String,
    'hint': String,
    'required': Boolean,
    'error': String
  },

  methods: {
  }
}
</script>

<style lang="sass" scoped>
@import "@/assets/sass/style.sass"
</style>