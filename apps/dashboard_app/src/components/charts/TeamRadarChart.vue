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
import { Radar } from 'vue-chartjs'
import { computed, type ComputedRef } from 'vue'
import { useUserConfig } from '@/composables/useUserConfig'
import CircleButton from '@/components/CircleButton.vue'
import type { ChartData, ChartOptions } from 'chart.js'
import type { ActionCard } from '@/client'

const props = defineProps(['categoryHiddenStates', 'teamData', 'scenarioScores'])
const emit = defineEmits(['cardLabelClicked'])

const userConfig = useUserConfig()

const chartOptions: ChartOptions<'radar'> = {
  normalized: true,
  responsive: false,
  events: [],
  plugins: {
    legend: {
      display: false
    }
  }, scales: {
    r: {
      max: 100,
      min: 0,
      angleLines: {
        color: '#64676E'
      },
      grid: {
        color: '#64676E' // Set the color of the axis line
      },
      pointLabels: {
        display: false // Hide point labels
      },
      ticks: {
        backdropColor: 'rgba(0, 0, 0, 0)', // Transparent background for scale labels
        font: {
          family: 'Lexend-Light', // Change font family
          size: 24
        },
        color: '#B0B5BF', // Change font color
        callback: function(value: any, index: any) {
          // Display only every second tick
          return index % 2 === 0 ? value : ''
        }
      }
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
      backgroundColor: userConfig.value?.graphs.colors[category] + '20',
      borderColor: userConfig.value?.graphs.colors[category],
      borderWidth: 3,
      pointRadius: 0,
      data: props.teamData.action_cards.map((card: ActionCard) => card[category] / props.scenarioScores.maxima[category] * 100)
    })
  }

  return allDatasets.filter((_, index) => !props.categoryHiddenStates[index])
})
const chartData: ComputedRef<ChartData<'radar'>> = computed(() => ({
  labels: labels.value ?? [],
  datasets: datasets.value ?? []
}))


const buttonStyle = (index: number, total: number) => {
  const angle = (index / total) * 2 * Math.PI - Math.PI / 2
  const radius = 480 // Adjust the radius as needed
  const x = radius * Math.cos(angle)
  const y = radius * Math.sin(angle)
  return {
    position: 'absolute',
    transform: `translate(${x}px, ${y}px)`,
    transformOrigin: 'center'
  }
}

function onLabelClicked(card: string) {
  emit('cardLabelClicked', card)
}
</script>

<template>
  <div class="chart-container">
    <Radar class="radar" :options="chartOptions" :data="chartData" />
    <div class="circle-buttons">
      <CircleButton
        v-for="(item, index) in labels"
        :key="index"
        :id="item"
        :style="buttonStyle(index, labels.length)"
        @clicked="onLabelClicked"
      />
    </div>
  </div>
</template>

<style scoped>
.chart-container {
  width: 840px;
  height: 840px;
  display: inline-block;
  position: relative; /* Added relative positioning */
}

.radar {
  display: block;
  width: 100%;
  height: 100%;
}

.circle-buttons {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
