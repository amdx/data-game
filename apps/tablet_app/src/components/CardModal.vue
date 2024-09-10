<template>
  <transition name="fade">
    <div v-if="modelValue" class="modal-overlay" @click.self="close">
      <div class="modal">
        <img alt="Action Card" :src="`images/cards/${props.cardId}.jpg`" />
        <ImageButton
          class="close-button"
          down-source="images/close_window_btn_down.svg"
          up-source="images/close_window_btn_up.svg"
          disabled-source=""
          :is-disabled="false"
          @clicked="close"
        ></ImageButton>
        <ImageButton
          class="delete-button"
          down-source="images/delete_card_btn_down.svg"
          up-source="images/delete_card_btn_up.svg"
          disabled-source=""
          :is-disabled="false"
          @clicked="deleteCard"
        ></ImageButton>
        <div class="delete-button-label">{{ $t('graph_view.card_delete_label') }}</div>
      </div>
    </div>
  </transition>
</template>

<script setup lang="ts">
import { defineEmits, defineProps } from 'vue'
import ImageButton from '@/components/ImageButton.vue'

const props = defineProps<{
  modelValue: boolean
  cardId: string
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
  (e: 'deleteCard'): void
}>()

const close = () => {
  emit('update:modelValue', false)
}

const deleteCard = () => {
  emit('deleteCard')
  close()
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
  height: 1058px;
  background: #1d1e20 0% 0% no-repeat padding-box;
  box-shadow: 0px 0px 20px #00000099;
  border-radius: 20px;
  position: relative;
}

.modal img {
  border-radius: 20px;
}

.close-button {
  position: absolute;
  top: 47px;
  right: 47px;
}

.delete-button {
  position: absolute;
  top: 907px;
  left: 271px;
}

.delete-button-label {
  position: absolute;
  top: 928px;
  left: 415px;
  width: 208px;
  height: 86px;
  letter-spacing: 3.08px;
  color: #1d1e20;
  font-size: 22px;
  font-family: Lexend;
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
