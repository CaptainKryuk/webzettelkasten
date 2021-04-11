<script>
export default {
  name: "BlockDropdownMenuMixin",

  data() {
    return {
      show_fold: false,
      approve_delete: false,
      options: [
        {name: 'Создать блок', func: this.createBlock},
        {name: 'Удалить блок', func: this.openApproveWindow}
      ]
    }
  },

  methods: {
    closeMenu() {
      this.show_fold = false
    },
  
    openApproveWindow(e) {
      this.approve_delete = true
    },
  }
}
</script>

<style lang="sass" scoped>
@import "@/assets/sass/style.sass"
</style>