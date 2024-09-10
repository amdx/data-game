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
    <div class="headline-holder">
      <div class="headline">{{ $t('evaluation_view.yeah') }}</div>
      <div class="sub-headline">{{ $t('evaluation_view.meet') }}</div>
    </div>
  </main>
</template>

<script setup lang="ts"></script>

<style scoped>
main {
  background-image: url('/images/final_scene_bg.svg');
  background-size: cover; /* This makes sure the image covers the entire element */
  height: 100vh; /* Set the height to 100% of the viewport height */
  color: white; /* If your image is dark, make the text color white for better contrast */
  display: flex;
}

.headline-holder {
  position: absolute;
  top: 83px;
  left: 144px;
}

.headline {
  font-size: 60px;
  letter-spacing: 4.86px;
}

.sub-headline {
  font-family: Lexend-ExtraLight;
  font-size: 38px;
  letter-spacing: 1.05px;
  white-space: pre-line;
}
</style>
