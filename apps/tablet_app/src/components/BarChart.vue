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
  <div>
    <div class="chart-holder">
      <Bar
        style="position: relative; width: 100%; height: 100%"
        :options="chartOptions"
        :data="chartData"
      />
    </div>
    <div class="card-label-holder">
      <CircleButton
        class="card-label"
        v-for="(item, index) in backendHandler.getGraphLabels()"
        :key="index"
        :label="item"
        @clicked="onLabelClicked"
      ></CircleButton>
    </div>
  </div>
</template>

<script setup lang="ts">
// @ts-nocheck
import { computed } from 'vue'
import { Bar } from 'vue-chartjs'
import { BarElement, CategoryScale, Chart as ChartJS, LinearScale } from 'chart.js'
import { backendHandler } from '@/utils/BackendHandler'
import { tabletConfig } from '@/utils/TabletConfig'
import CircleButton from '@/components/CircleButton.vue'

ChartJS.register(BarElement, CategoryScale, LinearScale)

const props = defineProps<{ categoryHiddenStates: boolean[] }>()

const emits = defineEmits(['card-label-clicked'])

const chartOptions = {
  normalized: true,
  responsive: true,
  maintainAspectRatio: false,
  events: [],
  scales: {
    y: {
      ticks: {
        font: {
          family: 'Lexend-Light', // Set your desired font family
          size: 24 // Set your desired font size
        },
        color: '#B0B5BF',
        padding: 32,
        callback: function (value: any, index: any) {
          // Display only every second tick
          return index % 2 === 0 ? value : ''
        }
      },
      min: 0,
      max: 100, // Set the maximum value for the y-axis
      grid: {
        color: '#3C3F43' // Set the color of the axis line
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
  const labels = backendHandler.getGraphLabels()
  const datasets = backendHandler.getGraphDatasets(
    tabletConfig.timeColor,
    tabletConfig.costColor,
    tabletConfig.efficiencyColor
  )

  for (let i = 0; i < datasets.length; i++) {
    datasets[i]['barPercentage'] = 0.75
    datasets[i]['categoryPercentage'] = 0.5
  }

  return {
    labels: labels,
    datasets: datasets.filter((d) => !props.categoryHiddenStates[datasets.indexOf(d)])
  }
})

function onLabelClicked(card: number) {
  emits('card-label-clicked', card)
}
</script>

<style scoped>
.chart-holder {
  display: block;
  width: 1488px;
  height: 820px;
}

.card-label-holder {
  padding-left: 168px;
}

.card-label {
  float: left;
  margin-right: 108px;
}

.card-label:last-child {
  margin-right: 0;
}
</style>
