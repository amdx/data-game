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
import { ref } from 'vue'

const props = withDefaults(defineProps<{
  id: string,
  label?: string,
  flipText?: boolean
}>(), {
  flipText: false
})
const emit = defineEmits(['clicked'])

const isButtonDown = ref(false)
</script>

<template>
  <div class="button-container"
       @mousedown="isButtonDown = true"
       @mouseup="isButtonDown = false"
       @mouseleave="isButtonDown = false"
       @touchstart="isButtonDown = true"
       @touchend="isButtonDown = false"
       @click="emit('clicked', props.id)"
  >
    <div v-if="label && flipText" class="button-label left">{{ label }}</div>
    <div :class="['button-circle', isButtonDown ? 'button-style-down' : 'button-style-up']">
      {{ props.id }}
    </div>
    <div v-if="label && !flipText" class="button-label right">{{ label }}</div>
  </div>
</template>

<style scoped>
.button-container {
  display: flex;
  align-items: center;
  letter-spacing: 1.92px;
  font-size: 24px;
}

.button-circle {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.button-label {
  font-size: 20px;
  width: 140px;
  color: #8D9199;
}

.button-label.right {
  margin-left: 22px;
  text-align: left;
}

.button-label.left {
  margin-right: 22px;
  text-align: right;
}

.button-style-up {
  background-color: #2C2E30;
  color: #BFD4FF;
}

.button-style-down {
  background-color: #BED5FD;
  color: #1D1E20;
}
</style>
