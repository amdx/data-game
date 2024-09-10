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
import ImageButton from '@/components/ImageButton.vue'

const props = defineProps<{
  visible: Boolean,
  width?: string,
  height?: string,
  left?: string,
  top?: string
  noCloseButton?: Boolean
  smallCloseButton?: Boolean
}>()
const emit = defineEmits(['close'])

const closeModal = () => {
  emit('close')
}
</script>

<template>
  <transition name="fade">
    <div v-if="visible" class="modal-overlay">
      <div class="modal-container" :style="{
           width: props.width || '1920px',
           height: props.height || '1128px',
           left: props.left || '50%',
           top: props.top || '50%',
           transform: props.left || props.top ? 'none' : 'translate(-50%, -50%)'
         }">
        <slot></slot>
        <ImageButton
          v-if="noCloseButton !== true"
          :up-source="props.smallCloseButton ? 'images/close_window_btn_small_up.svg' : 'images/close_window_btn_up.svg'"
          :down-source="props.smallCloseButton ? 'images/close_window_btn_small_down.svg' : 'images/close_window_btn_down.svg'"
          :style="{position: 'absolute', top: props.smallCloseButton ? '96px' : '80px', right: props.smallCloseButton ? '88px' : '72px'}"
          padding="20px"
          @clicked="closeModal"
        />
      </div>
    </div>
  </transition>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgb(29, 30, 32, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.modal-container {
  position: absolute;
  box-shadow: 0 0 30px #00000099;
  border-radius: 16px;
  background-color: #191A1C;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
