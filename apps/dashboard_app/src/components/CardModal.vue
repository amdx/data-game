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
import { onMounted, ref } from 'vue'
import { type ScenarioId, useApi } from '@/composables/useApi'
import ImageButton from '@/components/ImageButton.vue'
import ModalWindow from '@/components/ModalWindow.vue'

defineProps({cardId: String, visible: Boolean})
const emit = defineEmits(['close'])

const api = useApi()

const currentScenarioId = ref<ScenarioId>()

onMounted(async () => {
  currentScenarioId.value = await api.getScenarioId()
})
</script>

<template>
  <ModalWindow :visible="visible" width="654px" height="1058px" :no-close-button="true">
        <img alt="Action Card" :src="`images/cards/${currentScenarioId}_${cardId}.png`" />
        <ImageButton
          class="close-button"
          down-source="images/close_card_btn_down.svg"
          up-source="images/close_card_btn_up.svg"
          @clicked="emit('close')"
        />
  </ModalWindow>
</template>

<style scoped>
.close-button {
  position: absolute;
  top: 47px;
  right: 47px;
}
</style>
