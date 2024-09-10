<template>
  <transition name="fade">
    <div v-if="modelValue" class="modal-overlay" @click.self="close">
      <div class="modal">
        <div class="text">{{ text }}</div>
        <ImageButton
          v-if="hasCancelButton"
          class="cancel-button"
          down-source="images/cancel_btn_down.svg"
          up-source="images/cancel_btn_up.svg"
          disabled-source=""
          :is-disabled="false"
          @clicked="cancel"
        ></ImageButton>
        <div class="cancel-label" v-if="hasCancelButton">{{ $t('common.cancel') }}</div>
        <ImageButton
          :class="hasCancelButton ? 'ok-button-right' : 'ok-button-middle'"
          down-source="images/confirm_btn_down.svg"
          up-source="images/confirm_btn_up.svg"
          disabled-source=""
          :is-disabled="false"
          @clicked="ok"
        ></ImageButton>
        <div :class="hasCancelButton ? 'ok-label-right' : 'ok-label-middle'">
          {{ $t('common.ok') }}
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup lang="ts">
import { defineEmits, defineProps } from 'vue'
import ImageButton from '@/components/ImageButton.vue'

const props = defineProps<{
  modelValue: boolean
  text: string
  hasCancelButton: boolean
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
  (e: 'cancel'): void
  (e: 'ok'): void
}>()

const close = () => {
  emit('update:modelValue', false)
  if (props.hasCancelButton) {
    emit('cancel')
  } else {
    emit('ok')
  }
}

const cancel = () => {
  emit('cancel')
  emit('update:modelValue', false)
}

const ok = () => {
  emit('ok')
  emit('update:modelValue', false)
}
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
  width: 654px;
  height: 584px;
  background: #1d1e20 0% 0% no-repeat padding-box;
  box-shadow: 0px 0px 20px #00000099;
  border-radius: 20px;
  position: relative;
}

.text {
  position: absolute;
  top: 106px;
  left: 95px;
  width: 464px;
  letter-spacing: 1.04px;
  color: #b0b5bf;
  font-family: Lexend-Light;
  font-size: 26px;
  white-space: pre-line;
}

.cancel-button {
  position: absolute;
  top: 328px;
  left: 111px;
}

.cancel-label {
  position: absolute;
  top: 482px;
  left: 75px;
  width: 216px;
  text-align: center;
  letter-spacing: 3.08px;
  color: #b0b5bf;
  font-family: Lexend-Light;
  font-size: 22px;
  white-space: pre-line;
}

.ok-button-right {
  position: absolute;
  top: 328px;
  left: 399px;
}

.ok-label-right {
  position: absolute;
  top: 482px;
  left: 363px;
  width: 216px;
  text-align: center;
  letter-spacing: 3.08px;
  color: #b0b5bf;
  font-family: Lexend-Light;
  font-size: 22px;
  white-space: pre-line;
}

.ok-button-middle {
  position: absolute;
  top: 328px;
  left: 255px;
}

.ok-label-middle {
  position: absolute;
  top: 482px;
  left: 219px;
  width: 216px;
  text-align: center;
  letter-spacing: 3.08px;
  color: #b0b5bf;
  font-family: Lexend-Light;
  font-size: 22px;
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
