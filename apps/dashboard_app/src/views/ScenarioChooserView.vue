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
import { useRouter } from 'vue-router'
import { useApi, type ScenarioId } from '@/composables/useApi'
import { useErrorStore } from '@/composables/useErrorStore'
import AboutModal from '@/components/AboutModal.vue'

const router = useRouter()
const api = useApi()
const errorStore = useErrorStore()

const showAbout = ref(false)

const selectScenario = async (scenario: ScenarioId) => {
  try {
    await api.startSession(scenario)
  } catch (error) {
    errorStore.setError(`Unable to set the scenario: ${error}`)
    return
  }
  try {
    await api.setState('INTRODUCTION')
  } catch (error) {
    errorStore.setError(`Unable to set state: ${error}`)
    return
  }
  await router.push('/welcome')
}
</script>

<template>
  <main>
    <div class="fullscreen-container">
      <div class="scenario-button" style="left: 936px; top: 1160px;"
           @click="selectScenario('001')">
        <span style="color: #76BBE3">{{ $t('scenarios.001.theme') }}</span>
      </div>
      <div class="scenario-button" style="left: 1640px; top: 1160px;"
           @click="selectScenario('003')">
        <span style="color: #F5A845">{{ $t('scenarios.003.theme') }}</span>
      </div>
      <div class="scenario-button" style="left: 2344px; top: 1160px;"
           @click="selectScenario('002')">
        <span style="color: #D1DE5F">{{ $t('scenarios.002.theme') }}</span>
      </div>

      <div class="hidden-button" @click="showAbout = true" />
      <AboutModal :visible="showAbout" @close="showAbout = false" />
    </div>
  </main>
</template>

<style scoped>
.fullscreen-container {
  background-image: url("/images/theme_selection_bg.svg");
}

.scenario-button {
  position: absolute;
  width: 560px;
  height: 144px;
  box-shadow: 0 0 5px #0000004D;
  border: 2px solid #121314;
  background-color: #1E1F21;
  border-radius: 8px;
  opacity: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.scenario-button span {
  display: block;
  font-size: 40px;
  text-align: center;
  letter-spacing: 1.6px;
}

.hidden-button {
  position: fixed;
  width: 100px;
  height: 100px;
  top: 0;
  right: 0;
}
</style>
