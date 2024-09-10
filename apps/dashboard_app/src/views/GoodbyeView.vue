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

<script setup lang="ts">
import MenuButton, { ButtonType } from '@/components/MenuButton.vue'
import NextButton from '@/components/NextButton.vue'
</script>

<template>
  <main>
    <div class="fullscreen-container">
      <span class="title">{{ $t('goodbye.title') }}</span>
      <span class="text">{{ $t('goodbye.text') }}</span>

      <NextButton link-to="/" />
      <MenuButton :buttons="[ButtonType.RESET]" />
    </div>
  </main>
</template>

<style scoped>
.fullscreen-container {
  background-image: url("/images/end_scene_bg.svg");
}

.title {
  position: absolute;
  font-family: Lexend-ExtraLight;
  font-size: 138px;
  letter-spacing: 11.04px;
  line-height: 168px;
  color: #FFFFFF;
  top: 718px;
  left: 1216px;
  width: 1356px;
  height: 455px;
}

.text {
  position: absolute;
  font-family: Lexend-ExtraLight;
  font-size: 48px;
  letter-spacing: 1.92px;
  line-height: 64px;
  color: #FFFFFF;
  top: 1184px;
  left: 1648px;
  width: 974px;
  height: 361px;
}
</style>
