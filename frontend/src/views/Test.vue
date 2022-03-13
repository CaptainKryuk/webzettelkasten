<template>

    <Markdown :source="source" />

    <textarea @input="input" />
</template>

<script>
import Markdown from 'vue3-markdown-it';
import { mapState } from 'vuex';
import store from '../store'

export default {
  name: "Test",

  components: {
    Markdown
  },

  data() {
    return {
      source: '# Hello World!'
    }
  },

  computed: {
    ...mapState(['server'])
  },
  
  mounted() {
    console.log(this.server)
    console.log(store)
  },

  methods: {
    input(e) {
      e.preventDefault()
      e.stopPropagation()
      this.source += e.target.value
    }
  }
}
</script>