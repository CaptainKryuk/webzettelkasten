<template>
  <div :id="`input_${id_number}`"
       class="textarea img_textarea">

    <label v-if="block.images && !block.images.length" class="file_label">
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
                @keydown.enter.exact="$emit('keydown_enter_exact', $event)"
                @keydown.enter.shift="$emit('keydown_enter_shift', $event)"
                @keydown.enter.ctrl="$emit('keydown_enter_ctrl', $event)"
                @keydown.backspace="$emit('keydown_backspace', $event)"
                @keydown.up="$emit('keydown_up', $event)"
                @keydown.down="$emit('keydown_down', $event)"></textarea>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
  name: "img-mixin",
  props: ['id_number', 'block', 'index'],
  emits: ['update',
          'keydown_enter_exact', 
          'keydown_enter_shift', 
          'keydown_enter_ctrl',
          'keydown_backspace', 
          'keydown_up', 
          'keydown_down',
          'focus',
          'blur',],

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
      console.log('focus')
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
      document.querySelector(`#input_${this.id_number}`).querySelector('textarea').focus()
      this.is_focussed = true
    }

  }
}
</script>

<style lang="sass" scoped>
@import "@/assets/sass/style.sass"
</style>