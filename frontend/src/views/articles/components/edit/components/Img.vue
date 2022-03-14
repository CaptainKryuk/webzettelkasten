<template>
  <div :id="`input_${random_number}`"
       class="textarea img_textarea"
       ref="input">

    <label v-if="block.images && !block.images.length" 
           :class="['file_label', is_focussed ? 'focussed_label' : '']">
      Выберите картинку для загрузки
      <input type="file" id="file" ref="file" @change="uploadFile">
    </label>

    <div class="img_area" @click="selectImage">

      <img v-if="block.images && block.images[0]" 
           :src="`${media_server}${block.images[0].file}`" 
           :alt="block.images[0].filename"
           :class="[is_focussed ? 'focussed' : '']" />

      <textarea @focus="is_focussed = true"
                @blur="is_focussed = false"
                maxlength="1"
                @update="block.images = $event"
                @keydown.enter.exact="handleInput"
                @keydown.enter.shift="createBlock($event)"
                @keydown.enter.ctrl="createBlock($event)"
                @keydown.backspace="handleInput"
                @keydown.up="handleInput"
                @keydown.down="handleInput"></textarea>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import inputComponentsMixin from '../mixins/InputComponentsMixin.vue'

export default {
  name: "img-mixin",

  mixins: [inputComponentsMixin],

  props: {
    'random_number': String | Number, 
    'block': Object,
    'index': Number,

  },
  
  emits: ['update'],

  data() {
    return {
      file: '',
      is_focussed: false
    }
  },

  computed: {
    ...mapState(['server', 'media_server', 'auth_headers'])
  },

  methods: {
    focus(e) {
    },

    async uploadFile(e) {
      await this.handleFileUpload(e)
      await this.sendFileToServer()
    },

    async handleFileUpload(e) {
      return new Promise((resolve, reject) => {
        let handle_file = this.$refs.file.files[0]   
        // check that it's an image type
        if (handle_file.type.split('/')[0] === 'image') {
          this.file = handle_file
          resolve()
        } else {
          reject()
        }
      })
    },

    sendFileToServer() {
      return new Promise((resolve, reject) => {
        let formData = new FormData();
        formData.append('file', this.file)
        formData.append('filename', this.file.name)
        formData.append('filesize', this.file.size)
        formData.append('block', this.block.id)
        let headers = {
            'Content-Type': 'multipart/form-data',
            ...this.auth_headers
        }
        this.$axios.post(`${this.server}img/`,
                    formData,
                    {headers: headers})
          .then((response) => {
            this.$emit('update', [...this.block.images, response.data])
            this.$forceUpdate()
          })
      })
    },
    
    selectImage(e) {
      document.querySelector(`#input_${this.random_number}`).querySelector('textarea').focus()
      this.is_focussed = true
    }

  }
}
</script>

<style lang="sass" scoped>
@import "@/assets/sass/style.sass"
</style>