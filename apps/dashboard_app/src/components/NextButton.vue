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
import { useRouter } from 'vue-router'
import ImageButton from '@/components/ImageButton.vue'

const router = useRouter()

const props = defineProps({
  left: {
    type: String,
    default: '1816px'
  },
  top: {
    type: String,
    default: '1760px'
  },
  linkTo: {
    type: String,
    required: true
  },
  disabled: {
    type: Boolean,
    default: false
  }
})

const goNext = () => {
  if (!props.disabled) {
    router.push(props.linkTo)
  }
}
</script>

<template>
  <div class="next-button"
       :style="{position: 'absolute', top: props.top, left: props.left}">
    <ImageButton up-source="images/next_btn_up.svg"
                 down-source="images/next_btn_down.svg"
                 disabled-source="images/next_btn_disabled.svg"
                 :is-disabled="disabled"
                 @clicked="goNext"
    />
    <span :style="{color: disabled ? '#5E6166' : '#EBEBEB'}">{{ $t('ui.next') }}</span>
  </div>
</template>

<style scoped>
next-button {
  position: absolute;
  width: 208px;
  height: 208px;
}

.next-button span {
  display: block;
  position: relative;
  font-size: 36px;
  left: -16px;
  top: 44px;
  width: 240px;
  height: 70px;
  text-align: center;
  letter-spacing: 5.04px;
}
</style>
