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
import NextButton from '@/components/NextButton.vue'
import MenuButton, { ButtonType } from '@/components/MenuButton.vue'
import TitleGroup from '@/components/TitleGroup.vue'
</script>

<template>
  <main>
    <div class="fullscreen-container">
      <TitleGroup node="instructions" />

      <div class="textbox" style="position: absolute; left: 224px; top: 1328px">
        <span class="number">1</span>
        <span class="text">{{ $t('instructions.text1') }}</span>
      </div>

      <div class="textbox" style="position: absolute; left: 1400px; top: 1328px">
        <span class="number">2</span>
        <span class="text">{{ $t('instructions.text2') }}</span>
      </div>

      <div class="textbox" style="position: absolute; left: 2576px; top: 1328px">
        <span class="number">3</span>
        <span class="text">{{ $t('instructions.text3') }}</span>
      </div>

      <NextButton link-to="/heroes" />
      <MenuButton :buttons="[ButtonType.RESET, ButtonType.GOODBYE]" />
    </div>
  </main>
</template>

<style scoped>
.fullscreen-container {
  background-image: url("/images/info_graphic_bg.svg");
}

.textbox {
  display: flex;
}

.number {
  font-family: Lexend-ExtraLight;
  font-size: 61px;
  letter-spacing: 2.44px;
  color: #BFD4FF;
}

.text {
  position: relative;
  display: block;
  font-size: 44px;
  letter-spacing: 1.76px;
  line-height: 64px;
  left: 28px;
  width: 792px;
  height: 356px;
  padding-left: 72px;
}
</style>
