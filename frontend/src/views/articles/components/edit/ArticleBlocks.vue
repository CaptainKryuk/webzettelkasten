<template>
  <div class="article_blocks">
    <ckeditor :editor="editor" 
              v-model="article.source" 
              :config="editorConfig"
              @ready="onReady"></ckeditor>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import EditBlock from './EditBlock'
import DragAndDropMixin from './mixins/DragAndDropMixin'

import ClassicEditor from '@ckeditor/ckeditor5-editor-classic/src/classiceditor';

import EssentialsPlugin from '@ckeditor/ckeditor5-essentials/src/essentials';
import BoldPlugin from '@ckeditor/ckeditor5-basic-styles/src/bold';
import ItalicPlugin from '@ckeditor/ckeditor5-basic-styles/src/italic';
import LinkPlugin from '@ckeditor/ckeditor5-link/src/link';
import ParagraphPlugin from '@ckeditor/ckeditor5-paragraph/src/paragraph';
import InsertImage from '@/ckeditor/plugins/insertimage.js'
import Autoformat from '@ckeditor/ckeditor5-autoformat/src/autoformat';
import Underline from '@ckeditor/ckeditor5-basic-styles/src/underline';
import Strikethrough from '@ckeditor/ckeditor5-basic-styles/src/strikethrough';
import Code from '@ckeditor/ckeditor5-basic-styles/src/code';
import Subscript from '@ckeditor/ckeditor5-basic-styles/src/subscript';
import Superscript from '@ckeditor/ckeditor5-basic-styles/src/superscript';
import CodeBlock from '@ckeditor/ckeditor5-code-block/src/codeblock';
import Indent from '@ckeditor/ckeditor5-indent/src/indent';
import IndentBlock from '@ckeditor/ckeditor5-indent/src/indentblock';
import Heading from '@ckeditor/ckeditor5-heading/src/heading';
import List from '@ckeditor/ckeditor5-list/src/list';
import TodoList from '@ckeditor/ckeditor5-list/src/todolist';
import Link from '@ckeditor/ckeditor5-link/src/link';
import AutoLink from '@ckeditor/ckeditor5-link/src/autolink';
import Minimap from '@ckeditor/ckeditor5-minimap/src/minimap';


export default {
  /*
  * Этот компонент нужен, чтобы привязать к нему :key у родителя и обновлять его после перестановки
  * Если нужно перенести блок - он переносится, отправляется запрос на сохранение, 
  * С возвращенными данными делается сортировка и отправляется родителю запрос, по которому просто изменяем :key и 
  * компонент обновляется
  * Его нужно обновлять, потому что нужны нормальный параметр :index, потому что новый блок добавляется в центр списка по индексу
  */
  name: 'ArticleBlocks',

  components: {
    'editor': EditBlock
  },

  mixins: [DragAndDropMixin],

  computed: {
    ...mapState(['server', 'auth_headers', 'article'])
  },

  data() {
    return {
      editor: ClassicEditor,
      editorConfig: {
        plugins: [
          EssentialsPlugin,
          BoldPlugin,
          ItalicPlugin,
          LinkPlugin,
          ParagraphPlugin,
          InsertImage,
          Autoformat,
          Underline,
          Strikethrough,
          Code,
          Subscript,
          Superscript,
          CodeBlock,
          Indent,
          IndentBlock,
          Heading,
          List,
          TodoList,
          Link, AutoLink,
        ],

        toolbar: {
          items: [
            'heading', '|',
            'bold', 'italic', 'bulletedList', 'numberedList', 'todoList', 'link', '|',
            'outdent', 'indent', '|',
            'underline', 
            'strikethrough', 
            'code',
            'subscript', 
            'superscript', '|',
            'codeBlock',
          ]
        },

        codeBlock: {
          languages: [  
            { language: 'plaintext', label: 'Plain text' }, // The default language.
            { language: 'css', label: 'CSS' },
            { language: 'html', label: 'HTML' },
            { language: 'javascript', label: 'JavaScript' },
            { language: 'python', label: 'Python' },
            { language: 'bash', label: 'Bash'}
          ]
        },
      }
    }
  },

  mounted() {
    setTimeout(() => {
      this.setupDragAndDrop('article_blocks', 'detail_block')
    }, 400)
  },

  methods: {

    updateMovedObject() {
      this.$axios.put(`${this.server}block/${this.active_id}/update_order_number/`,
        {order_number: this.new_order_number},
        {headers: this.auth_headers})
        .then((response) => {
          // * мы получили это бэкенда номера блоков и сейчас выставляем их в правильном порядке
          for (let i=0; i<this.article.blocks.length; i++) {
            let block = this.article.blocks[i]
            this.article.blocks[i].order_number = response.data[block.id]
          }
          this.article.blocks = this.article.blocks.sort((a, b) => parseFloat(a.order_number) - parseFloat(b.order_number))
          this.$emit('render')
        })
    },

    forceRendered() {
      this.component_key += 1
    },
  }
}
</script>

<style lang="css">
.ck.ck-editor__top {
  /* styling editor header */
}
</style>