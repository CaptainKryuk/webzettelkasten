<template>
  <div class="detail_block">
    <div class="detail_block__icon">
      <img src="@/assets/img/move.svg" />
    </div>

    <!-- editor -->
    <label class="block_input" :for="`input_${random_number}`">
      <textarea :id="`input_${random_number}`"
                :ref="`input_${random_number}`"
                v-model="block.inner_text"
                rows="1"
                @input="mixin_autoResize_resize"
                @keydown.enter.shift="handleInput"
                @keydown.enter.ctrl="handleInput"
                @keydown.backspace="handleInput"
                @keydown.up="handleInput"
                @keydown.down="handleInput"></textarea>
    </label>

    <div class="detail_block__icon">
      <img src="@/assets/img/more.svg" />
    </div>

    <transition name="appear" appear>
      <div class="popup_menu" v-if="is_open_menu">
        <div v-for="(item, index) in popup_menu" :key="index" :class="['popup_menu__item', item.active ? 'active' : '']">
          <div class="icon">
            <div class="item_avatar">
              <img :src="`/static/img/${item.icon}.svg`" />
            </div>
          </div>

          <p class="tag">{{ item.tag }}</p>

          <p class="name">{{ item.name }}</p>
        </div>
      </div>
    </transition>

  </div>
</template>

<script>
import mixinAutoResize from "@/global/mixins/autoResize.js";
import _ from 'lodash';
import axios from 'axios'
import { mapMutations, mapState } from 'vuex';

export default {
  name: 'EditBlock',

  props: ['block', 'index'],

  mixins: [mixinAutoResize],

  data() {
    return {
      random_number: 0,

      popup_menu: [
        {icon: 'h', tag: '/header', name: 'Заголовок', active: true},
        {icon: 'pic', tag: '/img', name: 'Изображение', active: false},
        {icon: 'code', tag: '/code', name: 'Код', active: false},
        {icon: 'list', tag: '/list', name: 'Список', active: false},
      ]
    }
  },

  computed: {
    ...mapState(['server', 'auth_headers', 'article']),

    is_textarea_focus() {
      let textarea = this.$refs[`input_${this.random_number}`]
      return textarea === document.activeElement
    },

    is_open_menu() {
      return this.block.inner_text.match(/^\/$/) && this.is_textarea_focus
    }
  },

  watch: {
    'block.inner_text': {
      handler() {
        this.debouncedUpdateBlock()
      }
    }
  },

  created() {
    this.debouncedUpdateBlock = _.debounce(this.updateBlock, 500)
  },

  mounted() {
    this.random_number = Math.random()
    this.setupTextarea()
  },


  methods: {
    ...mapMutations(['ADD_NEW_BLOCK', 'DELETE_BLOCK',]),

    setupTextarea() {
      /* 
      * after page reloading need to install valid height
      */ 
      setTimeout(() => {
        let textarea = this.$refs[`input_${this.random_number}`]
        if (this.block.inner_text && this.block.inner_text.length) {
          textarea.style.height = textarea.scrollHeight + 'px'
        } else {
          textarea.style.height = '36px'
        }
      })
    },


    handleInput(e) {
      /*
      * if user click on: 
      *   Shift/Ctrl + Enter -> create new block
      *   Backspace and block.inner_text is blank -> delete this block and focus on previous 
      *   Arrows up and down -> go over blocks
      */
      if (e.key === 'Enter') {
        // * enter
        e.preventDefault()
        this.createBlock()
      } 

      else if (e.key === 'Backspace') {
        // * backspace
        let blank_string = this.block.inner_text.replace(/\s/g, '')
        let textarea = this.$refs[`input_${this.random_number}`]
        if (textarea.selectionStart === 0) {
          if (!blank_string.length) {
            // * when block is already blank -> delete if
            this.deleteBlock()
          } else {
            // * if we have content in this block go to previous
            this.focusOnBlock('previous', true)
          }
        }
      } 

      else if (e.key === 'ArrowUp' || e.key === 'ArrowDown') {
        // * arrows
        if (this.is_open_menu) {
          // * when menu is opened need to go over items in this menu
          e.preventDefault()
          this.goOverPopupMenu(e.key)
        } else {
          let textarea = this.$refs[`input_${this.random_number}`]
          let splitted_text = this.block.inner_text.split(/\r*\n/)

          if (e.key === 'ArrowUp') {
            if (splitted_text[0].length >= textarea.selectionStart) {
              e.preventDefault()
              this.focusOnBlock('previous', true)
            }
          } else if (e.key === 'ArrowDown') {
            if (textarea.selectionStart >= this.block.inner_text.length - splitted_text[splitted_text.length - 1].length
                || this.block.inner_text.length === 0) {
              e.preventDefault()

              if (this.index < this.article.blocks.length - 1) {
                this.focusOnBlock('next', true)
              }
            }
          }
        }    
      }
    },

    createBlock() {
      /*
      * if we call "Shift + Enter" from last block -> just add new to the end of block list
      * if we call from block from center -> add it after passed index
      */
     let data = {
       article: this.$route.params.id
     }
     let cur_index = this.getBlockIndex(this.block.id)
     if (cur_index !== Number(this.article.blocks.length) - 1) {
       data['order_number'] = this.block.order_number + 1
     }

      axios.post(`${this.server}block/`,
        data,
        {headers: this.auth_headers})
        .then((response) => {
          this.ADD_NEW_BLOCK({data: response.data, index: cur_index})
          setTimeout(() => {
            this.focusOnBlock('next')
          })
        })
    },

    deleteBlock() {
      /*
      * check that block is not last and 
      * delete current block and focus on previous 
      * if block is last -> don't delete it and focus on title
      */
      if (this.article.blocks.length > 1) {
        axios.delete(`${this.server}block/${this.block.id}/`,
          {headers: this.auth_headers})
          .then((response) => {
            this.focusOnBlock()
            this.DELETE_BLOCK(this.block.id)
          })
      } else {
        this.focusOnTitle()
      }

    },

    focusOnBlock(type='previous', to_start=false) {
      let textarea = this.$refs[`input_${this.random_number}`]
      let parent;
      if (type === 'previous') {
        let index = this.getBlockIndex(this.block.id)
        if (index !== 0) {
          parent = textarea.parentElement.parentElement.previousSibling
        } else {
          this.focusOnTitle()
        }
      } else if (type === 'next') {
        parent = textarea.parentElement.parentElement.nextSibling
      }


      if (parent) {
        let found_input = parent.querySelector('textarea')
        if (found_input) {
          found_input.focus()

          if (type === 'previous') {
            found_input.selectionStart = 9999
          } else if (type === 'next') {
            found_input.selectionStart = 0
            found_input.selectionEnd = 0
          }
        }
      }

    },

    focusOnLastBlock() {
      setTimeout(() => {
        let input_blocks = document.querySelectorAll('.block_input')
        input_blocks[input_blocks.length - 1].focus()
      })

    },

    focusOnTitle() {
      let textarea = this.$refs[`input_${this.random_number}`]
      let title_parent = textarea.parentElement.parentElement.parentElement.previousSibling
      let title_input = title_parent.querySelector('textarea')
      title_input.focus()
    },


    updateBlock() {
      axios.put(`${this.server}block/${this.block.id}/`,
        this.block,
        {headers: this.auth_headers})
    },

    getBlockIndex(id) {
      // * find block by id and return index of this block
      for (let i=0; i<this.article.blocks.length; i++) {
        if (Number(this.article.blocks[i].id) === Number(id)) {
          return i
        }
      }
    },


    goOverPopupMenu(key) {
      for (let i=0; i<this.popup_menu.length; i++) {
        if (this.popup_menu[i].active) {
          this.popup_menu[i].active = false
          // go to next block or on the first
          if (key === 'ArrowDown') {
            if (this.popup_menu[i+1] && !this.popup_menu[i+1].active) {
              this.popup_menu[i+1].active = true
            } else {
              this.popup_menu[0].active = true
            }
          } else if (key === 'ArrowUp') {
            if (this.popup_menu[i-1] && !this.popup_menu[i-1].active) {
              this.popup_menu[i-1].active = true
            } else {
              this.popup_menu[this.popup_menu.length - 1].active = true
            }
          }

          break;
        }
      }
    },
  }
}
</script>

<style lang="sass" scoped>
@import "@/assets/sass/style.sass"
</style>