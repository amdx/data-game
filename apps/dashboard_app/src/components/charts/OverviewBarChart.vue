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
import { Bar } from 'vue-chartjs'
import { useUserConfig } from '@/composables/useUserConfig'
import CircleButton from '@/components/CircleButton.vue'
import type { ChartDataset, ChartOptions } from 'chart.js'

const props = defineProps(['teamEvaluation', 'categoryFilterFlags'])
const emit = defineEmits(['datasetClicked'])

const userConfig = useUserConfig()

const chartOptions: ChartOptions<'bar'> = {
  normalized: true,
  responsive: true,
  maintainAspectRatio: false,
  events: [],
  plugins: {
    legend: {
      display: false
    }
  },
  scales: {
    y: {
      ticks: {
        font: {
          family: 'Lexend-Light',
          size: 22
        },
        color: '#B0B5BF',
        padding: 32,
        callback: function(value: any, index: any) {
          // Display only every second tick
          return index % 2 === 0 ? value : ''
        }
      },
      min: 0,
      max: 100,
      grid: {
        color: '#3C3F43'
      },
      border: {
        display: false
      }
    },
    x: {
      display: false
    }
  }
}

const chartData = computed(() => {
  const datasets: ChartDataset<'bar'>[] = []

  for (const category of userConfig.value!.graphs.categories) {
    if (props.categoryFilterFlags[category]) {
      datasets.push({
        backgroundColor: userConfig.value?.graphs.colors[category],
        barPercentage: 0.75,
        categoryPercentage: 0.5,
        data: props.teamEvaluation.teams_evaluation[category]
      })
    }
  }

  return {
    labels: props.teamEvaluation.team_names,
    datasets: datasets
  }
})
</script>

<template>
  <div class="chart-holder">
    <Bar
      :options="chartOptions"
      :data="chartData"
    />
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
.chart-holder {
  position: absolute;
  width: 1350px;
  height: 710px;
  top: 165px;
  left: 70px;
}

.card-label-holder {
  display: flex;
  justify-content: space-between;
  position: absolute;
  width: 1220px;
  top: 880px;
  left: 268px;
}
</style>
