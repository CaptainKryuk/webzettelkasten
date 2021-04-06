// autoResize.js
export default {
  methods: {
    mixin_autoResize_resize(event) {
      event.target.style.height = "auto";
      event.target.style.height = `${event.target.scrollHeight}px`;
    }
  },
  mounted() {
    this.$nextTick(() => {
      try {
        this.$el.setAttribute("style", "height",
        `${this.$el.scrollHeight}px`);
      } catch {

      }
    });
  }
};