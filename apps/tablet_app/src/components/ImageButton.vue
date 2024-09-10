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
    :style="isDisabled ? 'pointer-events: none;' : ''"
    @mousedown="handleMouseDown"
    @mouseup="handleMouseUp"
    @mouseleave="handleMouseLeave"
    @touchstart="handleTouchStart"
    @touchend="handleTouchEnd"
    @click="emits('clicked')"
  >
    <img :src="props.downSource" :hidden="!isButtonDown || isDisabled" />
    <img :src="props.upSource" :hidden="isButtonDown || isDisabled" />
    <img v-if="props.disabledSource" :src="props.disabledSource" :hidden="!isDisabled" />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{
  upSource: string
  downSource: string
  disabledSource: string
  isDisabled: boolean
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

<style scoped></style>
