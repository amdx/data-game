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
import MenuButton, { ButtonType } from '@/components/MenuButton.vue'
import NextButton from '@/components/NextButton.vue'
import ModalWindow from '@/components/ModalWindow.vue'
import TitleGroup from '@/components/TitleGroup.vue'

const api = useApi()
const errorStore = useErrorStore()

const currentScenarioId = ref<ScenarioId>()
const heroes = computed(() => {
  return [1, 2, 3, 4].map((index) => {
    return `images/heroes/${currentScenarioId.value}_${index}.svg`
  })
})
const showModal = ref(false)
const selectedIndex = ref<number>()

const openModal = (index: number) => {
  selectedIndex.value = index
  showModal.value = true
}

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
    <div class="fullscreen-container">
      <TitleGroup node="heroes" />

      <span class="text">{{ $t('heroes.text') }}</span>

      <div class="gallery">
        <div v-for="(hero, index) in heroes" :key="index">
          <img @click="openModal(index)" class="hero" :src="hero" alt="Hero" />
        </div>
      </div>

      <ModalWindow v-if="selectedIndex != null"
                   :visible="showModal"
                   top="448px"
                   left="960px"
                   @close="showModal = false">
        <img :src="heroes[selectedIndex]" alt="Hero" />
        <span class="modal-text">
          {{ $t(`heroes.modal.${currentScenarioId}.${selectedIndex + 1}`) }}
        </span>
      </ModalWindow>

      <NextButton link-to="/teams" />
      <MenuButton :buttons="[ButtonType.RESET, ButtonType.GOODBYE]" />
    </div>
  </main>
</template>

<style scoped>
.text {
  position: absolute;
  font-size: 44px;
  letter-spacing: 1.76px;
  line-height: 64px;
  top: 1661px;
  left: 352px;
  width: 1176px;
  height: 420px;
}

.gallery {
  position: absolute;
  display: flex;
  justify-content: space-between;
  gap: 16px;
  left: 360px;
  top: 464px;
}

.hero {
  cursor: pointer;
}

.modal-text {
  position: absolute;
  font-size: 44px;
  letter-spacing: 1.76px;
  line-height: 64px;
  top: 221px;
  left: 824px;
  width: 864px;
  height: 796px;
}
</style>
