<template>
  <h2>Оглавление</h2>

  <div class="ideas">

    <div class="ideas__draft">
      <div class="ideas__draft__detail" v-for="(idea, index) in draft_ideas" :key="index">
        <p class="title">Черновик</p>
        <img src="@/assets/img/close.svg" @click="openModal(index)" />
        <p class="name" @click="routeLink(`/minds/${idea.id}/update`)" v-if="idea.title.length">{{ idea.title }}</p>
        <p class="name absent" v-if="!idea.title.length" @click="routeLink(`/minds/${idea.id}/update`)">Заголовок отсутствует</p>
        <p class="date">{{ idea.created.split("T")[0] }}</p>
      </div>
    </div>

    <div class="ideas__completed">
      <div class="ideas__completed__detail" v-for="(idea, index) in completed_ideas" :key="index">
        <p class="title" @click="routeLink(`/minds/${idea.id}/`)">{{ idea.title }}</p>
        <p class="base_name">{{ idea.base_name }}</p>
        <p class="text">{{ idea.text }}</p>
        <div class="tags">
          <ul>
            <li v-for="(tag, index) in idea.tags" :key="index" :style="`background: ${tag.color}`">
              {{ tag.name }}
            </li>
          </ul>
        </div>
        <div class="buttons">
          <img src="@/assets/img/edit.svg" @click="routeLink(`/minds/${idea.id}/`)" />
          <img src="@/assets/img/delete.svg" @click="openModal(index + draft_ideas.length)" />
        </div>
      </div>
    </div>
  </div>

  <modal-window title="Удаление идею"
                description="Вы уверены, что хотите удалить идею?"
                button_name="Удалить"
                :show="show_modal"
                @close="show_modal = false"
                @submit="deleteIdea()"></modal-window>
</template>

<script>
import axios from 'axios'
import { mapActions, mapMutations, mapState } from 'vuex'
import marked from 'marked'

export default {
  name: "Home",

  data() {
    return {
      ideas: [],

      show_modal: false,
      idea_index: 0
    }
  },

  mounted() {
    this.getIdeas()
  },

  computed: {
    ...mapState(['server']),

    draft_ideas() {
      return this.ideas.filter((idea) => idea.status === 'draft')
    },

    completed_ideas() {
      return this.ideas.filter((idea) => idea.status === 'completed')
    },
  },

  methods: {
    ...mapMutations(['routeLink']),

    deleteIdea() {
      this.$store.dispatch('deleteIdea', this.ideas[this.idea_index].id)
        .then((response) => {
          this.show_modal = false
          this.ideas.splice([this.idea_index], 1)
        })
    },

    getMarkdownText(text) {
      return marked(text)
    },

    openModal(index) {
      this.show_modal = true
      this.idea_index = index
    },

    getIdeas() {
      axios.get(`${this.server}idea/`)
        .then((response) => {
          this.ideas = response.data
        })
    }
  }
}
</script>

<style lang="sass" scoped>
@import "@/assets/sass/style.sass"
</style>