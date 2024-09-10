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
    <div class="headline-holder">
      <div class="headline">{{ t('scan_view.headline') }}</div>
      <div class="sub-headline">{{ t('scan_view.sub_headline') }}</div>
    </div>
    <transition-group name="fade" tag="div" class="scanned-cards">
      <div
        :class="item !== undefined ? 'scanned-card' : 'empty-card'"
        v-for="(item, index) in scannedCards"
        :key="index"
      >
        {{ item ? item : '?' }}
      </div>
    </transition-group>
    <QRCamera
      class="qr-camera"
      :scanned-ids="scannedIds"
      @qr-code-changed="onQrCodeScanned"
    ></QRCamera>
    <ImageButton
      class="scan-button"
      down-source="images/scan_btn_down.svg"
      up-source="images/scan_btn_up.svg"
      disabled-source="images/scan_btn_idle.svg"
      :is-disabled="!currentId || isCardSetFull"
      @clicked="addActionCard"
    ></ImageButton>
    <div class="scan-button-label">{{ t('scan_view.scan_button_label') }}</div>
    <div class="info">
      <router-link :to="{ name: 'scanIntro' }">{{ t('scan_view.info') }} </router-link>
    </div>
  </main>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import QRCamera from '@/components/QRCamera.vue'
import { computed, onMounted, ref, watch } from 'vue'
import { backendHandler } from '@/utils/BackendHandler'
import ImageButton from '@/components/ImageButton.vue'

const router = useRouter()

const { t } = useI18n({ useScope: 'global' })

const scannedIds = ref<Array<string>>([])
const currentId = ref<string>('')

const scannedCards = computed(() => {
  const cards = new Array(8).fill(undefined)
  for (let i in scannedIds.value) {
    const qrCode = scannedIds.value[i]
    const card = backendHandler.getCardById(qrCode)
    if (card) {
      cards[i] = card.card_number
    }
  }
  return cards
})
const isCardSetFull = computed(() => {
  return scannedIds.value.length >= backendHandler.cardCount
})

watch(isCardSetFull, () => {
  if (isCardSetFull.value) {
    goToGraphView()
  }
})

function onQrCodeScanned(code: string) {
  currentId.value = code
}

function addActionCard() {
  if (!scannedIds.value.includes(currentId.value) && isCardSetFull) {
    scannedIds.value.push(currentId.value)
  }
}

function goToGraphView() {
  backendHandler.scannedIds = scannedIds.value
  router.replace({ name: 'graph' })
}

onMounted(() => {
  scannedIds.value = backendHandler.scannedIds
})
</script>

<style scoped>
.headline-holder {
  position: absolute;
  top: 83px;
  left: 144px;
}

.headline {
  font-size: 60px;
  letter-spacing: 4.86px;
}

.sub-headline {
  font-family: Lexend-ExtraLight;
  font-size: 38px;
  letter-spacing: 1.05px;
  white-space: pre-line;
}

.scanned-cards {
  position: absolute;
  top: 364px;
  left: 124px;
  width: 700px;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}

.scanned-card,
.empty-card {
  float: left;
  display: flex;
  margin: 20px;
  width: 128px;
  height: 168px;
  border-radius: 8px;
  border-width: 3px;
  border-style: solid;
  align-items: center;
  justify-content: center;
  text-align: center;
  font-family: Lexend-Light;
  font-size: 40px;
  letter-spacing: 1.6px;
  transition: all 0.3s ease;
  white-space: pre-line;
}

.scanned-card {
  background-color: #3498db;
  border-color: #3498db;
  opacity: 1;
}

.empty-card {
  border-color: #46484c;
  box-shadow: 0px 0px 3px #000000cc;
  border: 3px solid #46484c;
  font-size: 40px;
  color: #8d9199;
}

/* Fade transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}

.qr-camera {
  position: absolute;
  top: 176px;
  left: 864px;
}

.scan-button {
  position: absolute;
  top: 968px;
  left: 1312px;
}

.scan-button-label {
  position: absolute;
  top: 1122px;
  left: 1198px;
  width: 364px;
  height: 46px;
  text-align: center;
  letter-spacing: 3.08px;
  font-family: Lexend-Light;
  font-size: 22px;
  white-space: pre-line;
}

.info {
  position: absolute;
  top: 1114px;
  left: 1774px;
  width: 172px;
  height: 80px;
  text-align: center;
  text-align: right;
  letter-spacing: 4.2px;
  font-size: 30px;
}

.info a {
  color: #bfd4ff;
  text-decoration: none;
}

.info a:active {
  color: #5e6166;
  text-decoration: none;
}
</style>
