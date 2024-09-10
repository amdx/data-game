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
import { useUserConfig } from '@/composables/useUserConfig'
import CircleButton from '@/components/CircleButton.vue'
import { computed } from 'vue'
import type { ChartDataset, ChartOptions } from 'chart.js'

const props = defineProps(['teamEvaluation', 'categoryFilterFlags'])
const emit = defineEmits(['datasetClicked'])

const userConfig = useUserConfig()

const chartOptions: ChartOptions<'doughnut'> = {
  normalized: true,
  responsive: true,
  cutout: '82%',
  events: []
}

const datasets = computed(() => {
  const datasets: ChartDataset<'doughnut'>[] = []

  if (!userConfig.value) {
    return datasets
  }

  for (const index in props.teamEvaluation.team_names) {
    let cutOutValue = 0
    const data = []
    const backgroundColor = []
    const borderWidth = []

    for (const category of userConfig.value!.graphs.categories) {
      if (props.categoryFilterFlags[category]) {
        const value = props.teamEvaluation.teams_evaluation[category][index]
        data.push(value)
        cutOutValue += 100 - value
        backgroundColor.push(userConfig.value?.graphs.colors[category])
        borderWidth.push(0)
      }
    }

    data.push(cutOutValue)
    backgroundColor.push('#2D2C30')
    borderWidth.push(0)

    datasets.push({
      data,
      backgroundColor,
      borderWidth
    })
  }

  return datasets
})

const getChartValues = (dataset: any) => {
  const values = []
  for (let i = 0; i < dataset.data.length - 1; i++) {
    values.push({ color: dataset.backgroundColor[i], text: dataset.data[i] })
  }
  return values
}
</script>

<template>
  <div class="charts-container">
    <div v-for="(dataset, index) in datasets"
         :key="index"
         class="chart">
      <Doughnut
        :options="chartOptions"
        :data="{datasets: [dataset]}"
      />
      <div class="values">
        <div v-for="(valueDef, valueIndex) in getChartValues(dataset)" :key="valueIndex"
             class="value">
          <span :style="{color: valueDef.color}">
            {{ valueDef.text }}
          </span>
        </div>
      </div>
    </div>
  </div>
  <div class="card-label-holder">
    <CircleButton
      class="card-label"
      v-for="(item, index) in teamEvaluation.team_names"
      :key="index"
      :id="`${index + 1}`"
      :label="item"
      @clicked="emit('datasetClicked', index)"
    ></CircleButton>
  </div>
</template>

<style scoped>
.charts-container {
  position: absolute;
  display: flex;
  justify-content: space-between;
  align-content: center;
  width: 1348px;
  height: 710px;
  top: 394px;
  left: 96px;
}

.chart {
  width: 192px;
  height: 192px;
}

.values {
  position: relative;
  display: flex;
  justify-content: center;
  gap: 28px;
  top: 22px;
  width: 192px;
}

.value {
  font-family: Lexend-ExtraLight;
  font-size: 28px;
  letter-spacing: 2.24px
}

.card-label-holder {
  display: flex;
  justify-content: space-between;
  position: absolute;
  width: 1374px;
  top: 680px;
  left: 160px;
}

</style>