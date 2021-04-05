<template>
  <div class="approve__block">
    <transition name="appear" appear>
      <div class="shadow_background" v-if="show" @click="closeBoard()"></div>
    </transition>

    <transition name="floating-right" appear>
      <div class="approve__block_content" v-if="show">
        <p class="block_title">Удалить статью?</p>
        <div class="approve_buttons">
          <button class="btn success" @click="deleteArticle()">Удалить</button>
          <button class="btn cancel" @click="closeBoard()">Отмена</button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import { mapMutations, mapState } from 'vuex'
export default {
  name: 'DeleteArticle',

  data() {
    return {
      show: false
    }
  },

  computed: {
    ...mapState(['server', 'auth_headers'])
  },

  mounted() {
    this.show = true
  },

  methods: {
    ...mapMutations(['DELETE_ARTICLE']),
    deleteArticle() {
      this.$axios.delete(`${this.server}articles/${this.$route.params.id}`,
        {headers: this.auth_headers})
        .then((response) => {
          this.DELETE_ARTICLE(this.$route.params.id)
          this.closeBoard()
        })
    },

    closeBoard() {
      this.show = false
      setTimeout(() => {
        this.$router.go(-1)
      }, 300)
    }
  }
}
</script>

<style lang="sass" scoped>
@import "@/assets/sass/style.sass"
</style>

