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
import { onMounted, type Ref, ref } from 'vue'
import { type Category } from '@/composables/useUserConfig'
import { useApi } from '@/composables/useApi'
import { useErrorStore } from '@/composables/useErrorStore'
import MenuButton, { ButtonType } from '@/components/MenuButton.vue'
import CategoriesFilter from '@/components/CategoriesFilter.vue'
import ModalWindow from '@/components/ModalWindow.vue'
import TeamDetails from '@/components/TeamDetails.vue'
import OverviewChartWrapper from '@/components/charts/OverviewChartWrapper.vue'
import OverviewBarChart from '@/components/charts/OverviewBarChart.vue'
import OverviewDoughnutsChart from '@/components/charts/OverviewDoughnutsChart.vue'
import OverviewRadarChart from '@/components/charts/OverviewRadarChart.vue'
import OverviewPolarChart from '@/components/charts/OverviewPolarChart.vue'
import OverviewTotalsChart from '@/components/charts/OverviewTotalsChart.vue'

const api = useApi()
const errorStore = useErrorStore()

const teamEvaluation = ref()
const categoryFilterFlags: Ref<{ [key in Category]: boolean }> = ref({
  time: true,
  cost: true,
  efficiency: true
})
const showDetailsModal = ref(false)
const requestedTeamIndex = ref(0)

const toggleCategoryFilter = (category: Category) => {
  categoryFilterFlags.value[category] = !categoryFilterFlags.value[category]
}

const getTeamDetails = (index: number) => {
  requestedTeamIndex.value = index
  showDetailsModal.value = true
}

onMounted(async () => {
  try {
    await api.setState('EVALUATION')
  } catch (error) {
    errorStore.setError(`Cannot set session state: ${error}`)
    return
  }

  try {
    teamEvaluation.value = await api.getEvaluation()
  } catch (error) {
    errorStore.setError(`Cannot retrieve evaluation: ${error}`)
    return
  }
})
</script>

<template>
  <main>
    <div class="fullscreen-container">
      <div v-if="teamEvaluation" class="layout-container">
        <div class="grid">
          <div class="chart">
            <OverviewChartWrapper :title="$t('charts.types.bar')">
              <OverviewBarChart :team-evaluation="teamEvaluation"
                                :category-filter-flags="categoryFilterFlags"
                                @dataset-clicked="getTeamDetails" />
            </OverviewChartWrapper>
          </div>
          <div class="chart">
            <OverviewChartWrapper :title="$t('charts.types.doughnut')">
              <OverviewDoughnutsChart :team-evaluation="teamEvaluation"
                                      :category-filter-flags="categoryFilterFlags"
                                      @dataset-clicked="getTeamDetails" />
            </OverviewChartWrapper>
          </div>
          <div class="chart">
            <OverviewChartWrapper :title="$t('charts.types.web')">
              <OverviewRadarChart :team-evaluation="teamEvaluation"
                                  :category-filter-flags="categoryFilterFlags"
                                  @dataset-clicked="getTeamDetails" />
            </OverviewChartWrapper>
          </div>
          <div class="chart">
            <OverviewChartWrapper :title="$t('charts.types.polar')">
              <OverviewPolarChart :team-evaluation="teamEvaluation"
                                  :category-filter-flags="categoryFilterFlags"
                                  @dataset-clicked="getTeamDetails" />
            </OverviewChartWrapper>
          </div>
        </div>
        <div class="sidebar">
          <OverviewTotalsChart :values="teamEvaluation.totals_evaluation"
                               class="overview-chart" />
          <CategoriesFilter :category-filter-flags="categoryFilterFlags"
                            @click="(category) => toggleCategoryFilter(category)"
                            class="categories-filter" />
          <div class="annotation">
            {{ $t('charts.annotation') }}
          </div>
        </div>
      </div>
      <div v-else style="font-size: 108px">Loading data..</div>
      <ModalWindow :visible="showDetailsModal" @close="showDetailsModal = false"
                   width="2384px" height="1536px" :small-close-button="true">
        <TeamDetails :team-evaluation="teamEvaluation"
                     :initial-team-index="requestedTeamIndex" />
      </ModalWindow>

      <MenuButton
        :buttons="[ButtonType.RESET, ButtonType.RESTART_SCAN, ButtonType.GOODBYE]" />
    </div>
  </main>
</template>

<style scoped>
.layout-container {
  display: grid;
  grid-template-columns: 1fr auto;
  height: 100vh;
  width: 100vw;
  box-sizing: border-box;
  padding: 48px;
  background-color: #121314;
}

.grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  gap: 48px;
  padding-right: 48px;
  padding-left: 8px;
}

.chart {
  width: 1536px;
  height: 1008px;
  display: flex;
  border-radius: 8px;
  background-color: #191A1C;
}

.sidebar {
  display: flex;
  flex-direction: column;
  width: 560px;
  height: 2064px;
  margin-right: 56px;
  background-color: #191A1C;
  border-radius: 8px;
}

.overview-chart {
  height: 1116px;
  padding-top: 180px;
}

.categories-filter {
  height: 390px;
  padding-top: 134px;
}

.annotation {
  position: absolute;
  font-family: Lexend-ExtraLight;
  font-size: 24px;
  text-align: center;
  letter-spacing: 1.92px;
  line-height: 34px;
  color: #8D9199;
  top: 1990px;
  width: inherit;
  white-space: pre-line;
}
</style>
