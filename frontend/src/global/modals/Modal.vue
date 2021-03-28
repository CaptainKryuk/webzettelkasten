<template>
  <div class="modal" v-if="show">
    <div class="shadow" @click="$emit('close')"></div>
    <div class="modal__window">
      <img src="@/assets/img/close.svg" class="close_icon" @click="$emit('close')" />

      <h1>{{ title }}</h1>
      <p class="description">{{ description }}</p>

      <div class="buttons">
        <button class="transparent" @click="$emit('close')">Отменить</button>
        <button class="success" @click="$emit('submit')">{{ button_name }}</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'modal-window',
  
  /*
  <modal-window title="Удаление идеи"
                description="описание"
                button_name="удалить"
                :show="show_delete"
                @close="show_delete = false"
                @submit="deleteEnviroment()"></modal-window>
  */

  props: {
    title: String,
    description: String,
    button_name: String,
    show: Boolean
  },
  
  data() {
    return {

    }
  },

  mounted() {
  },

  methods: {
  }
}
</script>

<style scoped lang="sass">
@import "@/assets/sass/style.sass"
</style>