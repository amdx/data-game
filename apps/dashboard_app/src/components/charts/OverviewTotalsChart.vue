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

<!--Sample usage:-->
<!--<OverviewChart :values="{time: 31, cost: 61, efficiency: 29}"/>-->

<script setup lang="ts">
import 'chart.js/auto'
import { Doughnut } from 'vue-chartjs'
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useUserConfig } from '@/composables/useUserConfig'
import type { ChartOptions } from 'chart.js'

const props = defineProps(['values'])

const { t } = useI18n()
const userConfig = useUserConfig()

const chartOptions: ChartOptions<'doughnut'> = {
  normalized: true,
  responsive: true,
  cutout: '88%',
  events: []
}

const datasets = computed(() => {
  return userConfig.value?.graphs.categories.map((cat) => {
    return {
      label: t(`charts.overall.${cat}`),
      data: [props.values[cat], 100 - props.values[cat]],
      backgroundColor: [userConfig.value!.graphs.colors[cat], '#2D2C30'],
      borderWidth: 0
    }
  })
})
</script>

<template>
  <div class="chart-container">
    <div class="chart-block" v-for="(item, index) in datasets" :key="index">
      <div class="doughnut-wrapper">
        <div class="doughnut">
          <Doughnut :data="{ datasets: [item] }" :options="chartOptions" />
          <div class="value" :style="{ color: item.backgroundColor[0] }">
            <span>{{ item.data[0] }}</span>
          </div>
        </div>
      </div>
      <div class="caption">
        <span>{{ item.label }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.chart-container {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
}

.chart-block {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.doughnut-wrapper {
  position: relative;
}

.doughnut {
  position: relative;
  width: 240px;
  height: 240px;
}

.value {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) translate(2px, 4px);
  text-align: center;
  font-family: Lexend-ExtraLight;
  font-size: 56px;
  letter-spacing: 4.52px;
}

.caption {
  margin-top: 40px;
  text-align: center;
  font-family: Lexend-Light;
  font-size: 30px;
  letter-spacing: 2.4px;
}
</style>
