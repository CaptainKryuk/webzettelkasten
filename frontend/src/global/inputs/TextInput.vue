<template>
  <section>
    <div class="input" :style="`width: ${width && width.length ? width : '100%'}`">
      <label :for="'input' + unique_id">
        <p class="input__name" v-if="field_name">{{ field_name }} <span style="color: red" v-if="required">*</span></p>

        <p class="error" v-if="error">{{ error }}</p>

        <div class="input__textinput">
          
          <input :type="type"
                :value="modelValue"
                class="inside_input"
                :id="'input' + unique_id"
                @input="$emit('update:modelValue', $event.target.value)" 
                :required="required"
                :placeholder="placeholder" />
          <img v-if="icon" :src="icon">
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
    'error': String,
    'type': {
      type: String,
      default: 'text'
    }
  },

  data() {
    return {
      unique_id: Math.random(),
    }
  },

  methods: {
  }
}
</script>

<style lang="sass" scoped>
@import "@/assets/sass/style.sass"
</style>