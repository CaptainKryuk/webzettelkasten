<template>
<div id="app">
  <router-view/>
</div>
</template>

<style lang="scss">
@mixin font($fname, $fstyle, $fweight, $furl) {
  @font-face {
    font-family: $fname;
    font-style: $fstyle;
    font-weight: $fweight;
    // font-display: swap // Uncomment to initially display system fonts
    src: local($fname), url($furl) format('woff2');
  }
}

@include font('Lato', normal, 300, './assets/fonts/Lato/Lato-Light.ttf');
@include font('Lato', normal, 400, './assets/fonts/Lato/Lato-Regular.ttf');
@include font('Lato', normal, 500, './assets/fonts/Lato/Lato-Medium.ttf');
@include font('Lato', normal, 700, './assets/fonts/Lato/Lato-Bold.ttf');
@include font('Lato', normal, 900, './assets/fonts/Lato/Lato-Heavy.ttf');

#app {
  font-family: 'Lato', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;
  line-height: 1.5;
  overflow-y: hidden;
}

body {
  margin: 0;
  overflow-y: auto;
}
</style>
