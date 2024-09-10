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
    <div class="donut-holder" v-for="(item, index) in chartData" :key="index">
      <div class="donut-value">
        <span :style="{ color: `${item.backgroundColor[0]}` }">{{ item.data[0] }}</span>
      </div>
      <div class="donut">
        <Doughnut :data="{ datasets: [item] }" :options="chartOptions" />
      </div>
      <div class="donut-label">
        <span>{{ chartLabels[index] }}</span>
      </div>
    </div>
    <div class="button-holder">
      <ImageButton
        class="send-button"
        down-source="images/send_data_btn_down.svg"
        up-source="images/send_data_btn_up.svg"
        disabled-source=""
        :is-disabled="false"
        @clicked="emits('send-data')"
      />
      <div class="button-label">
        <span>{{ t('graph_view.send_label') }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ArcElement, Chart as ChartJS } from 'chart.js'
import { Doughnut } from 'vue-chartjs'
import { computed, defineEmits } from 'vue'
import { useI18n } from 'vue-i18n'
import { backendHandler } from '@/utils/BackendHandler'
import { tabletConfig } from '@/utils/TabletConfig'
import ImageButton from '@/components/ImageButton.vue'

ChartJS.register(ArcElement)

const emits = defineEmits(['send-data'])

const { t } = useI18n({ useScope: 'global' })
const chartOptions = {
  normalized: true,
  responsive: true,
  cutout: 75,
  events: []
}
const chartLabels = [
  t('graph_view.time_overall'),
  t('graph_view.cost_overall'),
  t('graph_view.efficiency_overall')
]

const chartData = computed<any[]>(() => {
  const timeValue = Math.round(
    (backendHandler.getTimeSum() / backendHandler.getOverallTimeValue()) * 100
  )
  const time = {
    data: [timeValue, 100 - timeValue],
    backgroundColor: [tabletConfig.timeColor, '#2D2C30'],
    borderWidth: 0
  }
  const costValue = Math.round(
    (backendHandler.getCostSum() / backendHandler.getOverallCostValue()) * 100
  )
  const cost = {
    data: [costValue, 100 - costValue],
    backgroundColor: [tabletConfig.costColor, '#2D2C30'],
    borderWidth: 0
  }
  const efficiencyValue = Math.round(
    (backendHandler.getEfficiencySum() / backendHandler.getOverallEfficiencyValue()) * 100
  )
  const efficiency = {
    data: [efficiencyValue, 100 - efficiencyValue],
    backgroundColor: [tabletConfig.efficiencyColor, '#2D2C30'],
    borderWidth: 0
  }
  return [time, cost, efficiency]
})
</script>

<style scoped>
.donut-holder {
  float: left;
  display: block;
  width: 319px;
  height: 300px;
  align-items: center;
}

.donut {
  display: block;
  padding-left: 74px;
  width: 170px;
  height: 170px;
}

.donut-value {
  position: absolute;
  display: grid;
  padding-left: 74px;
  width: 170px;
  height: 170px;
  align-items: center;
  text-align: center;
  font-family: Lexend-ExtraLight;
  font-size: 42px;
  letter-spacing: 3.36px;
  white-space: pre-line;
}

.donut-label {
  padding-top: 32px;
  text-align: center;
  font-family: Lexend-ExtraLight;
  font-size: 24px;
  letter-spacing: 1.92px;
  white-space: pre-line;
}

.donut-label span {
  margin: 0 10px; /* Adjust the margin value as needed */
}

.button-holder {
  float: left;
  display: block;
  width: 319px;
  align-items: center;
}

.send-button {
  display: block;
  padding-left: 103px;
  width: 112px;
  height: 104px;
}

.button-label {
  padding-top: 12px;
  text-align: center;
  font-family: Lexend-ExtraLight;
  font-size: 22px;
  letter-spacing: 3.08px;
  white-space: pre-line;
}

.button-label span {
  margin: 0 10px; /* Adjust the margin value as needed */
}
</style>
