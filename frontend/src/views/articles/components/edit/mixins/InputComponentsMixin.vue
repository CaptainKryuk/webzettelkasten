<script>
import ListFunctioinsMixin from './ListFunctionsMixin.vue'

import { mapMutations, mapState } from 'vuex'
export default {

  mixins: [
    ListFunctioinsMixin
  ],

  data() {
    return {
      // blocks which use textarea block
      text_types: ['text', 'title', 'code', 'markdown']
    }
  },

  computed: {
    ...mapState(['server', 'auth_headers', 'popup_menu', 'article'])
  },

  methods: {
    ...mapMutations(['ADD_NEW_BLOCK', 'DELETE_BLOCK']),

    textInput(e) {
      this.mixin_autoResize_resize(e)
      this.$emit('update:modelValue', e.target.value)
    },

    addTabSpace(e) {
      e.preventDefault()
      let input = e.target
      let start = input.selectionStart
      let end = input.selectionEnd
      let text = this.block.inner_text

      if (start === end) {
        this.tabCursorSpace(input, text, start)
      } else {
        this.tabHighlightedText(input, start, end)
      }
    },

    tabCursorSpace(input, text, start) {
      // * Текст не выделен, просто добавление пары пробелов
      input.blur()
      let before = text.slice(0, start)
      let after = text.slice(start)
      this.block.inner_text = before + '  ' + after
      setTimeout(() => {
        input.focus()
        input.selectionStart = before.length + 2
        input.selectionEnd = before.length + 2
      })
    },

    tabHighlightedText(input, start, end) {
      // * текст выделен, и если выделено несколько строк, их надо все перенести
      input.blur()
      let text_inside = this.block.inner_text.slice(start, end)
      let split_inside_text = text_inside.split(/\n/)
      let new_string = '';
      split_inside_text.forEach((text, index) => {
        new_string += '  ' + text + (index !== split_inside_text.length - 1 ? '\n' : '')
      })
      this.block.inner_text = this.block.inner_text.replace(text_inside, new_string)
      setTimeout(() => {
        input.focus()
        let additional_space = '';
        split_inside_text.forEach((space) => {
          additional_space += '  '
        })
        input.selectionStart = end + additional_space.length
        input.selectionEnd = end + additional_space.length
      })
    },

    handleMenuKeys(e) {
      /*
      * if user click on: 
      *   Enter: change this block to the selected type
      *   Backspace: close menu 
      *   Arrows up and down: go over blocks
      */
      if (e.key === 'Enter') {
        for (let i=0; i<this.popup_menu.length; i++) {
          if (this.popup_menu[i].active) {
            this.changeBlock(e, this.popup_menu[i].type);
            break
          }
        }
      } else if (e.key === 'ArrowUp' || e.key === 'ArrowDown') {
        // * when menu is opened need to go over items in this menu
        e.preventDefault()
        this.goOverPopupMenu(e.key)
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

    async handleInput(e) {
      /*
      * if user click on: 
      *   Enter: if menu opened -> change this block to the selected type
      *   Backspace and block.inner_text is blank -> delete this block and focus on previous 
      *   Arrows up and down -> go over blocks
      */
      if (this.is_open_menu) {
        return this.handleMenuKeys(e)
      }
      if (e.key === 'Enter') {
          if (this.block.block_type === 'title') {
            e.preventDefault()
            this.createOrFocus()
          } else if (this.block.block_type === 'list') {
            // * get last li element, if that blank -> go to next block or create new
            let all_li = e.target.querySelectorAll('li')
            let last_li = all_li[all_li.length-1]
            let len_last = last_li.innerText.replace(/\s*/, '').length

            if (window.getSelection().getRangeAt(0).startOffset === len_last && len_last === 0) {
              e.preventDefault()

              if (all_li.length === 1) {
                this.changeBlock(e, 'text')
              } else {
                const foo = async function() { return new Promise((resolve, reject) => { last_li.remove(); resolve(); })}
                await foo()
                this.block.inner_text = e.target.innerHTML
                this.mixin_autoResize_resize(e)
                await this.updateBlock()
                this.createOrFocus(e)
              }

            }
          } 

          else if (this.block.block_type === 'img') {
            e.preventDefault()
            this.createOrFocus(e)
          } 

          else {
            e.preventDefault()
            e.target.blur()
            let cursor = e.target.selectionEnd
            let text_before = this.block.inner_text.slice(0, cursor)
            let text_after = this.block.inner_text.slice(cursor)
            let split_text = text_before.split(/\n/)
            let blank_space = split_text[split_text.length-1].match(/^ */)[0]
            let new_string = text_before + '\n' + blank_space + text_after
            this.block.inner_text = new_string

            setTimeout(() => {
              e.target.focus()
              e.target.selectionStart = text_before.length + blank_space.length + 1
              e.target.selectionEnd = text_before.length + blank_space.length + 1
              this.mixin_autoResize_resize(e)
            })
          }
        }

      else if (e.key === 'Backspace') {
        // * backspace
        let blank_string = this.block.inner_text.replace(/<\/?\s*[ullibr][^>]*>/g, '').replace(/\s*/, '')
        if ((e.target.selectionStart === 0 && e.target.selectionEnd === 0)
            || (this.block.block_type === 'list' 
                && window.getSelection().getRangeAt(0).startOffset === 0 
                && this.getLiElements(e.target).length === 1)) {
          if (!blank_string.length ) {
            // * when block is already blank -> delete if
            this.deleteBlock(e)
          } else {
            // * if we have content in this block go to previous
            e.preventDefault()
            this.focusOnBlock('previous', true)
          }
        }
      } 

      else if (e.key === 'ArrowUp' || e.key === 'ArrowDown') {
        const one_element_width = 6.651162790697675
        // * arrows          
          if (e.key === 'ArrowUp') {
            // 6.651162790697675 - длина 1 символа текста или кода

            // * get number of elements in 1 line in textarea
            let line_length = Math.round(e.target.clientWidth / one_element_width)

            if (this.text_types.includes(this.block.block_type)) {
              // * block text/code/title
              let split_line = e.target.value.split(/\n/)

              if (e.target.selectionStart <= line_length && e.target.selectionStart <= split_line[0].length) {
                e.preventDefault()
                this.focusOnBlock('previous', true)
              }
            } 
            
            else if (this.block.block_type === 'list') {
              // * if list and current position < then first li length and < first line -> go to previous block
              let first_li = this.getLiElements(e.target)[0].innerText
              let cursor = this.getCaretCharacterOffsetWithin(e.target)
              if (cursor[0] <= first_li.length 
                  && first_li[first_li.length - 1] === cursor[1][cursor[1].length - 1] // * check that last elements of line is equal
                  && cursor[0] < line_length) {
                e.preventDefault()
                this.focusOnBlock('previous')
              }
            }

            else if (this.block.block_type === 'img') {
              e.preventDefault()
              this.focusOnBlock('previous')
            }

          } else if (e.key === 'ArrowDown') {
            /*
            * Блок текстовый/code/title: если каретка находится на последней строке-> перенос(нужно знать сколько в строке символов и считать по ним)
            * Блок list: если находится на последней строке - перенос
            */
            let line_length = Math.round(e.target.clientWidth / one_element_width)

            if (this.text_types.includes(this.block.block_type)) {
              let split_value = e.target.value.split(/\n/)
              let last_line = split_value[split_value.length-1]

              if (e.target.selectionStart >= e.target.value.length - last_line.length) {
                // * check that our cursor on last line
                if (last_line.length > line_length) {
                  let elements_in_last_line = this.getElementsInLine(last_line, line_length)
                  // * check that we on last line when clicked arrow
                  if (e.target.selectionStart > (last_line.length - elements_in_last_line)) {
                    e.preventDefault()
                    this.focusOnBlock('next')
                  }
                } else {
                  e.preventDefault()
                  this.focusOnBlock('next')
                }
              }
            } else if (this.block.block_type === 'list') {
              /*
              * Нам нужно понять, находимся ли мы на последнем элементе и
              * если находимся - перенести курсор на тот же элемент первой строки
              */
             
              // * получили все элементы
              let li = this.getLiElements(e.target)
              // * длинная всего контента в ul
              let list_length = this.getListLength(e.target)
              // * получили последний li
              let last_li = li[li.length - 1]

              let elements_in_last_line = this.getElementsInLine(last_li.innerText, line_length)
              let cursor = this.getCaretCharacterOffsetWithin(e.target)
              let clean_last_li =  last_li.innerText.replace(/\s*/, '')

              if ((clean_last_li.length !== 0 ? last_li.innerText : null) === (cursor[1].length ? cursor[1] : null) 
                  && cursor[0] >= (list_length - elements_in_last_line)) {
                e.preventDefault()
                this.focusOnBlock('next')
              }
            } else if (this.block.block_type === 'img') {
              e.preventDefault()
              this.focusOnBlock('next')
            }
          }
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

      // * Установка порядкового номера
      if (this.index !== Number(this.article.blocks.length) - 1) {
        data['order_number'] = this.block.order_number + 1
      }

      this.$axios.post(`${this.server}block/`,
        data,
        {headers: this.auth_headers})
        .then((response) => {
          this.ADD_NEW_BLOCK({data: response.data, index: this.index})
          setTimeout(() => {
            this.focusOnBlock('next')
          })
        })
    },

    focusOnBlock(type='previous', to_start=false) {
      let textarea = this.$refs.input
      let parent;
      if (type === 'previous') {
        if (this.index !== 0) {
          parent = textarea.parentElement.parentElement.previousSibling
        } else {
          this.focusOnTitle(textarea.selectionStart)
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
          // that's for list element
          found_input = parent.querySelector('.textarea')
          is_div = true
        }

        if (found_input) {
          // * Нужно изменить стиль, если тип поля markdown
          found_input.style.display = 'inline-block'

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

    deleteBlock(e) {
      /*
      * check that block is not last and 
      * delete current block and focus on previous 
      * if block is last -> don't delete it and focus on title
      */
      if (this.article.blocks.length > 1) {
        this.$axios.delete(`${this.server}block/${this.block.id}/`,
          {headers: this.auth_headers})
          .then((response) => {
            this.focusOnBlock('previous')
            this.DELETE_BLOCK(this.block.id)
          })
      } else {
        this.block.inner_text = ''
        if (this.block.block_type === 'list' || this.block.block_type === 'img' || this.block.block_type === 'title') {
          this.changeBlock(e, 'text')
        }
        try {
          e.preventDefault()
        } catch {
          
        }

        this.focusOnTitle()
      }

    },

    focusOnTitle(selectionPosition=9999) {
      let textarea = this.$refs.input
      let title_parent = textarea.parentElement.parentElement.parentElement.previousSibling
      let title_input = title_parent.querySelector('textarea')
      title_input.selectionStart = selectionPosition
      title_input.selectionEnd = selectionPosition
      title_input.focus()
    },

    changeBlock(e, new_type) {
      try {
        e.preventDefault()
      } catch {
        
      }
      
      this.block.block_type = new_type

      let text_types = ['title', 'text', 'code', 'markdown']

      if (text_types.includes(new_type)) {
        if (new_type === 'code') {
          this.setupNewBlock(e, '42px')
        } else {
          this.setupNewBlock(e)
        }

      }
      
      else if (new_type === 'list') {
        this.block.inner_text = '<ul style="margin-top: 0; margin-bottom: 0"><li></li></ul>'
        setTimeout(() => {
          // * setTimeout need to be in time, whem ListMixin have been updated
          this.focusOnNewInput('42px')
        }, 400)

      } 
    
      else if (new_type === 'img') {
        this.block.inner_text = ''
        let blocks = this.article.blocks
        // * if we have only 1 block or img block in last position - create new text block after that
        if (blocks.length === 1 || this.block.id === blocks[blocks.length-1].id) {
          this.createBlock()
        }
        e.target.focus()
      }

    },

    setupNewBlock(e, height=undefined) {
      this.block.inner_text = ''
      this.focusOnNewInput(height)
    },

    focusOnNewInput(height=undefined) {
      // * Когда меняется тип блока - меняется элемент - нужно получить новый
      // * также можно передать высоту элемента для установки
      setTimeout(() => {
        let newinput = document.querySelector(`#input_${this.random_number}`)
        
        // * нужно для блока markdown, потому что там стоит v-show и мы должны сначала его показать, а потом focus поставить
        newinput.style.display = 'inline-block'
        if (height) {
          newinput.style.height = height
        }
        newinput.focus()
      })
    },


    createOrFocus(e) {
      if (this.article.blocks[this.index + 1]) {
        this.focusOnBlock('next')
      } else {
        this.createBlock(e)
      }
    },

    updateBlock() {
      return new Promise((resolve, reject) => {
        this.$axios.put(`${this.server}block/${this.block.id}/`,
          this.block,
          {headers: this.auth_headers})
          .then((response) => {
            resolve()

          })
      })
    },
  }
}
</script>