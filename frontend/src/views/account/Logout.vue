<template>
  <section>
    <h1>Logout</h1>
  </section>
</template>

<script>
export default {
  created () {
    localStorage.clear()
    this.$router.push("/")
  }
}
</script>

<style scoped lang="sass">
@import "@/assets/sass/style.sass"
</style>