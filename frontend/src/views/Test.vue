<template>
message: {{ message }}
<div v-html="message" 
     :value="message" 
     contenteditable=""
     ref="input"
     style="margin: 20px; outline: none"></div>


<contenteditable tag="b" 
                 :contenteditable="isEditable" 
                 v-model="re" 
                 :noNL="false" 
                 :noHTML="true" 
                 @returned="enterPressed" />
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
      isEditable: true,
      message: "<h1>Hello</h1>",
      result: ''
    }
  },

  computed: {
    ...mapState(['server'])
  },

  watch: {
    message: {
      handler() {
        let markdown = require('markdown-it')
        let md = new markdown()
        let result = md.render(this.message)
        this.message = result
      }
    }
  },
  
  mounted() {
  },

  methods: {
     enterPressed(){
       alert('Enter Pressed');
     },

    controlContent(e) {
      let markdown = require('markdown-it')
      let md = new markdown()
      let result = md.render(e.target.innerText)
      this.message = result
      setTimeout(() => {
        this.$refs.input.focus()
        this.$refs.input.selectionStart = 99999
        this.$refs.input.selectionEnd = 0
      }, 500)

    },

    input(e) {
      e.preventDefault()
      e.stopPropagation()
      this.source += e.target.value
    }
  }
}
</script>