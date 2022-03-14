<template>
  <div class="article_blocks">
    <editor v-for="(block, index) in article.blocks" 
            :block="block" 
            :index="index"
            :drag_index="block.order_number"
            :drag_id="block.id"
            :key="index"
            class='detail_block_wrapper'></editor>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import EditBlock from './EditBlock'
import DragAndDropMixin from './mixins/DragAndDropMixin'

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