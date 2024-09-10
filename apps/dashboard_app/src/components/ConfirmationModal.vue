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
import ModalWindow from '@/components/ModalWindow.vue'

defineProps(['text', 'visible'])
const emit = defineEmits(['confirm', 'cancel'])

const confirm = () => {
  emit('confirm')
}

const cancel = () => {
  emit('cancel')
}
</script>

<template>
  <ModalWindow :visible="visible" top="664px" left="1376px" width="1096px"
               height="800px" :no-close-button="true">
    <span class="text">{{ text }}</span>

    <div class="button" style="left: 121px; top: 376px">
      <ImageButton down-source="images/cancel_btn_down.svg"
                   up-source="images/cancel_btn_up.svg" @clicked="cancel" />
      <span class="caption">{{ $t('ui.cancel') }}</span>
    </div>
    <div class="button" style="left: 601px; top: 376px">
      <ImageButton down-source="images/confirm_btn_down.svg"
                   up-source="images/confirm_btn_up.svg" @clicked="confirm" />
      <span class="caption">{{ $t('ui.confirm') }}</span>
    </div>
  </ModalWindow>
</template>

<style scoped>
.text {
  position: relative;
  font-family: Lexend-Light;
  font-size: 44px;
  letter-spacing: 1.76px;
  left: 152px;
  top: 124px;
}

.button {
  position: absolute;
  width: 366px;
  text-align: center;
}

.caption {
  display: block;
  position: relative;
  font-family: Lexend-Light;
  font-size: 36px;
  text-align: center;
  letter-spacing: 5.04px;
  top: 44px;
}
</style>
