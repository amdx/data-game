<template>
  <transition name="fade">
    <div v-if="modelValue" class="modal-overlay">
      <div class="modal">
        <div class="your-team">{{ $t('team_name_view.your_team') }}</div>
        <div class="name">{{ teamName }}</div>
        <DotLottieVue class="animation" autoplay loop src="progress_animation.json"></DotLottieVue>
        <div class="logged-in">{{ $t('team_name_view.logged_in') }}</div>
      </div>
    </div>
  </transition>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'
import { DotLottieVue } from '@lottiefiles/dotlottie-vue'

const props = defineProps<{
  modelValue: boolean
  teamName: string
}>()
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgb(29, 30, 32, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.modal {
  width: 1024px;
  height: 992px;
  background: #1d1e20 0% 0% no-repeat padding-box;
  box-shadow: 0px 0px 20px #00000099;
  border-radius: 20px;
  position: relative;
}

.your-team {
  position: absolute;
  top: 82px;
  left: 67px;
  width: 890px;
  letter-spacing: 1.52px;
  text-align: center;
  font-family: Lexend-ExtraLight;
  font-size: 38px;
}

.name {
  position: absolute;
  top: 139px;
  left: 68px;
  width: 888px;
  letter-spacing: 4.8px;
  text-align: center;
  font-family: Lexend-Light;
  font-size: 60px;
  overflow: hidden;
}

.animation {
  position: absolute;
  top: 296px;
  left: 312px;
  width: 400px;
  height: 400px;
}

.logged-in {
  position: absolute;
  top: 822px;
  left: 240px;
  width: 544px;
  letter-spacing: 1.04px;
  text-align: center;
  font-family: Lexend-Light;
  font-size: 26px;
  white-space: pre-line;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
