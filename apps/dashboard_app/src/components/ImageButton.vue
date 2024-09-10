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
import { computed, ref } from 'vue'

const props = defineProps({
  upSource: String,
  downSource: String,
  disabledSource: String,
  isDisabled: Boolean,
  padding: String
})
const emit = defineEmits(['clicked'])

const isButtonDown = ref(false)
const style = computed(() => {
  const attributes: Record<string, string> = {}

  if (props.isDisabled) {
    attributes['pointer-events'] = 'none'
  } else {
    attributes['cursor'] = 'pointer'
  }

  if (props.padding) {
    attributes['padding'] = props.padding
  }

  return attributes
})

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

<template>
  <div
    :style="style"
    @mousedown="handleMouseDown"
    @mouseup="handleMouseUp"
    @mouseleave="handleMouseLeave"
    @touchstart="handleTouchStart"
    @touchend="handleTouchEnd"
    @click="emit('clicked')"
  >
    <img :src="props.downSource" :hidden="!isButtonDown || isDisabled" />
    <img :src="props.upSource" :hidden="isButtonDown || isDisabled" />
    <img v-if="props.disabledSource" :src="props.disabledSource"
         :hidden="!isDisabled" />
  </div>
</template>

<style scoped>

</style>
