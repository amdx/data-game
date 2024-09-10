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
  <div class="container">
    <RouterView v-slot="{ Component, route }">
      <transition name="fade" mode="out-in" @enter="resizeApp"
                  @after-enter="resizeApp">
        <component :is="Component" :key="route.path" class="main-div" />
      </transition>
    </RouterView>
    <TabletPrompt
      :text="$t('common.fullscreen_prompt')"
      :has-cancel-button="false"
      v-model="showFullscreenPrompt"
      @ok="goFullscreen"
    >
    </TabletPrompt>
  </div>
</template>

<script setup lang="ts">
import { RouterView, useRoute, useRouter } from 'vue-router'
import { nextTick, onMounted, onUnmounted, reactive, ref, watch } from 'vue'
import { setWasmUrl } from '@lottiefiles/dotlottie-vue'
import { backendHandler } from './utils/BackendHandler'
import { eventBus } from '@/utils/EventBus'
import { SessionState } from '@/utils/DataTypes'
import { tabletConfig } from '@/utils/TabletConfig'
import TabletPrompt from '@/components/TabletPrompt.vue'

const session = reactive({ state: '' })
const router = useRouter()
const route = useRoute()

const showFullscreenPrompt = ref(false)
const isFullscreen = ref(false) // Manually track fullscreen state

let wakeLock: any = null

setWasmUrl(tabletConfig.lottieWasmUrl)

watch(
  () => session.state,
  (state) => {
    handleState(state)
  }
)

watch(
  () => route.name,
  () => {
    nextTick(() => {
      resizeApp()
    })
    requestWakeLock()
  }
)

watch(isFullscreen, (newValue) => {
  console.debug('Fullscreen state changed:', newValue)
  setFullscreenPrompt(!newValue)
})

function handleState(state: string) {
  if (state === SessionState.INTRODUCTION) {
    backendHandler.teamId = undefined
    backendHandler.scannedIds = []
    router.replace({ name: 'standBy' })
  } else if (state === SessionState.TEAM_NAMING) {
    router.replace({ name: 'welcome' })
  } else if (state === SessionState.SCANNING) {
    backendHandler.scannedIds = []
    localStorage.setItem('showExplainer', 'true')
    router.replace({ name: 'scanIntro' })
  } else if (state === SessionState.EVALUATION) {
    router.replace({ name: 'evaluation' })
  }
}

onMounted(() => {
  document.addEventListener('contextmenu', disableRightClick)
  document.addEventListener('fullscreenchange', onFullscreenChange)
  window.addEventListener('resize', onResize)

  updateFullscreenState()
  setFullscreenPrompt(!isFullscreen.value)

  eventBus.on('newState', onNewSessionState)
  backendHandler.backendPath = tabletConfig.backendPath
  backendHandler.startCommunication()
  window.addEventListener('resize', resizeApp)
  nextTick(() => {
    resizeApp() // Initial call to set the scale
  })
  requestWakeLock()
  requestCameraPermission()
})

onUnmounted(() => {
  document.removeEventListener('contextmenu', disableRightClick)
  document.removeEventListener('fullscreenchange', onFullscreenChange)
  window.removeEventListener('resize', onResize)
  eventBus.off('newState', onNewSessionState)
  backendHandler.stopCommunication()
  window.removeEventListener('resize', resizeApp)
  releaseWakeLock()
})

function onNewSessionState(state: string): void {
  session.state = state
}

function resizeApp() {
  const app = document.querySelector('.main-div') as HTMLElement
  if (!app) return

  const appWidth = 2000
  const appHeight = 1200

  const windowWidth = window.innerWidth
  const windowHeight = window.innerHeight

  const scaleWidth = windowWidth / appWidth
  const scaleHeight = windowHeight / appHeight

  const scale = Math.min(scaleWidth, scaleHeight)

  app.style.transform = `scale(${scale})`
  app.style.transformOrigin = 'top left'
  app.style.width = `${appWidth}px`
  app.style.height = `${appHeight}px`

  const left = (windowWidth - appWidth * scale) / 2
  const top = (windowHeight - appHeight * scale) / 2

  app.style.position = 'absolute'
  app.style.left = `${left}px`
  app.style.top = `${top}px`
}

function setFullscreenPrompt(show: boolean) {
  if (tabletConfig.showFullscreenPrompt) {
    showFullscreenPrompt.value = show
  }
}

function goFullscreen() {
  const element = document.documentElement
  console.debug('Attempting to enter fullscreen mode...')
  if (element.requestFullscreen) {
    element
      .requestFullscreen()
      .then(() => {
        console.debug('Fullscreen mode entered successfully')
        isFullscreen.value = true
        // lock to landscape
        // @ts-ignore
        return screen.orientation.lock('landscape')
      })
      .catch((err) => {
        console.error(`Error attempting to enable full-screen mode: ${err.message} (${err.name})`)
      })
    // @ts-ignore
  } else if (element.mozRequestFullScreen) {
    // Firefox
    // @ts-ignore
    element.mozRequestFullScreen()
    isFullscreen.value = true
    // @ts-ignore
  } else if (element.webkitRequestFullscreen) {
    // Chrome, Safari and Opera
    // @ts-ignore
    element.webkitRequestFullscreen()
    isFullscreen.value = true
    // @ts-ignore
  } else if (element.msRequestFullscreen) {
    // IE/Edge
    // @ts-ignore
    element.msRequestFullscreen()
    isFullscreen.value = true
  }
}

function onFullscreenChange() {
  console.debug('Fullscreen change event detected')
  updateFullscreenState()
}

function onResize() {
  console.debug('Window resize detected')
  updateFullscreenState()
}

function updateFullscreenState() {
  isFullscreen.value = !!(
    document.fullscreenElement || // @ts-ignore
    document.mozFullScreenElement || // @ts-ignore
    document.webkitFullscreenElement || // @ts-ignore
    document.msFullscreenElement // @ts-ignore
  )
}

function disableRightClick(event: any) {
  if (tabletConfig.disableRightClick) {
    event.preventDefault()
  }
}

function requestWakeLock() {
  if (wakeLock) {
    return wakeLock.release().then(() => {
      wakeLock = null
      return _requestWakeLock()
    })
  } else {
    _requestWakeLock()
  }
}

function releaseWakeLock() {
  if (wakeLock) {
    return wakeLock.release().then(() => {
      wakeLock = null
    })
  }
}

function requestCameraPermission() {
  // Check if the browser supports the media devices API
  if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    // Request access to the camera
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(function(stream) {
        // Permissions granted, but we do not use the stream here
        console.info('Camera permission granted.')

        // Stop all tracks of the stream to release the camera
        stream.getTracks().forEach(track => track.stop())
      })
      .catch(function(error) {
        // Permissions denied or an error occurred
        console.error('Camera permission denied:', error)
      })
  } else {
    console.error('getUserMedia not supported on this browser!')
  }
}

function _requestWakeLock() {
  return navigator.wakeLock
    .request('screen')
    .then((lock) => {
      wakeLock = lock
      console.debug('Wake Lock is active!')
    })
    .catch((error) => {
      console.error(`${error.name}, ${error.message}`)
    })
}
</script>

<style>
html,
body {
  margin: 0px !important;
  padding: 0px !important;
  background-color: #1e1f20;
  color: #ebebeb;
  font-family: Lexend-Light;
  user-select: none;
  width: 100%;
  height: 100%;
}

.container {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

.main-div {
  width: 2000px;
  height: 1200px;
  transform-origin: top left;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
