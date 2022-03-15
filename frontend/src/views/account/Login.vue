<template>
<transition name="appear" appear="">
  <div class="account" v-if="show">
    <div class="form_wrapper">
      <div class="title_text">
        <p class="title">Вход в Webzettel</p>
        <p class="subtitle">
          Нет аккаунта? <router-link to="/registration">Зарегистрируйтесь</router-link>
        </p>
      </div>

      <form @submit.prevent="successForm()">
        <textinput v-model="user.email" type="email" :required='true' field_name="Электронная почта" placeholder="mail@mail.com" icon="/static/img/mail.svg" />
        <textinput v-model="user.password" :required='true' field_name="Пароль" type="password" placeholder="6+ знаков. 1+ Заглавная буква" icon="/static/img/lock.svg" />

        <p style="color: red">{{ error }}</p>
        <button class="form_button" type="submit">Войти</button>
      </form>
    </div>
  </div>
</transition>
</template>

<script>
import axios from 'axios'
import { mapMutations, mapState } from 'vuex'

export default {
  name: 'Registration',

  data() {
    return {
      user: {
        email: '',
        password: ''
      },
      error: '',
      show: false,
    }
  },

  computed: {
    ...mapState(['server'])
  },

  mounted() {
    this.show = true
  },

  methods: {
    ...mapMutations(['UPDATE_EMAIL', 'UPDATE_ID', 'UPDATE_AUTH_HEADERS', 'UPDATE_USERNAME']),

    successForm() {
      this.error = ''
      axios.post(`${this.server}user/login/`,
        this.user)
        .then((response) => {
          this.UPDATE_EMAIL(response.data.email)
          this.UPDATE_ID(response.data.id)
          this.UPDATE_AUTH_HEADERS(response.data.token)
          this.UPDATE_USERNAME(response.data.username)
          this.$router.push('/mind')
        })
        .catch((error) => {
          this.error = error.response.data
        })
    }
  }

}
</script>

<style lang="sass" scoped>
@import "@/assets/sass/style.sass"
</style>