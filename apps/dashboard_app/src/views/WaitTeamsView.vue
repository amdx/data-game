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
import { DotLottieVue } from '@lottiefiles/dotlottie-vue'
import { useApi, type Team } from '@/composables/useApi'
import { useErrorStore } from '@/composables/useErrorStore'
import MenuButton, { ButtonType } from '@/components/MenuButton.vue'
import NextButton from '@/components/NextButton.vue'
import TitleGroup from '@/components/TitleGroup.vue'

const api = useApi()
const errorStore = useErrorStore()

const teamNames = ref<String[] | null[]>([
  null,
  null,
  null,
  null,
  null
])
const activeTeams = ref(0)
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
    activeTeams.value = teams.length
    updatePlaceholders(teams)
  }
}

const updatePlaceholders = (teams: Team[]) => {
  for (let i = 0; i < teams.length && i < teamNames.value.length; i++) {
    teamNames.value[i] = teams[i].name
  }
}

onMounted(async () => {
  try {
    await api.setState('TEAM_NAMING')
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
      <TitleGroup node="wait_teams" />

      <DotLottieVue v-if="activeTeams != 5" class="spinner" autoplay loop
                    src="progress_animation_dashboard.json" />

      <div :class="['teams', { up: activeTeams == 5 }]">
        <div v-for="(teamName, index) in teamNames" :key="index" class="team">
          <div class="group-icon">
            <img v-if="teamName == null"
                 src="/images/group_check_in_waiting_icon.svg" />
            <img v-else src="/images/group_check_in_icon.svg" />
          </div>
          <span class="group-caption">{{ $t('wait_teams.group_caption') }}</span>
          <span class="group-name" :style="teamName != null ? {color: '#B0B5BF'} : ''">
            {{ teamName != null ? teamName : $t('wait_teams.not_checked_in') }}
          </span>
        </div>
      </div>

      <NextButton link-to="/scan" :disabled="activeTeams != 5" />
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
  left: 356px;
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
