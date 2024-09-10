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
    <video ref="webcam" autoplay playsinline style="display: none"></video>
    <canvas ref="canvas"></canvas>
    <img class="canvas-mask" src="/images/camera_image_overlay.png" />
  </div>
</template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { backendHandler } from '@/utils/BackendHandler'
import { tabletConfig } from '@/utils/TabletConfig'

const props = defineProps<{
  scannedIds: string[]
}>()

const webcam = ref<HTMLVideoElement | null>(null)
const canvas = ref<HTMLCanvasElement | null>(null)
const qrCodeId = defineModel({ default: '' })
const noPointsDelay = tabletConfig.qrScanDelay
// @ts-ignore
let detector: BarcodeDetector | null = null
// @ts-ignore
let cornerPoints = ref<DetectedBarcode['cornerPoints'] | null>(null)
let noCornerPointsCount = ref<number>(0)
let animationFrameId: number | null = null

const emits = defineEmits(['qrCodeChanged'])

watch(qrCodeId, () => {
  emits('qrCodeChanged', qrCodeId.value)
})

onMounted(() => {
  startWebcam()
})

onBeforeUnmount(() => {
  if (animationFrameId) {
    cancelAnimationFrame(animationFrameId)
  }
  stopWebcam()
})

function filterQRCodes(width: number, height: number, qrCodes: Array<any>): Object | undefined {
  // Find the QR code closest to the center of the image, ignore all non-matching
  const centerX = width / 2
  const centerY = height / 2
  let closestQRCode = undefined
  let minDistance = Number.MAX_VALUE

  qrCodes.forEach((qrCode: any) => {
    const points = qrCode.cornerPoints
    const qrCenterX = (points[0].x + points[2].x) / 2
    const qrCenterY = (points[0].y + points[2].y) / 2
    const distance = Math.hypot(centerX - qrCenterX, centerY - qrCenterY)
    // Expects a code like 001_001_001
    const scenarioId = qrCode.rawValue.split('_')[0]
    if (
      distance < minDistance &&
      scenarioId === backendHandler.scenarioId &&
      !props.scannedIds.includes(qrCode.rawValue)
    ) {
      minDistance = distance
      closestQRCode = qrCode
    }
  })
  return closestQRCode
}

async function onWebcamFrame() {
  if (detector && webcam.value && canvas.value) {
    try {
      const width = webcam.value.videoWidth
      const height = webcam.value.videoHeight
      const ctx = canvas.value.getContext('2d')!

      // Set canvas size
      ctx.canvas.width = 965
      ctx.canvas.height = 742

      // Clear the canvas
      ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height)

      // Calculate aspect ratios
      const canvasAspect = ctx.canvas.width / ctx.canvas.height
      const webcamAspect = width / height

      // Determine the dimensions for drawing
      let drawWidth, drawHeight
      if (webcamAspect > canvasAspect) {
        // Webcam is wider than canvas, fit by width
        drawWidth = ctx.canvas.width
        drawHeight = drawWidth / webcamAspect
      } else {
        // Webcam is taller than canvas, fit by height
        drawHeight = ctx.canvas.height
        drawWidth = drawHeight * webcamAspect
      }

      // Calculate the position to center the image
      const offsetX = (ctx.canvas.width - drawWidth) / 2
      const offsetY = (ctx.canvas.height - drawHeight) / 2

      // Draw the video frame onto the canvas
      ctx.drawImage(webcam.value, 0, 0, width, height, offsetX, offsetY, drawWidth, drawHeight)

      const scaleFactor = drawWidth / width

      // Draw QR code corners if available, delay is against flickering
      if (cornerPoints.value && noCornerPointsCount.value < noPointsDelay) {
        // Calculate bounding box around corner points
        const minX =
          Math.min(
            cornerPoints.value[0].x,
            cornerPoints.value[1].x,
            cornerPoints.value[2].x,
            cornerPoints.value[3].x
          ) * scaleFactor
        const minY =
          Math.min(
            cornerPoints.value[0].y,
            cornerPoints.value[1].y,
            cornerPoints.value[2].y,
            cornerPoints.value[3].y
          ) * scaleFactor
        const maxX =
          Math.max(
            cornerPoints.value[0].x,
            cornerPoints.value[1].x,
            cornerPoints.value[2].x,
            cornerPoints.value[3].x
          ) * scaleFactor
        const maxY =
          Math.max(
            cornerPoints.value[0].y,
            cornerPoints.value[1].y,
            cornerPoints.value[2].y,
            cornerPoints.value[3].y
          ) * scaleFactor

        const boxWidth = maxX - minX
        const boxHeight = maxY - minY

        // Draw bounding box with rounded corners
        drawRoundedRect(ctx, offsetX + minX, offsetY + minY, boxWidth, boxHeight, 16)
      } else {
        qrCodeId.value = ''
        cornerPoints.value = undefined
      }

      const qrCodes = await detector.detect(webcam.value)
      if (qrCodes.length > 0) {
        // Filters closest, belonging to scenario and not send yet code
        // Increase delay count if no qr code was found
        let closestQRCode = filterQRCodes(width, height, qrCodes)
        if (closestQRCode != undefined) {
          // @ts-ignore
          qrCodeId.value = closestQRCode.rawValue
          // @ts-ignore
          cornerPoints.value = closestQRCode.cornerPoints
          noCornerPointsCount.value = 0
        } else {
          noCornerPointsCount.value++
        }
      } else {
        noCornerPointsCount.value++
      }
    } catch (error) {
      console.error(error)
    }
  }

  // Request the next frameAd
  animationFrameId = requestAnimationFrame(onWebcamFrame)
}

function drawRoundedRect(
  ctx: any,
  x: number,
  y: number,
  width: number,
  height: number,
  radius: number
) {
  ctx.beginPath()
  ctx.moveTo(x + radius, y)
  ctx.lineTo(x + width - radius, y)
  ctx.quadraticCurveTo(x + width, y, x + width, y + radius)
  ctx.lineTo(x + width, y + height - radius)
  ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height)
  ctx.lineTo(x + radius, y + height)
  ctx.quadraticCurveTo(x, y + height, x, y + height - radius)
  ctx.lineTo(x, y + radius)
  ctx.quadraticCurveTo(x, y, x + radius, y)
  ctx.closePath()
  ctx.lineWidth = 5
  ctx.strokeStyle = '#BFD4FF' // Change color if needed
  ctx.stroke()
}

function startWebcam() {
  const constraints = {
    audio: false,
    video: { facingMode: 'environment' }
  }

  // @ts-ignore
  detector = new BarcodeDetector({ formats: ['qr_code'] })

  navigator.mediaDevices
    .getUserMedia(constraints)
    .then((stream) => {
      if (webcam.value) {
        webcam.value.srcObject = stream
        webcam.value.addEventListener('loadedmetadata', () => {
          webcam.value!.play()
          onWebcamFrame() // Start the frame loop
        })
      }
    })
    .catch((error) => {
      alert("May the browser didn't support or there is some errors: " + error)
    })
}

function stopWebcam() {
  if (webcam.value && webcam.value.srcObject) {
    const stream = webcam.value.srcObject
    // @ts-ignore
    const tracks = stream.getTracks()

    // @ts-ignore
    tracks.forEach((track) => {
      track.stop() // Stop each track
    })

    webcam.value.srcObject = null // Clear the video element's srcObject
    webcam.value.removeEventListener('loadedmetadata', onWebcamFrame) // Remove the event listener
  }

  if (detector) {
    detector = null // Clear the detector if needed
  }
}
</script>

<style scoped>
canvas {
  position: absolute;
  display: block;
  left: 25px;
  top: 30px;
}

.canvas-mask {
  top: 0;
  left: 0;
  position: absolute;
}
</style>
