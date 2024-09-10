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
import { PolarArea } from 'vue-chartjs'
import type { ChartDataset, ChartOptions } from 'chart.js'
import { useUserConfig } from '@/composables/useUserConfig'
import CircleButton from '@/components/CircleButton.vue'

const props = defineProps(['teamEvaluation', 'categoryFilterFlags'])
const emit = defineEmits(['datasetClicked'])

const userConfig = useUserConfig()

const chartOptions: ChartOptions<'polarArea'> = {
  normalized: true,
  responsive: false,
  events: [],
  plugins: {
    legend: {
      display: false
    }
  },
  scales: {
    r: {
      max: 100,
      min: 0,
      angleLines: {
        color: '#64676E'
      },
      grid: {
        color: '#64676E'
      },
      ticks: {
        backdropColor: 'rgba(0, 0, 0, 0)', // Transparent background for scale labels
        font: {
          family: 'Lexend-Light',
          size: 24
        },
        color: '#B0B5BF',
        callback: function(value: any, index: any) {
          // Display only every second tick
          return index % 2 === 0 ? value : ''
        }
      }
    }
  }
}

const chartData = computed(() => {
  const data = []
  const backgroundColor = []
  const borderColor = []
  const borderWidth = []
  const datasets: ChartDataset<'polarArea'>[] = []
  for (const index in props.teamEvaluation.team_names) {
    for (const category of userConfig.value!.graphs.categories) {
      if (props.categoryFilterFlags[category]) {
        data.push(props.teamEvaluation.teams_evaluation[category][index])
        backgroundColor.push(userConfig.value?.graphs.colors[category] + '20')
        borderColor.push(userConfig.value?.graphs.colors[category])
        borderWidth.push(3)
      }
    }

    data.push(0)
    backgroundColor.push('#000')
    borderColor.push('#000')
    borderWidth.push(3)
  }

  datasets.push({
    data,
    backgroundColor,
    borderColor,
    borderWidth
  })
  return {
    datasets
  }
})

const buttonStyle = (index: number, total: number, subtractWidth: boolean) => {
  const angle = (index / total) * 2 * Math.PI - Math.PI / 2 + 0.5
  const radius = 420
  const x = radius * Math.cos(angle) + (subtractWidth ? -140 : 0)
  const y = radius * Math.sin(angle)
  return {
    position: 'absolute',
    transform: `translate(${x}px, ${y}px)`,
    transformOrigin: 'center'
  }
}
</script>

<template>
  <div class="chart-holder">
    <PolarArea
      class="polararea"
      :options="chartOptions"
      :data="chartData"
    />
    <div class="circle-buttons">
      <CircleButton
        v-for="(item, index) in teamEvaluation.team_names"
        :key="index"
        :id="`${index + 1}`"
        :label="item"
        :flip-text="[3, 4].includes(index)"
        :style="buttonStyle(index, teamEvaluation.team_names.length, [3, 4].includes(index))"
        @clicked="emit('datasetClicked', index)"
      />
    </div>
  </div>
</template>

<style scoped>
.chart-holder {
  position: absolute;
  width: 1270px;
  height: 710px;
  top: 165px;
  left: 70px;
}

.polararea {
  position: absolute;
  width: 720px;
  height: 720px;
  left: 325px;
}

.circle-buttons {
  position: absolute;
  top: 0;
  left: 120px;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
