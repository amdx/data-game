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
import type { ChartOptions } from 'chart.js'
import type { ActionCard } from '@/client'
import { useUserConfig } from '@/composables/useUserConfig'
import CircleButton from '@/components/CircleButton.vue'

const props = defineProps(['categoryHiddenStates', 'teamData', 'scenarioScores'])
const emit = defineEmits(['cardLabelClicked'])

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
          family: 'Lexend-Light', // Set your desired font family
          size: 24 // Set your desired font size
        },
        color: '#B0B5BF',
        padding: 32,
        callback: function(value: any, index: any) {
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

  const allDatasets = []
  for (const category of userConfig.value!.graphs.categories) {
    allDatasets.push({
      backgroundColor: userConfig.value?.graphs.colors[category],
      barPercentage: 0.75,
      categoryPercentage: 0.5,
      data: props.teamData.action_cards.map((card: ActionCard) => card[category] / props.scenarioScores.maxima[category] * 100)
    })
  }

  return allDatasets.filter((_, index) => !props.categoryHiddenStates[index])
})
const chartData = computed(() => {
  if (labels.value && datasets) {
    return {
      labels: labels.value,
      datasets: datasets.value
    }
  } else {
    return null
  }
})

function onLabelClicked(card: number) {
  emit('cardLabelClicked', card)
}
</script>

<template>
  <div v-if="chartData">
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
        v-for="(item, index) in labels"
        :key="index"
        :id="item"
        @clicked="onLabelClicked"
      ></CircleButton>
    </div>
  </div>
</template>

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
