<template>
  <div class="chart-container">
    <PolarArea class="polar-area" :options="chartOptions" :data="chartData" />
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
import { ArcElement, Chart as ChartJS, Filler, RadialLinearScale } from 'chart.js'
import { PolarArea } from 'vue-chartjs'
import { computed } from 'vue'
import { backendHandler } from '@/utils/BackendHandler'
import { tabletConfig } from '@/utils/TabletConfig'
import CircleButton from '@/components/CircleButton.vue'

ChartJS.register(ArcElement, RadialLinearScale, Filler)

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
  let datasets = backendHandler.getPolarGraphDatasets(
    !props.categoryHiddenStates[0] ? tabletConfig.timeColor : undefined,
    !props.categoryHiddenStates[1] ? tabletConfig.costColor : undefined,
    !props.categoryHiddenStates[2] ? tabletConfig.efficiencyColor : undefined
  )

  for (let i = 0; i < datasets.data.length; i++) {
    datasets.borderWidth[i] = 3
    // Add transparency
    datasets.backgroundColor[i] = datasets.backgroundColor[i] + '20'
  }

  return {
    datasets: [datasets]
  }
})

const buttonStyle = (index: number, total: number) => {
  const angle = (index / total) * 2 * Math.PI - Math.PI / 2 + 0.29
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

.polar-area {
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
