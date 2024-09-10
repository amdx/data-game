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
import { computed, onMounted, reactive, ref } from 'vue'
import { useApi } from '@/composables/useApi'
import { useErrorStore } from '@/composables/useErrorStore'
import { useUserConfig } from '@/composables/useUserConfig'
import DropdownMenu from '@/components/DropdownMenu.vue'
import TeamBarChart from '@/components/charts/TeamBarChart.vue'
import TeamRadarChart from '@/components/charts/TeamRadarChart.vue'
import TeamDoughnutsChart from '@/components/charts/TeamDoughnutsChart.vue'
import TeamTotalsChart from '@/components/charts/TeamTotalsChart.vue'
import TeamPolarChart from '@/components/charts/TeamPolarChart.vue'
import CardModal from '@/components/CardModal.vue'

const props = defineProps(['currentTeamIndex'])

const api = useApi()
const errorStore = useErrorStore()
const userConfig = useUserConfig()

const categoryData = reactive([
  {
    color: userConfig.value?.graphs.colors.time,
    textKey: 'charts.categories.time',
    picked: true
  },
  {
    color: userConfig.value?.graphs.colors.cost,
    textKey: 'charts.categories.cost',
    picked: true
  },
  {
    color: userConfig.value?.graphs.colors.efficiency,
    textKey: 'charts.categories.efficiency',
    picked: true
  }
])
const allTeamsData = ref()
const scenarioScores = ref()
const selectedTeamData = computed(() => {
  if (allTeamsData.value && props.currentTeamIndex !== undefined) {
    return allTeamsData.value[props.currentTeamIndex]
  } else {
    return null
  }
})
const currentGraphIndex = ref<number>(0)
const showModal = ref(false)
const pickedCard = ref('')

const categoryHiddenStates = computed(() => {
  return categoryData.map((c) => !c.picked)
})

const handleCategory = (index: number) => {
  categoryData[index].picked = !categoryData[index].picked
}

const handleGraphSelect = (index: number) => {
  resetView()
  currentGraphIndex.value = index
}

const resetView = () => {
  for (const category of categoryData) {
    category.picked = true
  }
}

const onLabelClicked = (label: string) => {
  showModal.value = true
  pickedCard.value = label
}

onMounted(async () => {
  try {
    allTeamsData.value = await api.getTeams()
    scenarioScores.value = await api.getScenarioScores()
  } catch (error) {
    errorStore.setError(`Cannot retrieve teams data or scenario scores: ${error}`)
    return
  }
})
</script>

<template>
  <DropdownMenu
    class="dropdown-menu"
    :items="[
      $t('charts.types.bar'),
      $t('charts.types.web'),
      $t('charts.types.doughnut'),
      $t('charts.types.polar'),
    ]"
    @select="handleGraphSelect"
  />

  <div class="category-bar">
    <div
      class="category-bar-item"
      v-for="(item, index) in categoryData"
      v-on:click="handleCategory(index)"
      :key="index"
    >
      <div
        class="category-dot"
        :style="{ 'background-color': `${categoryData[index].picked ? item.color : '#2C2E30'}` }"
      />
      <div :style="{ color: `${categoryData[index].picked ? '#8D9199' : '#5E6166'}` }">
        {{ $t(item.textKey) }}
      </div>
    </div>
  </div>
  <div class="hint">{{ $t('details.hint') }}</div>
  <div>
    <TeamBarChart
      class="bar-chart"
      v-if="currentGraphIndex === 0"
      :category-hidden-states="categoryHiddenStates"
      :team-data="selectedTeamData"
      :scenario-scores="scenarioScores"
      @card-label-clicked="onLabelClicked"
    ></TeamBarChart>
    <TeamRadarChart
      class="radar-chart"
      v-if="currentGraphIndex === 1"
      :category-hidden-states="categoryHiddenStates"
      :team-data="selectedTeamData"
      :scenario-scores="scenarioScores"
      @card-label-clicked="onLabelClicked"
    ></TeamRadarChart>
    <TeamDoughnutsChart
      class="doughnut-chart"
      v-if="currentGraphIndex === 2"
      :category-hidden-states="categoryHiddenStates"
      :team-data="selectedTeamData"
      :scenario-scores="scenarioScores"
      @card-label-clicked="onLabelClicked"
    ></TeamDoughnutsChart>
    <TeamPolarChart
      class="polar-chart"
      v-if="currentGraphIndex === 3"
      :category-hidden-states="categoryHiddenStates"
      :team-data="selectedTeamData"
      :scenario-scores="scenarioScores"
      @card-label-clicked="onLabelClicked"
    ></TeamPolarChart>
  </div>
  <TeamTotalsChart
    class="totals-chart"
    :team-data="selectedTeamData"
    :scenario-scores="scenarioScores" />
  <CardModal :visible="showModal" :card-id="pickedCard" @close="showModal = false" />
</template>

<style scoped>
.dropdown-menu {
  z-index: 2;
  position: absolute;
  top: 34px;
  left: 65px;
}

.category-bar {
  position: absolute;
  top: 144px;
  left: 88px;
  font-size: 26px;
  letter-spacing: 1.04px;
}

.category-bar-item {
  float: left;
  width: 184px;
}

.category-dot {
  height: 24px;
  width: 24px;
  border-radius: 50%;
  float: left;
  margin-right: 21px;
  margin-top: 4px;
}

.hint {
  position: absolute;
  top: 194px;
  left: 88px;
  letter-spacing: 1.76px;
  color: #8D9199;
  font-family: Lexend-ExtraLight;
  font-size: 22px;
}

.bar-chart {
  z-index: 1;
  position: absolute;
  top: 264px;
  left: 64px;
  display: inline-block;
}

.radar-chart {
  z-index: 1;
  position: absolute;
  top: 224px;
  left: 428px;
  display: inline-block;
}

.polar-chart {
  z-index: 1;
  position: absolute;
  top: 224px;
  left: 428px;
  display: inline-block;
}

.doughnut-chart {
  z-index: 1;
  position: absolute;
  top: 315px;
  left: 122px;
  display: inline-block;
}

.totals-chart {
  z-index: 1;
  position: absolute;
  top: 106px;
  left: 1624px;
  width: 304px;
  max-width: 304px;
  height: 1040px;
  max-height: 1040px;
  display: inline-block;
}
</style>
