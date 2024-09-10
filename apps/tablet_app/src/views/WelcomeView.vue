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
  <main :style="{ backgroundImage: 'url(images/intro_bg_' + scenarioId + '.jpg)' }">
    <div class="welcome">{{ $t('welcome_view.welcome') }}</div>
    <div class="text">{{ $t('welcome_view.text_' + backendHandler.scenarioId) }}</div>
    <ImageButton
      class="button"
      up-source="images/next_btn_up.svg"
      down-source="images/next_btn_down.svg"
      disabled-source=""
      :is-disabled="false"
      @click="router.replace({ name: 'teamName' })"
      >Next
    </ImageButton>
    <div class="button-label">{{ $t('common.next_label') }}</div>
  </main>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { backendHandler } from '@/utils/BackendHandler'
import { onMounted, onUnmounted, ref } from 'vue'
import { eventBus } from '@/utils/EventBus'
import ImageButton from '@/components/ImageButton.vue'

const router = useRouter()

const scenarioId = ref(backendHandler.scenarioId)

onMounted(() => {
  eventBus.on('newState', onNewSessionState)
})

onUnmounted(() => {
  eventBus.off('newState', onNewSessionState)
})

function onNewSessionState(): void {
  scenarioId.value = backendHandler.scenarioId
}
</script>

<style scoped>
main {
  background-size: cover; /* This makes sure the image covers the entire element */
  height: 100vh; /* Set the height to 100% of the viewport height */
  color: white; /* If your image is dark, make the text color white for better contrast */
  display: flex;
}

.welcome {
  position: absolute;
  top: 364px;
  left: 608px;
  width: 752px;
  letter-spacing: 6.08px;
  color: #ffffff;
  font-size: 76px;
  font-family: Lexend-ExtraLight;
  white-space: pre-line;
}

.text {
  position: absolute;
  top: 622px;
  left: 608px;
  width: 760px;
  letter-spacing: 1.04px;
  font-size: 26px;
  font-family: Lexend-Light;
  white-space: pre-line;
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
