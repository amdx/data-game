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
  <main>
    <div>
      <div class="group-name">{{ t('team_name_view.group_name') }}</div>
      <div class="text">{{ t('team_name_view.text') }}</div>
      <input
        ref="teamNameInput"
        v-on:keyup.enter="showNamePrompt"
        :maxlength="tabletConfig.maxTeamNameLength"
        v-model="teamName"
        style="text-transform:uppercase"
        :inputmode="isInput ? 'text' : 'none'"
        spellcheck="false"
        autocomplete="off"
        autocapitalize="off"
      />
    </div>
    <TabletPrompt
      :text="`${t('team_name_view.name_prompt')}\n\n${teamName.toUpperCase()}`"
      :has-cancel-button="true"
      v-model="isNamePrompt"
      @ok="sendTeamName"
      @cancel="focusInput"
    >
    </TabletPrompt>
    <TabletPrompt
      :text="`${t('common.error')}\n\n${errorText}`"
      :has-cancel-button="false"
      v-model="isErrorPrompt"
      @ok="focusInput"
    >
    </TabletPrompt>
    <TeamNameModal :team-name="teamName.toUpperCase()" v-model="isNameModal"></TeamNameModal>
  </main>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { backendHandler } from '@/utils/BackendHandler'
import TabletPrompt from '@/components/TabletPrompt.vue'
import { useI18n } from 'vue-i18n'
import { tabletConfig } from '@/utils/TabletConfig'
import TeamNameModal from '@/components/TeamNameModal.vue'

const { t } = useI18n()

const teamName = defineModel<string>({ default: '' })
const isLoading = ref<boolean>(false)
const isNamePrompt = ref(false)
const isErrorPrompt = ref(false)
const isNameModal = ref(false)
const errorText = ref('')
const teamNameInput = ref(null)

const isValid = computed(() => {
  return teamName.value && teamName.value.length > 0
})

const isInput = computed(() => {
  return !isNamePrompt.value && !isErrorPrompt.value && !isLoading.value
})

function showNamePrompt() {
  if (isValid.value) {
    isNamePrompt.value = true
  }
}

function sendTeamName() {
  isNameModal.value = true
  isLoading.value = true
  backendHandler
    .sendTeamName(teamName.value.toUpperCase())
    .then((data) => {
      backendHandler.teamId = data.data.team.id
      isLoading.value = false
    })
    .catch((error) => {
      console.error(error)
      isNameModal.value = false
      if (error.response) {
        errorText.value = error.response.data.detail
      } else {
        errorText.value = error.message
      }
      isErrorPrompt.value = true
      isLoading.value = false
    })
}

function focusInput() {
  if (teamNameInput.value) {
    // @ts-ignore
    teamNameInput.value.focus()
  }
}

onMounted(() => {
  focusInput()
})
</script>

<style lang="css" scoped>
input {
  position: absolute;
  top: 360px;
  left: 474px;
  width: 1045px;
  height: 119px;
  border-radius: 39px;
  text-align: center;
  font-size: 60px;
  font-family: Lexend-Light;
  color: #1d1e20;
}

.group-name {
  position: absolute;
  top: 83px;
  left: 144px;
  width: 576px;
  letter-spacing: 4.8px;
  font-size: 60px;
  font-family: Lexend-Light;
  white-space: pre-line;
}

.text {
  position: absolute;
  top: 154px;
  left: 144px;
  width: 840px;
  letter-spacing: 1.52px;
  font-size: 38px;
  font-family: Lexend-ExtraLight;
  white-space: pre-line;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
