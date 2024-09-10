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
import 'chart.js/auto'
import { Doughnut } from 'vue-chartjs'
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useUserConfig } from '@/composables/useUserConfig'
import type { ChartOptions } from 'chart.js'
import type { ActionCard } from '@/client'

const props = defineProps(['teamData', 'scenarioScores'])

const userConfig = useUserConfig()

const { t } = useI18n({ useScope: 'global' })
const chartOptions: ChartOptions<'doughnut'> = {
  normalized: true,
  responsive: true,
  cutout: '85%',
  events: []
}
const chartLabels = [
  t('charts.overall.time'),
  t('charts.overall.cost'),
  t('charts.overall.efficiency')
]

const chartData = computed(() => {
  if (!props.teamData || !props.scenarioScores) {
    return []
  }

  const datasets = []
  for (const category of userConfig.value!.graphs.categories) {
    const value = Math.round(props.teamData.action_cards
      .map((card: ActionCard) => card[category])
      .reduce((a: number, b: number) => a + b) / props.scenarioScores.best[category] * 100)

    const dataset = {
      data: [value, 100 - value],
      backgroundColor: [userConfig.value!.graphs.colors[category], '#2D2C30'],
      borderWidth: 0
    }

    datasets.push(dataset)
  }

  return datasets
})
</script>

<template>
  <div v-if="chartData">
    <div class="donut-holder" v-for="(item, index) in chartData" :key="index">
      <div class="donut-value">
        <span :style="{ color: `${item.backgroundColor[0]}` }">{{ item.data[0] }}</span>
      </div>
      <div class="donut">
        <Doughnut :data="{ datasets: [item] }" :options="chartOptions" />
      </div>
      <div class="donut-label">
        <span>{{ chartLabels[index] }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.donut-holder {
  float: left;
  display: block;
  width: 319px;
  height: 330px;
  align-items: center;
}

.donut {
  display: block;
  padding-left: 74px;
  width: 170px;
  height: 170px;
}

.donut-value {
  position: absolute;
  display: grid;
  padding-left: 74px;
  width: 170px;
  height: 170px;
  align-items: center;
  text-align: center;
  font-family: Lexend-ExtraLight;
  font-size: 42px;
  letter-spacing: 3.36px;
  white-space: pre-line;
}

.donut-label {
  padding-top: 32px;
  text-align: center;
  font-family: Lexend-ExtraLight;
  font-size: 24px;
  letter-spacing: 1.92px;
  white-space: pre-line;
}

.donut-label span {
  margin: 0 10px;
}
</style>
