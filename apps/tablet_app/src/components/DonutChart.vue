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
  <div class="donut-chart">
    <div class="donut-holder" v-for="(item, index) in chartData" :key="index">
      <div class="donut">
        <Doughnut :data="{ datasets: [item] }" :options="chartOptions" />
      </div>
      <div class="donut-label">
        <span
          v-for="(lItem, lIndex) in getChartLabels(item)"
          :key="lIndex"
          :style="{ color: `${lItem.color}` }"
          >{{ lItem.text }}</span
        >
      </div>
      <CircleButton class="card-label" :label="cardLabels[index]" @clicked="onLabelClicked" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ArcElement, Chart as ChartJS } from 'chart.js'
import { Doughnut } from 'vue-chartjs'
import { computed } from 'vue'
import { backendHandler } from '@/utils/BackendHandler'
import { tabletConfig } from '@/utils/TabletConfig'
import CircleButton from '@/components/CircleButton.vue'

ChartJS.register(ArcElement)

const props = defineProps<{ categoryHiddenStates: boolean[] }>()

const emits = defineEmits(['card-label-clicked'])

const chartOptions = {
  normalized: true,
  responsive: true,
  cutout: 99,
  events: []
}

const chartData = computed<any[]>(() => {
  return backendHandler.getDonutGraphDatasets(
    !props.categoryHiddenStates[0] ? tabletConfig.timeColor : undefined,
    !props.categoryHiddenStates[1] ? tabletConfig.costColor : undefined,
    !props.categoryHiddenStates[2] ? tabletConfig.efficiencyColor : undefined
  )
})
const cardLabels = computed(() => {
  return backendHandler.getGraphLabels()
})

function getChartLabels(data: any) {
  const labels = []
  for (let i = 0; i < data.data.length - 1; i++) {
    labels.push({ color: data.backgroundColor[i], text: data.data[i] })
  }
  return labels
}

function onLabelClicked(card: string) {
  emits('card-label-clicked', card)
}
</script>

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

.donut-label {
  padding-top: 32px;
  text-align: center;
  font-family: Lexend-ExtraLight;
  font-size: 32px;
  white-space: pre-line;
}

.donut-label span {
  margin: 0 20px; /* Adjust the margin value as needed */
}

.card-label {
  margin-top: 35px;
  margin-left: 122px;
  text-align: center;
}
</style>
