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
  <div
    :class="isButtonDown ? 'button-style-down' : 'button-style-up'"
    @mousedown="handleMouseDown"
    @mouseup="handleMouseUp"
    @mouseleave="handleMouseLeave"
    @touchstart="handleTouchStart"
    @touchend="handleTouchEnd"
    @click="emits('clicked', props.label)"
  >
    {{ props.label }}
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{
  label: string | number
}>()

const emits = defineEmits(['clicked'])
const isButtonDown = ref(false)

const handleMouseDown = () => {
  isButtonDown.value = true
}

const handleMouseUp = () => {
  isButtonDown.value = false
}

const handleMouseLeave = () => {
  if (isButtonDown.value) {
    isButtonDown.value = false
  }
}

const handleTouchStart = () => {
  isButtonDown.value = true
}

const handleTouchEnd = () => {
  isButtonDown.value = false
}
</script>

<style scoped>
div {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  letter-spacing: 1.92px;
  font-size: 24px;
  font-family: Lexend-Light;
  white-space: pre-line;
}

.button-style-up {
  background-color: #2c2e30;
  color: #bfd4ff;
}

.button-style-down {
  background-color: #bed5fd;
  color: #1d1e20;
}
</style>
