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
import { computed, onMounted, ref } from 'vue'
import { type ScenarioId, useApi } from '@/composables/useApi'
import { useErrorStore } from '@/composables/useErrorStore'
import NextButton from '@/components/NextButton.vue'
import MenuButton, { ButtonType } from '@/components/MenuButton.vue'
import ModalWindow from '@/components/ModalWindow.vue'

const api = useApi()
const errorStore = useErrorStore()

const showModal = ref(false)
const currentScenarioId = ref<ScenarioId>()
const scenarioBackground = computed(() => {
  const backgroundMap: { [key in ScenarioId]: string } = {
    '001': 'url("images/intro_scene_bg_mobilitaet.svg")',
    '002': 'url("images/intro_scene_bg_artenvielfalt.svg")',
    '003': 'url("images/intro_scene_bg_klima.svg")'
  }

  if (currentScenarioId.value) {
    return { backgroundImage: backgroundMap[currentScenarioId.value] || '' }
  } else {
    return {}
  }
})

onMounted(async () => {
  try {
    currentScenarioId.value = await api.getScenarioId()
  } catch (error) {
    errorStore.setError(`Cannot read current scenario: ${error}`)
  }
})
</script>

<template>
  <main>
    <div v-if="currentScenarioId" class="fullscreen-container"
         :style="scenarioBackground">
      <span class="title">{{ $t('welcome.title') }}</span>
      <span class="text">
        {{ $t(`scenarios.${currentScenarioId}.welcome`) }}
      </span>

      <div class="ai-info-clickbox" @click="showModal = true" />

      <ModalWindow :visible="showModal" width="1984px" height="1704px" left="936px"
                   top="256px" @close="showModal = false">
        <img src="/images/AI_info_header_graphic.svg" />
        <span class="modal-title">{{ $t('welcome.modal.title') }}</span>
        <span class="modal-text">
          {{ $t('welcome.modal.text') }}
        </span>
      </ModalWindow>

      <NextButton link-to="/instructions" />
      <MenuButton :buttons="[ButtonType.RESET, ButtonType.GOODBYE]" />
    </div>
  </main>
</template>

<style scoped>
.title {
  position: absolute;
  font-size: 138px;
  font-family: Lexend-Extralight;
  line-height: 168px;
  top: 718px;
  left: 1216px;
  width: 1345px;
  height: 341px;
  letter-spacing: 11.04px;
  color: #FFFFFF;
}

.text {
  position: absolute;
  font-size: 48px;
  font-family: Lexend-Extralight;
  line-height: 64px;
  top: 1184px;
  left: 1648px;
  width: 974px;
  height: 361px;
  text-align: left;
  letter-spacing: 1.92px;
  white-space: pre-line;
  color: #FFFFFF;
}

.ai-info-clickbox {
  position: absolute;
  width: 600px;
  height: 400px;
  right: 0;
  bottom: 0;
  pointer-events: auto;
  cursor: pointer;
}

.modal-title {
  display: block;
  position: relative;
  top: 172px;
  font-size: 108px;
  text-align: center;
  letter-spacing: 8.64px;
}

.modal-text {
  display: block;
  position: relative;
  left: 176px;
  top: 300px;

  width: 1655px;
  height: 485px;
  font-size: 44px;
  text-align: left;
  white-space: pre-line;
  letter-spacing: 1.76px;
  line-height: 64px;
}
</style>
