<template>
  <h2>Теги</h2>


  <div class="tags">
    <div class="tag" v-for="(tag, index) in tags_ideas" :key="index">
      <p class="tag__name"># {{ tag.name }}</p>

      <div class="tag__ideas">
        <div class="idea" v-for="(idea, index) in tag.ideas" :key="idea.id" @click="routeLink(`/minds/${idea.id}`)">
          <p class="idea__name">{{ idea.title }} <span class="base_name">({{ idea.base_name }})</span></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapMutations, mapState } from 'vuex'
import axios from 'axios'

export default {
  name: 'Tags',

  data() {
    return {
      tags_ideas: []
    }
  },

  computed: {
    ...mapState(['server'])
  },

  mounted() {
    this.getTagsIdeas()
  },

  methods: {
    ...mapMutations(['routeLink']),

    getTagsIdeas() {
      axios.get(`${this.server}idea/get_tags_ideas/`)
        .then((response) => {
          this.tags_ideas = response.data
        })
    }
  }
}
</script>

<style lang="sass" scoped>
@import "@/assets/sass/style.sass"
</style>