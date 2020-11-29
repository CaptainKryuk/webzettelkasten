<template>
  <h2>Новая мысль</h2>

  <div class="spinner large" v-if="loading"></div>

  <form @submit.prevent="completeIdea()">
    <div class="add_idea" v-if="Object.keys(idea).length && !loading">
      <textinput v-model="idea.title" required field_name="Заголовок"></textinput>

      <taginput :created_values="idea.tags"
                value_param="name"
                :default_values="['programming', 'python', 'js', 'vuejs', 'django']"
                @updateList="idea.tags = $event.list"
                field_name="Теги"></taginput>

      <textareainput v-model="idea.text" required field_name="Текст"></textareainput>

      <button class="button" type="submit">Сохранить</button>
    </div>
  </form>


</template>

<script>
import axios from 'axios'
import { mapActions, mapState } from 'vuex'
import _ from 'lodash'

export default {
  name: 'UpdateIdea',

  data() {
    return {
      idea: {},
      loading: false,
    }
  },

  computed: {
    ...mapState(['server'])
  },

  watch: {
    idea: {
      handler() {
        this.debouncedUpdateIdea()
      },
      deep: true
    }
  },

  created() {
    this.debouncedUpdateIdea = _.debounce(this.updateIdea, 500);
  },

  mounted() {
    this.getIdea()
  },

  methods: {
    ...mapActions(['deleteIdea']),


    getIdea() {
      this.loading = true
      axios.get(`${this.server}idea/${this.$route.params.id}/`)
        .then((response) => {
          this.idea = response.data
          this.loading = false
        })
    },

    updateIdea() {
      axios.put(`${this.server}idea/${this.$route.params.id}/`,
        this.idea)
    },

    completeIdea() {
      this.idea.status = 'completed'
      axios.put(`${this.server}idea/${this.$route.params.id}/`,
        this.idea)
        .then((response) => {
          this.$router.push('/minds')
        })
    }
  }
}
</script>

<style lang="sass" scoped>
@import "@/assets/sass/style.sass"
</style>