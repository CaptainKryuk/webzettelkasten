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
    this.$store.commit('UPDATE_AUTH_HEADERS', '123')
  }
}
</script>

<style scoped lang="sass">
@import "@/assets/sass/style.sass"
</style>