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
import { computed } from 'vue'
import 'chart.js/auto'
import { Doughnut } from 'vue-chartjs'
import type { ChartOptions } from 'chart.js'
import type { ActionCard } from '@/client'
import { useUserConfig } from '@/composables/useUserConfig'
import CircleButton from '@/components/CircleButton.vue'

const props = defineProps(['categoryHiddenStates', 'teamData', 'scenarioScores'])
const emit = defineEmits(['cardLabelClicked'])

const userConfig = useUserConfig()

const chartOptions: ChartOptions<'doughnut'> = {
  normalized: true,
  responsive: true,
  cutout: '85%',
  events: []
}

const allBackgroundColors = [
  userConfig.value?.graphs.colors.time,
  userConfig.value?.graphs.colors.cost,
  userConfig.value?.graphs.colors.efficiency,
  '#2D2C30'
]

const calculateDatapoints = (index: number) => {
  const actionCard = props.teamData.action_cards[index]
  const data = []
  let cutOutValue = 0

  for (const [index, category] of userConfig.value!.graphs.categories.entries()) {
    if (!props.categoryHiddenStates[index]) {
      const value = Math.round(actionCard[category] / props.scenarioScores.maxima[category] * 100)
      cutOutValue += 100 - value
      data.push(value)
    }
  }

  data.push(cutOutValue)

  return data
}
const labels = computed(() => {
  if (!props.teamData) {
    return []
  }

  return props.teamData.action_cards.map((card: ActionCard) => String(card.card_number))
})
const datasets = computed(() => {
  if (!props.teamData || !props.scenarioScores) {
    return []
  }

  const backgroundColors = allBackgroundColors.filter((_, index) => !props.categoryHiddenStates[index])

  return labels.value.map((_: unknown, index: number) => {
    return {
      borderWidth: 0,
      backgroundColor: backgroundColors,
      data: calculateDatapoints(index)
    }
  })
})

function getChartValues(dataset: any) {
  const values = []
  for (let i = 0; i < dataset.data.length - 1; i++) {
    values.push({ color: dataset.backgroundColor[i], text: dataset.data[i] })
  }
  return values
}

function onLabelClicked(card: string) {
  emit('cardLabelClicked', card)
}
</script>

<template>
  <div v-if="datasets" class="donut-chart">
    <div class="donut-holder" v-for="(dataset, index) in datasets" :key="index">
      <div class="donut">
        <Doughnut :data="{ datasets: [dataset] }" :options="chartOptions" />
      </div>
      <div class="donut-values">
        <span
          v-for="(valueDef, valueIndex) in getChartValues(dataset)"
          :key="valueIndex"
          :style="{ color: `${valueDef.color}` }"
        >{{ valueDef.text }}</span
        >
      </div>
      <CircleButton class="card-label" :id="labels[index]" @clicked="onLabelClicked" />
    </div>
  </div>
</template>

<style scoped>
.donut-chart {
  width: 1276px;
  max-width: 1276px;
  height: 660px;
  max-height: 660px;
}

.donut-holder {
  float: left;
  display: block;
  width: 319px;
  height: 435px;
  align-items: center;
}

.donut {
  display: block;
  padding-left: 50px;
  width: 220px;
  height: 220px;
}

.donut-values {
  padding-top: 32px;
  text-align: center;
  font-family: Lexend-ExtraLight;
  font-size: 32px;
  white-space: pre-line;
}

.donut-values span {
  margin: 0 20px;
}

.card-label {
  margin-top: 35px;
  margin-left: 122px;
  text-align: center;
}
</style>
