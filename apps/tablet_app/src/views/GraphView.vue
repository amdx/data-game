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
  <main>
    <dropdown-menu :items="menuEntries"
                   :selected-index="currentChart"
                   @select="handleGraphSelect"></dropdown-menu>
    <div class="category-bar">
      <div
        class="category-bar-item"
        v-for="(item, index) in categoryData"
        v-on:click="handleCategory(index)"
        :key="index"
      >
        <div
          class="category-dot"
          :style="{ 'background-color': `${isCategoryPicked(index) ? item.color : '#2C2E30'}` }"
        ></div>
        <div
          :style="{ color: `${isCategoryPicked(index) ? '#8D9199' : '#5E6166'}` }">
          {{ $t(item.textKey) }}
        </div>
      </div>
    </div>
    <div class="hint">{{ $t('graph_view.hint') }}</div>
    <div>
      <BarChart
        class="bar-chart"
        v-if="currentChart === 0"
        :category-hidden-states="categoryHiddenStates"
        @card-label-clicked="onLabelClicked"
      ></BarChart>
      <WebChart
        class="web-chart"
        v-if="currentChart === 1"
        :category-hidden-states="categoryHiddenStates"
        @card-label-clicked="onLabelClicked"
      ></WebChart>
      <DonutChart
        class="donut-chart"
        v-if="currentChart === 2"
        :category-hidden-states="categoryHiddenStates"
        @card-label-clicked="onLabelClicked"
      ></DonutChart>
      <PolarChart
        class="polar-chart"
        v-if="currentChart === 3"
        :category-hidden-states="categoryHiddenStates"
        @card-label-clicked="onLabelClicked"
      ></PolarChart>
    </div>
    <DonutOverviewChart
      class="donut-overview-chart"
      @send-data="showSendPrompt"
    ></DonutOverviewChart>
    <CardModal v-model="showModal" :card-id="pickedCard"
               @delete-card="onDeleteCard">
      <p>This is the modal content!</p>
    </CardModal>
    <TabletPrompt
      :text="t('graph_view.send_prompt')"
      :has-cancel-button="true"
      v-model="isSendPrompt"
      @ok="onSendQRCodes"
    ></TabletPrompt>
    <TabletPrompt
      :text="`${t('common.error')}\n\n${errorText}`"
      :has-cancel-button="false"
      v-model="isErrorPrompt"
    >
    </TabletPrompt>
    <ImageButton v-if="!showExplainer" class="info-button"
                 up-source="images/info_btn_up.svg"
                 down-source="images/info_btn_down.svg" disabled-source=""
                 :is-disabled="false" @clicked="onInfoButtonClicked" />
    <Transition>
      <div v-if="showExplainer" class="explainer"
           @click="onExplainerClicked"></div>
    </Transition>
  </main>
</template>

<script setup lang="ts">
import { computed, onBeforeMount, reactive, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import DropdownMenu from '@/components/DropdownMenu.vue'
import BarChart from '@/components/BarChart.vue'
import DonutChart from '@/components/DonutChart.vue'
import PolarChart from '@/components/PolarChart.vue'
import WebChart from '@/components/WebChart.vue'
import { tabletConfig } from '@/utils/TabletConfig'
import DonutOverviewChart from '@/components/DonutOverviewChart.vue'
import { backendHandler } from '@/utils/BackendHandler'
import CardModal from '@/components/CardModal.vue'
import { useRouter } from 'vue-router'
import TabletPrompt from '@/components/TabletPrompt.vue'
import ImageButton from '@/components/ImageButton.vue'

const router = useRouter()
const { t } = useI18n({ useScope: 'global' })
const menuEntries = [
  t('graph_view.bar_chart'),
  t('graph_view.web_chart'),
  t('graph_view.donut_chart'),
  t('graph_view.polar_chart')
]
const categoryData = reactive([
  {
    color: tabletConfig.timeColor,
    textKey: 'graph_view.time_category',
    picked: true
  },
  {
    color: tabletConfig.costColor,
    textKey: 'graph_view.cost_category',
    picked: true
  },
  {
    color: tabletConfig.efficiencyColor,
    textKey: 'graph_view.efficiency_category',
    picked: true
  }
])
const currentChart = ref<number>(Number(localStorage.getItem('currentChart')) || 0)
const showModal = ref(false)
const pickedCard = ref('')
const isSendPrompt = ref(false)
const isErrorPrompt = ref(false)
const errorText = ref('')
const showExplainer = ref(true)

const categoryHiddenStates = computed(() => {
  return categoryData.map((c) => !c.picked)
})

function isCategoryPicked(index: number) {
  return categoryData[index].picked
}

function handleGraphSelect(index: number) {
  resetView()
  currentChart.value = index
}

function handleCategory(index: number) {
  categoryData[index].picked = !categoryData[index].picked
}

function resetView() {
  for (const category of categoryData) {
    category.picked = true
  }
}

function showSendPrompt() {
  isSendPrompt.value = true
}

function onSendQRCodes() {
  localStorage.removeItem('currentChart')
  backendHandler
    .sendTeamCards()
    .then(() => {
      router.replace({ name: 'evaluation' })
    })
    .catch((error) => {
      console.error(error)
      if (error.response) {
        errorText.value = error.response.data.detail
      } else {
        errorText.value = error.message
      }
      isErrorPrompt.value = true
    })
}

function onLabelClicked(label: number) {
  showModal.value = true
  pickedCard.value = backendHandler.getCardByNumber(label)!.card_id
}

function onDeleteCard() {
  backendHandler.scannedIds = backendHandler.scannedIds.filter((cId) => cId !== pickedCard.value)
  localStorage.setItem('currentChart', String(currentChart.value))
  router.replace({ name: 'scan' })
}

function onExplainerClicked() {
  showExplainer.value = false
  localStorage.setItem('showExplainer', 'false')
}

function onInfoButtonClicked() {
  currentChart.value = 0
  showExplainer.value = true
}

onBeforeMount(() => {
  const _showExplainer: string | null = localStorage.getItem('showExplainer')
  showExplainer.value = (_showExplainer == null || _showExplainer === 'true')
})
</script>

<style scoped>
.dropdown-menu {
  z-index: 2;
  position: absolute;
  top: 40px;
  left: 65px;
}

.category-bar {
  position: absolute;
  top: 144px;
  left: 88px;
  font-size: 26px;
  letter-spacing: 1.04px;
}

.category-bar-item {
  float: left;
  width: 184px;
}

.category-dot {
  height: 24px;
  width: 24px;
  border-radius: 50%;
  float: left;
  margin-right: 21px;
  margin-top: 4px;
}

.hint {
  position: absolute;
  top: 194px;
  left: 88px;
  letter-spacing: 1.76px;
  color: #8D9199;
  font-family: Lexend-ExtraLight;
  font-size: 22px;
}

.bar-chart {
  z-index: 1;
  position: absolute;
  top: 264px;
  left: 64px;
  display: inline-block;
}

.web-chart {
  z-index: 1;
  position: absolute;
  top: 224px;
  left: 428px;
  display: inline-block;
}

.polar-chart {
  z-index: 1;
  position: absolute;
  top: 224px;
  left: 428px;
  display: inline-block;
}

.donut-chart {
  z-index: 1;
  position: absolute;
  top: 315px;
  left: 122px;
  display: inline-block;
}

.donut-overview-chart {
  z-index: 1;
  position: absolute;
  top: 106px;
  left: 1624px;
  width: 304px;
  max-width: 304px;
  height: 1040px;
  max-height: 1040px;
  display: inline-block;
}

.explainer {
  z-index: 9999;
  background: url('/images/explain_layer.png') no-repeat center center;
  background-size: cover;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.info-button {
  position: absolute;
  top: 1085px;
  width: 64px;
  height: 64px;
}

.v-enter-active,
.v-leave-active {
  transition: opacity 0.5s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>
