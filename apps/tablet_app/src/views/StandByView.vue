<!--
  - Copyright (C) 2024. Archimedes Exhibitions GmbH,
  - Saarbrücker Str. 24, Berlin, Germany
  -
  - This file contains proprietary source code and confidential
  - information. Its contents may not be disclosed or distributed to
  - third parties unless prior specific permission by Archimedes
  - Exhibitions GmbH, Berlin, Germany is obtained in writing. This applies
  - to copies made in any form and using any medium. It applies to
  - partial as well as complete copies.
  -->

<template>
  <main>
    <div class="stand-by">{{ $t('standby_view.text') }}</div>
  </main>
</template>

<style scoped>
main {
  background-image: url('/images/theme_selection_bg.jpg');
  background-size: cover; /* This makes sure the image covers the entire element */
  height: 100vh; /* Set the height to 100% of the viewport height */
  color: white; /* If your image is dark, make the text color white for better contrast */
  display: flex;
}

.stand-by {
  position: absolute;
  top: 588px;
  left: 608px;
  width: 752px;
  letter-spacing: 6.08px;
  color: #ffffff;
  font-size: 76px;
  font-family: Lexend-ExtraLight;
  white-space: pre-line;
}
</style>
