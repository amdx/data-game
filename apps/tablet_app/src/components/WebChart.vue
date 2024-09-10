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
  <div class="chart-container">
    <Radar class="radar" :options="chartOptions" :data="chartData" />
    <div class="circle-buttons">
      <CircleButton
        v-for="(item, index) in backendHandler.getGraphLabels()"
        :key="index"
        :label="item"
        :style="buttonStyle(index, backendHandler.getGraphLabels().length)"
        @clicked="onLabelClicked"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { Chart as ChartJS, Filler, LineElement, PointElement, RadialLinearScale } from 'chart.js'
import { Radar } from 'vue-chartjs'
import { computed } from 'vue'
import { backendHandler } from '@/utils/BackendHandler'
import { tabletConfig } from '@/utils/TabletConfig'
import CircleButton from '@/components/CircleButton.vue'

ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler)

const props = defineProps<{ categoryHiddenStates: boolean[] }>()

const emits = defineEmits(['card-label-clicked'])

const chartOptions = {
  normalized: true,
  responsive: false,
  events: [],
  scales: {
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
        callback: function (value: any, index: any) {
          // Display only every second tick
          return index % 2 === 0 ? value : ''
        }
      }
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
  for (let i = 0; i < props.categoryHiddenStates.length; i++) {
    datasets[i].borderWidth = 3
    // Add transparency
    datasets[i].backgroundColor = datasets[i].backgroundColor + '20'
  }
  return {
    labels: labels,
    datasets: datasets.filter((d) => !props.categoryHiddenStates[datasets.indexOf(d)])
  }
})

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
  emits('card-label-clicked', card)
}
</script>

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
