<template>
  <div class="detail_block" :drag_id="drag_id" :drag_index="drag_index">

    <div class="detail_block__icon move" :style="is_input_focus ? 'opacity: 1;' : ''">
      <img src="@/assets/img/move.svg" />
    </div>

    <!-- editor -->

    <label class="block_input">

      <!-- <div style="position: absolute; left: -150px">{{ block.id }} {{ block.order_number }} {{ index }}</div> -->

      <!-- text -->
      <text-com v-model="block.inner_text"
                v-if="block.block_type === 'text'"
                :block='block'
                :index='index'
                :random_number="random_number"
                @change_input_focus='is_input_focus = $event'
                :is_open_menu="is_open_menu"></text-com>

      <!-- code -->
      <code-com v-model="block.inner_text"
                v-else-if="block.block_type === 'code'"
                 :block='block'
                 :index='index'
                 :random_number="random_number"
                 @change_input_focus='is_input_focus = $event'
                 @change_lang="block.code_lang = $event"></code-com>

      <!-- title -->
      <title-com v-model="block.inner_text"
                 v-else-if="block.block_type === 'title'"
                 :block='block'
                 :index='index'
                 :random_number="random_number"
                 @change_input_focus='is_input_focus = $event'></title-com>


      <list-com v-else-if="block.block_type === 'list'"
                  v-model="block.inner_text" 
                  :random_number="random_number"
                  :block="block"
                  :index="index"
                  @change_input_focus='is_input_focus = $event'></list-com>

      <img-com v-else-if="block.block_type === 'img'"
               :random_number="random_number"
               :block="block"
               :index="index"
               @update="block.images = $event"></img-com>

      <markdown-com v-model="block.inner_text"
                    v-if="block.block_type === 'markdown'"
                    :block='block'
                    :index='index'
                    :random_number="random_number"
                    @change_input_focus='is_input_focus = $event'
                    :is_open_menu="is_open_menu"></markdown-com>
    </label>

    <div class="detail_block__icon">
      <div class="dropdown-object" v-click-outside="closeMenu">
        <img class="icon" src="@/assets/img/more.svg" @click="show_fold = true" />

        <div v-if="show_fold" class="fold">
          <div class="option" v-for="(option, index) in options" :key="index" @click="option.func">
            <p class="option__text">{{ option.name }}</p>
          </div>      
        </div>
      </div>
    </div>

    <!-- menu for block changing -->
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

  <!-- modal window for approving -->
  <!-- <modal-window title="Удаление блока"
                description="Вы уверены, что хотите удалить данный блок?"
                button_name="Удалить"
                :show="approve_delete"
                @close="approve_delete = false"
                @submit="deleteBlock"></modal-window> -->
  </div>
</template>

<script>
import mixinAutoResize from "@/global/mixins/autoResize.js";
import _ from 'lodash';
import axios from 'axios'
import { mapMutations, mapState } from 'vuex';
import ListFunctionsMixinVue from './mixins/ListFunctionsMixin.vue';
import BlockDropdownMenuMixin from './mixins/BlockDropdownMenuMixin.vue'
import Img from './components/Img.vue'
import Title from './components/Title.vue'
import Text from './components/Text.vue'
import Code from './components/Code.vue'
import List from './components/List.vue'
import Markdown from './components/Markdown.vue'

export default {
  name: 'EditBlock',

  props: ['block', 'index', 'drag_index', 'drag_id', 'class'],

  mixins: [
    mixinAutoResize, 
    ListFunctionsMixinVue,
    BlockDropdownMenuMixin
  ],

  components: {
    'list-com': List,
    'img-com': Img,
    'title-com': Title,
    'text-com': Text,
    'code-com': Code,
    'markdown-com': Markdown
  },

  data() {
    return {
      random_number: 0,
      greph: '',
      is_input_focus: false,
    }
  },

  computed: {
    ...mapState(['server', 'auth_headers', 'article', 'popup_menu', 'block_sizes']),

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
    },
  },

  created() {
    this.debouncedUpdateBlock = _.debounce(this.updateBlock, 500)
  },

  mounted() {
    this.random_number = String(Math.random()).split('.')[1]
    this.setupTextarea()
  },

  methods: {
    myEventHandler(e) {
      // your code for handling resize...
      e.preventDefault()
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
            textarea.style.height = this.block_sizes[this.block.block_type] 
          }
        }

      })
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

<style lang="sass">
@import "@/assets/sass/style.sass"
</style>