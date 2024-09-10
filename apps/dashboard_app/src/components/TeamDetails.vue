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
import { ref } from 'vue'
import ImageButton from '@/components/ImageButton.vue'
import TeamDetailsChartsContainer from '@/components/TeamDetailsChartsContainer.vue'

const props = defineProps(['initialTeamIndex', 'teamEvaluation'])

const currentTeamIndex = ref(props.initialTeamIndex)

const gotoTeam = (index: number) => {
  currentTeamIndex.value = index
}

const previousTeam = () => {
  if (currentTeamIndex.value > 0) {
    currentTeamIndex.value -= 1
  }
}

const nextTeam = () => {
  if (currentTeamIndex.value < props.teamEvaluation.team_names.length - 1) {
    currentTeamIndex.value += 1
  }
}
</script>

<template>
  <div class="header">
    <span class="group-caption">{{ $t('details.group_caption') }}</span>
    <span class="group-name">{{ teamEvaluation.team_names[currentTeamIndex] }}</span>
  </div>
  <div class="midsection">
    <div class="navigation left">
      <ImageButton
        v-if="currentTeamIndex > 0"
        class="previous-button"
        down-source="images/chart_previous_btn_down.svg"
        up-source="images/chart_previous_btn_up.svg"
        padding="40px"
        @clicked="previousTeam()" />
    </div>
    <div class="content">
      <TeamDetailsChartsContainer :current-team-index="currentTeamIndex" />
    </div>
    <div class="navigation">
      <ImageButton
        v-if="currentTeamIndex < teamEvaluation.team_names.length - 1"
        class="next-button"
        down-source="images/chart_next_btn_down.svg"
        up-source="images/chart_next_btn_up.svg"
        padding="40px"
        @clicked="nextTeam()" />
    </div>
  </div>
  <div class="pagination">
    <div
      v-for="(team, index) in teamEvaluation.team_names"
      :key="index"
      :class="['circle', { active: index === currentTeamIndex }]"
      @click="gotoTeam(index)"
    />
  </div>
</template>

<style scoped>
.header {
  width: 100%;
  height: 168px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.group-caption {
  position: absolute;
  font-family: Lexend;
  font-size: 22px;
  letter-spacing: 2.64px;
  color: #5E6166;
  top: 66px;
}

.group-name {
  position: absolute;
  font-size: 36px;
  letter-spacing: 2.88px;
  color: #B0B5BF;
  top: 100px;
}

.midsection {
  width: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
}

.navigation {
  width: 192px;
  display: flex;
  justify-content: center;
}

.previous-button {
  margin-left: 8px;
}

.next-button {
  margin-right: 8px;
}

.content {
  position: relative;
  width: 2000px;
  height: 1200px;
}

.pagination {
  height: 168px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 30px;
  margin-top: 19px;
}

.circle {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background-color: #27292B;
  cursor: pointer;
}

.circle.active {
  background-color: #BFD4FF;
}
</style>