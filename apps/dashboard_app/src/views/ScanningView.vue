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
import { onMounted, onUnmounted, ref } from 'vue'
import { useApi, type Team } from '@/composables/useApi'
import { useErrorStore } from '@/composables/useErrorStore'
import MenuButton, { ButtonType } from '@/components/MenuButton.vue'
import { DotLottieVue } from '@lottiefiles/dotlottie-vue'
import NextButton from '@/components/NextButton.vue'
import TitleGroup from '@/components/TitleGroup.vue'

const api = useApi()
const errorStore = useErrorStore()

const teamNames = ref<String[]>()
const activeTeams = ref(0)
const readyTeams = ref([false, false, false, false, false])

let intervalId: number

const poll = async () => {
  let teams
  try {
    teams = await api.getTeams()
  } catch (error) {
    errorStore.setError(`Cannot get teams information: ${error}`)
    return
  }

  if (teams) {
    teamNames.value = teams.map((team) => team.name)
    activeTeams.value = teams.length
    readyTeams.value = teams.map((team: Team) => team.has_all_cards)
  }
}

onMounted(async () => {
  try {
    await api.setState('SCANNING')
  } catch (error) {
    errorStore.setError(`Cannot set session state: ${error}`)
    return
  }

  await poll()
  intervalId = window.setInterval(poll, 1000)
})

onUnmounted(() => {
  if (intervalId) {
    clearInterval(intervalId)
  }
})
</script>

<template>
  <main>
    <div class="fullscreen-container">
      <TitleGroup node="scanning" />

      <DotLottieVue v-if="!readyTeams.every(value => value)" class="spinner" autoplay
                    loop
                    src="progress_animation_dashboard.json" />

      <div :class="['teams', {up: readyTeams.every(value => value)}]">
        <div v-for="(teamName, index) in teamNames" :key="index" class="team">
          <div class="group-icon">
            <img v-if="!readyTeams[index]"
                 src="/images/group_check_in_waiting_icon.svg" />
            <img v-else src="/images/group_check_in_icon.svg" />
          </div>
          <span class="group-caption">{{ $t('wait_teams.group_caption') }}</span>
          <span class="group-name" :style="readyTeams[index] ? {color: '#B0B5BF'} : ''">
            {{ teamName }}
          </span>
        </div>
      </div>

      <NextButton link-to="/evaluation" :disabled="!readyTeams.every(value => value)" />
      <MenuButton :buttons="[ButtonType.RESET, ButtonType.GOODBYE]" />
    </div>
  </main>
</template>

<style scoped>
.spinner {
  position: absolute;
  left: 1720px;
  top: 588px;
  width: 400px;
  height: 400px;
}

.teams {
  display: flex;
  justify-content: center;
  position: absolute;
  width: 100%;
  top: 1176px;
  gap: 8px;
  transition: top 800ms ease-in-out;
}

.up {
  top: 880px;
}

.team {
  width: 620px;
}

.group-icon {
  display: flex;
  justify-content: center;
  width: 100%;
}

.team img {
  max-width: 100%;
  height: auto;
}

.group-caption {
  display: block;
  position: relative;
  font-family: Lexend;
  font-size: 27px;
  letter-spacing: 3.24px;
  color: #5E6166;
  text-align: center;
  top: 30px;
}

.group-name {
  display: block;
  position: relative;
  font-family: Lexend-Light;
  font-size: 44px;
  text-align: center;
  letter-spacing: 3.52px;
  color: #5E6166;
  top: 33px;
}
</style>
