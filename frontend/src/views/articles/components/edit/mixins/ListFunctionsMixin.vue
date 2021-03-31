<script>
export default {
  name: 'ListFunctioinsMixin',

  methods: {
    setListCaret(input) {
      /*
      * if you go to list block you need to create Range for valid installing caret on editable div block 
      */
      let range = document.createRange()
      let sel = window.getSelection()

      let li = this.getListLiChilds(input)

      range.setStart(li[li.length-1], 1)
      range.collapse(true)

      sel.removeAllRanges()
      sel.addRange(range)
    },

    getListLiChilds(input) {
      let ul = input.childNodes[0]
      if (ul) {
        let li = ul.childNodes
        return li
      }
      return []
    }
  }
}
</script>