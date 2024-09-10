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
import ErrorNotification from '@/components/ErrorNotification.vue'
import { setWasmUrl } from '@lottiefiles/dotlottie-vue'
import { useUserConfig } from '@/composables/useUserConfig'

const userConfig = useUserConfig()

setWasmUrl(userConfig.value!.dotlottie.wasmUrl)
</script>

<template>
  <div class="toplevel">
    <ErrorNotification />
    <RouterView v-slot="{ Component, route }">
      <transition name="fade" mode="out-in">
        <component :is="Component" :key="route.fullPath" class="main-div" />
      </transition>
    </RouterView>
  </div>
</template>

<style>
html, body {
  margin: 0 !important;
  padding: 0 !important;
  background-color: #191A1C;
  color: #ebebeb;
  font-family: Lexend-Light;
  user-select: none;
  width: 100%;
  height: 100%;
  overscroll-behavior: none;
}

.fullscreen-container {
  width: 3840px;
  height: 2160px;
  background-repeat: no-repeat;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

button {
  flex-shrink: 0;
  padding: 5px 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #ccc;
}
</style>
