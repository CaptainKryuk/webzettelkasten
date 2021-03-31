<template>
  <div class="detail_block">
    <div class="detail_block__icon" :style="is_textarea_focus ? 'opacity: 1;' : ''">
      <img src="@/assets/img/move.svg" />
    </div>

    <!-- editor -->
    <label class="block_input" :for="`input_${random_number}`" >
      <textarea v-if="block.block_type === 'text' || block.block_type === 'title' || block.block_type === 'code'"
                :class="block_classes"
                :id="`input_${random_number}`"
                v-model="block.inner_text"
                rows="1"
                :placeholder="getBlockPlaceholder()"
                @input="mixin_autoResize_resize"
                @keydown.tab.exact="addTabSpace"
                @keydown.enter.exact="handleInput"
                @keydown.enter.shift="createBlock($event)"
                @keydown.enter.ctrl="createBlock($event)"
                @keydown.backspace="handleInput"
                @focus="is_textarea_focus = true"
                @blur="is_textarea_focus = false"
                @keydown.up="handleInput"
                @keydown.down="handleInput">
                </textarea>
      
      <div class="row_numbered" v-if="block.block_type === 'code'">
        <span class="number" v-for="(number, index) in line_numbers" :key="index">{{ number }}</span>
      </div>

      <div class="code_lang" v-if="block.block_type === 'code'">
        <img :src="`/static/img/${block.code_lang}.svg`" @click="show_langs = true" />

        <div class="lang_lists">
          
          <div v-for="(lang, index) in langs" :key="index" @click="block.code_lang = lang" >
            <img :src="`/static/img/${lang}.svg`" v-if="lang !== block.code_lang" />
          </div>
        </div>

      </div>

      
      <list-mixin v-if="block.block_type === 'list'"
                  v-model="block.inner_text" 
                  :id_number="random_number"
                  @keydown_tab_exact="addTabSpace"
                  @keydown_enter_exact="handleInput"
                  @keydown_enter_shift="createBlock($event)"
                  @keydown_enter_ctrl="createBlock($event)"
                  @keydown_backspace="handleInput"
                  @keydown_up="handleInput"
                  @focus="is_textarea_focus = true"
                  @blur="is_textarea_focus = false"
                  @keydown_down="handleInput"></list-mixin>

    </label>

    <div class="detail_block__icon">
      <img src="@/assets/img/more.svg" />
    </div>

    <transition name="appear" appear>
      <div class="popup_menu" v-if="is_open_menu">
        <div v-for="(item, index) in popup_menu" 
             :key="index" 
             :class="['popup_menu__item', item.active ? 'active' : '']"
             @click="changeBlock($event, item.type)">
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
import ListMixin from './components/ListMixin'
import ListFunctionsMixinVue from './mixins/ListFunctionsMixin.vue';

export default {
  name: 'EditBlock',

  props: ['block', 'index'],

  mixins: [mixinAutoResize, ListFunctionsMixinVue],

  components: {
    'list-mixin': ListMixin
  },

  data() {
    return {
      random_number: 0,
      greph: '',
      show_langs: false,

      popup_menu: [
        {icon: 'h', tag: '/header', name: 'Заголовок', active: true, type: 'title'},
        {icon: 'pic', tag: '/img', name: 'Изображение', active: false, type: 'img'},
        {icon: 'code', tag: '/code', name: 'Код', active: false, type: 'code'},
        {icon: 'list', tag: '/list', name: 'Список', active: false, type: 'list'},
      ],

      langs: ['python', 'sql', 'js', 'vuejs'],

      is_textarea_focus: false
    }
  },

  computed: {
    ...mapState(['server', 'auth_headers', 'article']),

    is_open_menu() {
      let match_text = this.block.inner_text.match(/^\/$/)
      return match_text && match_text[0].length
      && this.isTextareaFocus()
      && this.block.block_type === 'text'
    },

    block_classes() {
      if (this.block.block_type === 'title') {
        return 'title_textarea h1'
      } else if (this.block.block_type === 'code') {
        return 'code_textarea'
      }
    },

    line_numbers() {
      return this.block.inner_text.split(/\r*\n/).length
    },
  },

  watch: {
    'block.inner_text': {
      handler() {
        this.debouncedUpdateBlock()
      }
    },

    'block.code_lang': {
      handler() {
        this.debouncedUpdateBlock()
      }
    }
  },

  created() {
    this.debouncedUpdateBlock = _.debounce(this.updateBlock, 500)
  },

  mounted() {
    this.random_number = String(Math.random()).split('.')[1]
    this.setupTextarea()
  },


  methods: {
    test(e) {
      this.block.inner_text = e.target.innerText
    },

    ...mapMutations(['ADD_NEW_BLOCK', 'DELETE_BLOCK',]),

    setupTextarea() {
      /* 
      * after page reloading need to install valid height
      */ 
      setTimeout(() => {
        let textarea = this.getCurrentInput()
        if (textarea) {
          if (this.block.inner_text && this.block.inner_text.length) {
            // * if text area have text
            textarea.style.height = textarea.scrollHeight + 'px'
          } else {
            if (this.block.block_type === 'text') {
              textarea.style.height = '36px'
            } else if (this.block.block_type === 'title') {
              textarea.style.height = '39px'
            }
          }
        }

      })
    },


    async handleInput(e) {
      /*
      * if user click on: 
      *   Enter: if menu opened -> change this block to the selected type
      *   Backspace and block.inner_text is blank -> delete this block and focus on previous 
      *   Arrows up and down -> go over blocks
      */
      if (e.key === 'Enter') {
        // * enter
        if (this.is_open_menu) {
          // * If menu open change block type
          for (let i=0; i<this.popup_menu.length; i++) {
            if (this.popup_menu[i].active) {
              this.changeBlock(e, this.popup_menu[i].type);
              break
            }
          }
        } 

        else {
          if (this.block.block_type === 'title') {
            e.preventDefault()
            this.createOrFocus()
          } 

          else if (this.block.block_type === 'list') {
            // * get last li element, if that blank -> go to next block or create new
            let block = this.getCurrentInput()
            let all_li = block.querySelectorAll('li')
            let last_li = all_li[all_li.length-1]
            let len_last = last_li.innerText.replace(/\s*/, '').length

            if (window.getSelection().getRangeAt(0).startOffset === len_last && len_last === 0) {
              e.preventDefault()

              if (all_li.length === 1) {
                this.changeBlock(e, 'text')
              } else {
                const foo = async function() { return new Promise((resolve, reject) => { last_li.remove(); resolve(); })}
                await foo()
                this.block.inner_text = this.getCurrentInput().innerHTML
                this.mixin_autoResize_resize(e)
                await this.updateBlock()
                this.createOrFocus(e)
              }

            }
          }
        }
      } 

      else if (e.key === 'Backspace') {
        // * backspace
        let blank_string = this.block.inner_text.replace(/<\/?\s*[ullibr][^>]*>/g, '').replace(/\s*/, '')
        let textarea = this.getCurrentInput()

        if ((textarea.selectionStart === 0 && textarea.selectionEnd === 0)
            || (this.block.block_type === 'list' 
                && window.getSelection().getRangeAt(0).startOffset === 0 
                && this.getListLiChilds(textarea).length === 1)) {
          if (!blank_string.length ) {
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
          let textarea = this.getCurrentInput()
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
              this.focusOnBlock('next', true)
            }
          }
        }    
      }
    },

    changeBlock(e, new_type) {
      e.preventDefault()
      this.block.block_type = new_type
      if (new_type === 'title') {
        this.block.inner_text = ''
        e.srcElement.style.height = '39px'
      } 
      
      else if (new_type === 'list') {
        this.block.inner_text = '<ul style="margin-top: 0; margin-bottom: 0"><li></li></ul>'
        setTimeout(() => {
          // * setTimeout need to be in time, whem ListMixin have been updated
          this.getCurrentInput().focus()
        })

      } 
      
      else if (new_type === 'text') {
        this.block.inner_text = ''
        e.srcElement.style.height = '36px'
        setTimeout(() => {
          // * need time to install valid styles
          this.getCurrentInput().focus()
        })
      } 
      
      else if (new_type === 'code') {
        this.block.inner_text = ''
        e.srcElement.style.height = '42px'
      }

    },

    getBlockPlaceholder() {
      if (this.block.block_type === 'title') {
        return 'Заголовок'
      } else if (this.index === this.article.blocks.length - 1 && this.block.block_type === 'text') {
        return 'Введите "/" для вызова меню'
      } else {
        return ''
      }
    },

    createOrFocus(e) {
      if (this.article.blocks[this.index + 1]) {
        this.focusOnBlock('next')
      } else {
        this.createBlock(e)
      }
    },

    createBlock(e, type='text') {
      /*
      * if we call "Shift/Ctrl + Enter" from last block -> just add new to the end of block list
      * if we call from block from center -> add it after passed index
      */
      try {
        e.preventDefault()
      } catch {

      }
      
      let data = {
        article: this.$route.params.id,
        block_type: type
      }
      if (this.index !== Number(this.article.blocks.length) - 1) {
        data['order_number'] = this.block.order_number + 1
      }

      axios.post(`${this.server}block/`,
        data,
        {headers: this.auth_headers})
        .then((response) => {
          this.ADD_NEW_BLOCK({data: response.data, index: this.index})
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
      let textarea = this.getCurrentInput()
      let parent;
      if (type === 'previous') {
        if (this.index !== 0) {
          parent = textarea.parentElement.parentElement.previousSibling
        } else {
          this.focusOnTitle()
        }
      } else if (type === 'next') {
        if (this.index < this.article.blocks.length - 1) {
          parent = textarea.parentElement.parentElement.nextSibling
        }
      }

      if (parent) {
        let is_div = false
        let found_input = parent.querySelector('textarea')
        if (!found_input) {
          found_input = parent.querySelector('.textarea')
          is_div = true
        }
        if (found_input) {
          found_input.focus()

          if (type === 'previous') {
            found_input.selectionStart = 9999
            if (is_div) {
              this.setListCaret(found_input)
            }
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
      let textarea = this.getCurrentInput()
      let title_parent = textarea.parentElement.parentElement.parentElement.previousSibling
      let title_input = title_parent.querySelector('textarea')
      title_input.focus()
    },


    updateBlock() {
      return new Promise((resolve, reject) => {
        axios.put(`${this.server}block/${this.block.id}/`,
          this.block,
          {headers: this.auth_headers})
          .then((response) => {
            resolve()
          })
      })

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

    addTabSpace(e) {
      console.log('tab')
      e.preventDefault()
    },

    closeLangs() {
      console.log('te', this.index)
      this.show_langs = false
    },

    isTextareaFocus() {
      let textarea = this.getCurrentInput()
      return textarea === document.activeElement
    },

    getCurrentInput() {
      if (this.block.block_type === 'list') {
        return document.querySelector(`#input_${this.random_number}`)
      } else {
        return document.querySelector(`#input_${this.random_number}`)
      }

    },
  }
}
</script>

<style lang="sass" scoped>
@import "@/assets/sass/style.sass"
</style>