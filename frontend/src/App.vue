<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style lang="sass">
@mixin font($fname, $fstyle, $fweight, $furl)
  @font-face
    font-family: $fname
    font-style: $fstyle
    font-weight: $fweight
    // font-display: swap // Uncomment to initially display system fonts
    src: local($fname), url($furl) format('woff2')

@include font('Lato', normal, 300, './assets/fonts/Lato/Lato-Light.ttf')
@include font('Lato', italic, 300, './assets/fonts/Lato/Lato-LightItalic.ttf')
@include font('Lato', normal, 400, './assets/fonts/Lato/Lato-Regular.ttf')
@include font('Lato', italic, 400, './assets/fonts/Lato/Lato-Italic.ttf')
@include font('Lato', normal, 500, './assets/fonts/Lato/Lato-Medium.ttf')
@include font('Lato', italic, 500, './assets/fonts/Lato/Lato-MediumItalic.ttf')
@include font('Lato', normal, 700, './assets/fonts/Lato/Lato-Bold.ttf')
@include font('Lato', italic, 700, './assets/fonts/Lato/Lato-BoldItalic.ttf')
@include font('Lato', normal, 800, './assets/fonts/Lato/Lato-Heavy.ttf')
@include font('Lato', italic, 800, './assets/fonts/Lato/Lato-HeavyItalic.ttf')


#app
  font-family: 'Lato', sans-serif
  -webkit-font-smoothing: antialiased
  -moz-osx-font-smoothing: grayscale
  text-align: left
  scroll-behavior: smooth
  text-rendering: optimizeLegibility
  padding: 0
  margin: 0

body
  margin: 0
  padding: 0

</style>
