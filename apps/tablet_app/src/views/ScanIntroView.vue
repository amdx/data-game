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
      <div class="headline">{{ t('scan_intro_view.headline') }}</div>
      <div class="sub-headline">{{ t('scan_intro_view.sub_headline') }}</div>
    </div>
    <div class="text-box-holder">
      <div class="text-box" v-for="(item, index) in textKeys" :key="index">
        {{ t(item) }}
      </div>
    </div>
    <ImageButton
      class="button"
      up-source="images/next_btn_up.svg"
      down-source="images/next_btn_down.svg"
      disabled-source=""
      :is-disabled="false"
      @click="router.replace({ name: 'scan' })"
      >Next
    </ImageButton>
    <div class="button-label">{{ t('common.next_label') }}</div>
  </main>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import ImageButton from '@/components/ImageButton.vue'

const router = useRouter()
const { t } = useI18n({ useScope: 'global' })

const textKeys = ['scan_intro_view.text_1', 'scan_intro_view.text_2', 'scan_intro_view.text_3']

// Ensures forced reset of the stored chart type selection
localStorage.removeItem('currentChart')
</script>

<style scoped>
main {
  background-image: url('/images/game_info_bg.svg');
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

.text-box-holder {
  position: absolute;
  top: 742px;
  left: 144px;
}

.text-box {
  float: left;
  width: 440px;
  letter-spacing: 1.04px;
  font-size: 26px;
  font-family: Lexend-Light;
  margin-right: 196px;
  white-space: pre-line;
}

.text-box:last-child {
  margin-right: 0;
}

.button {
  position: absolute;
  top: 968px;
  left: 928px;
}

.button-label {
  position: absolute;
  top: 1122px;
  left: 842px;
  width: 316px;
  text-align: center;
  letter-spacing: 3.08px;
  font-size: 22px;
}
</style>
