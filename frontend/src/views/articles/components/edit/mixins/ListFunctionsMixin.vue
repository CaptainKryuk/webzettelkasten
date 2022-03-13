<script>
export default {
  name: 'ListFunctioinsMixin',

  methods: {
    setListCaret(input, where='end') {
      /*
      * if you go to list block you need to create Range for valid installing caret on editable div block 
      */
      let range = document.createRange()
      let sel = window.getSelection()

      let li = this.getLiElements(input)
      if (where === 'end') {
        range.setStart(li[li.length-1], 1)
        range.collapse(true)
      } else {
        range.setStart(li[0], 1)
        range.collapse(true)
      }

      sel.removeAllRanges()
      sel.addRange(range)
    },

    getCaretCharacterOffsetWithin(element) {
      // * Получает [позиция курсора, Текст на этой строке]
      var caretOffset = 0;
      let container;
      var doc = element.ownerDocument || element.document;
      var win = doc.defaultView || doc.parentWindow;
      var sel;
      if (typeof win.getSelection != "undefined") {
        sel = win.getSelection();
        if (sel.rangeCount > 0) {
            var range = win.getSelection().getRangeAt(0);
            var preCaretRange = range.cloneRange();
            preCaretRange.selectNodeContents(element);
            container = range.endContainer
            preCaretRange.setEnd(range.endContainer, range.endOffset);
            caretOffset = preCaretRange.toString().length;
        }
      } else if ( (sel = doc.selection) && sel.type != "Control") {
        var textRange = sel.createRange();
        var preCaretTextRange = doc.body.createTextRange();
        preCaretTextRange.moveToElementText(element);
        preCaretTextRange.setEndPoint("EndToEnd", textRange);
        caretOffset = preCaretTextRange.text.length;
      }
      return [caretOffset, container.nodeValue || container.innerText.length]; // cursor index, string value
    },

    getLiElements(input) {
      // * получить все элементы li
      let ul = input.childNodes[0]
      if (ul) {
        return ul.childNodes
      }
      return []
    },

    getElementsInLine(last_line, line_length) {
      return Math.floor(((last_line.length / line_length) - Math.floor(last_line.length / line_length)) * line_length)
    },

    getListLength(input) {
      // * Получить длину всех элементов всех li в списке
      let li_text = '';
      let li = this.getLiElements(input)
      li.forEach(element => {
        li_text += element.innerText
      });
      return li_text.length;
    }
  }
}
</script>