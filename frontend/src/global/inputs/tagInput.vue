<template>
<section>
  <div class="input" :style="`width: ${width && width.length ? width : '100%'}`">
    <p class="input__name" v-if="field_name">{{ field_name }}</p>

    <p class="error" v-if="error">{{ error }}</p>

    <div class="input__taginput" v-click-outside="closeBoard">
      <!-- list of created objects -->

        <form @submit.prevent="addTag(new_tag_name)">
          <div class="form_input">
            <div class="tag_list created">
              <div v-for="(tag, index) in created_values" :key="index" class="tag_list__object">
                <p>{{ tag[value_param] || tag }}</p><img src="@/assets/img/close_gray.svg" @click="deleteTag(index)" />
              </div>

              <!-- new tag name input -->
              <input type="text" class='inside_input' v-model="new_tag_name" @focus="show_board = true" /> 
            </div>

          </div>
        </form>


      <!-- fold -->
      <div class="fold_board" v-if="show_board">
        <div class="tag_list">
          <div v-for="(tag, index) in default_values" :key="index" class="tag_list__object" @click="addTag(tag[value_param] || tag)">
            <p>{{ tag }}</p>
          </div>
        </div>

        <div class="fold_board__bottom">
          <div class="type">
            <p class="text">Создать</p>
            <div class="tag_list__object" v-if="new_tag_name.length">{{ new_tag_name }}</div>
          </div>
          <div class="text">Нажмите <img src="@/assets/img/enter-keyboard.svg" /></div>
        </div>
      </div>
    </div>

  </div>
</section>
</template>


<script>
export default {
  name: "taginput",

  /* example 
     <taginput :created_values="['programm' 'work']" 
               :default_values=['ux', 'ui'] 
               @updateList = new_idea.tags = "$event "
               field_name="Теги"></taginput>
  */

  props: {
    'field_name': String, // Теги
    'value_param': String, // created_values[0][value_param] 
    'created_values': Array, // ['Имя', 'Фамилия] / [{'name': 'Имя', 'id': 1}]
    'default_values': Array,
    'width': String,
    'error': String,

    // api settings
    'api': Boolean,
    'add_url': String,
    'delete_url': String
  },
  
  data() {
    return {
      new_tag_name: '',
      show_board: false,
    }
  },

  methods: {
    closeBoard() {
      this.show_board = false
    },

    addTag(name) {
      if (name) {
        this.$emit('updateList', {list: [...this.created_values, name], item: name})
        this.new_tag_name = ''
      }
    },

    deleteTag(index) {
      let new_list = this.created_values.slice()
      new_list.splice(index, 1)
      this.$emit('updateList', {list: new_list, item: this.created_values[index].name})
    }
  }
}
</script>

<style lang="sass" scoped>
@import "@/assets/sass/style.sass"
</style>