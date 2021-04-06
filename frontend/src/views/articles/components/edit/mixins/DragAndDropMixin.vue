<template>
  
</template>

<script>
export default {
  name: 'DragAndDropMixin',

  data() {
    return {
      new_order_number: 0,
      active_id: 0
    }
  },

  methods: {
    setupDragAndDrop(list_class, detail_class) {
      if (window.screen.width > 1200) {
        const tasksListElement = document.querySelector(`.${list_class}`);
        const taskElements = tasksListElement.querySelectorAll(`.${detail_class}`);

        // добавляем свойство для перемещения
        for (const task of taskElements) {
          task.draggable = true;
        }

        tasksListElement.addEventListener(`dragstart`, (evt) => {
          if (evt.target.classList.contains(`${detail_class}`)) {
            this.active_id = evt.target.getAttribute('drag_id')
            this.new_order_number = evt.target.getAttribute('drag_index')
            evt.target.classList.add(`selected`);
          }
        });

        tasksListElement.addEventListener(`dragend`, (evt) => {
          evt.target.classList.remove(`selected`);        
          this.updateMovedObject()
        });

        const getNextElement = (cursorPosition, currentElement) => {
          const currentElementCoord = currentElement.getBoundingClientRect();
          const currentElementCenter = currentElementCoord.y + currentElementCoord.height / 2;
          
          const nextElement = (cursorPosition < currentElementCenter) ?
            currentElement :
            currentElement.nextElementSibling;
          
          return nextElement;
        };

        tasksListElement.addEventListener(`dragover`, (evt) => {
          evt.preventDefault();
          
          const activeElement = tasksListElement.querySelector(`.selected`);
          const currentElement = evt.target;
          const isMoveable = activeElement !== currentElement &&
            currentElement.classList.contains(`${detail_class}`);

          if (!isMoveable) {
            return;
          }
          
          const nextElement = getNextElement(evt.clientY, currentElement);
          
          if (
            nextElement && 
            activeElement === nextElement.previousElementSibling ||
            activeElement === nextElement
          ) {
            return;
          }
            
          tasksListElement.insertBefore(activeElement, nextElement);
          
          let a_index = activeElement.getAttribute('drag_index')
          let n_index;
          try {
            n_index = nextElement.getAttribute('drag_index') 
          } catch {
            n_index = null
          }

          if (!n_index) {
            // need to get last element
            this.new_order_number = taskElements[taskElements.length - 1].getAttribute('drag_index')
          } else {
            if (a_index < n_index) {
              this.new_order_number = n_index - 1
            } else if (a_index > n_index) {
              this.new_order_number = n_index
            }
          }
        });
      }
    },
  }
}
</script>

