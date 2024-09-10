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

<script lang="ts">
export enum ButtonType {
  RESET = 'RESET',
  RESTART_SCAN = 'RESTART_SCAN',
  GOODBYE = 'GOODBYE'
}
</script>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import ConfirmationModal from './ConfirmationModal.vue'
import ImageButton from '@/components/ImageButton.vue'

const props = defineProps<{
  buttons: ButtonType[]
}>()

const router = useRouter()
const { t } = useI18n()

const expanded = ref(false)
const showModal = ref(false)
const selectedButton = ref<ButtonType | null>(null)
const menuBarWidth = computed(() => {
  return `${72 * (props.buttons.length + 1)}px`
})
const confirmationText = computed(() => {
  return t(`ui.confirmation_texts.${selectedButton.value}`)
})

const imagesMap: { [key in ButtonType]: string } = {
  [ButtonType.RESET]: 'reset',
  [ButtonType.RESTART_SCAN]: 'scan_again',
  [ButtonType.GOODBYE]: 'terminate_game'
}

const routeMap: { [key in ButtonType]: string } = {
  [ButtonType.RESET]: '/',
  [ButtonType.RESTART_SCAN]: '/scan',
  [ButtonType.GOODBYE]: '/goodbye'
}

const toggleExpand = () => {
  expanded.value = !expanded.value
}

const handleIconClick = (button: ButtonType) => {
  selectedButton.value = button
  showModal.value = true
}

const handleConfirm = () => {
  if (selectedButton.value) {
    router.push(routeMap[selectedButton.value])
  }
  showModal.value = false
  expanded.value = false
}

const handleCancel = () => {
  showModal.value = false
}
</script>

<template>
  <div :class="['menu', { open: expanded }]">
    <img
      class="menu-btn"
      @click="toggleExpand"
      :src="`${expanded ? 'images/menu/button_menu_minus_btn_up.svg' : 'images/menu/button_menu_btn_up.svg'}`"
      alt="Menu"
    />
    <ImageButton
      v-for="(button, index) in buttons"
      :key="index"
      :id="`menu-button-${index}`"
      :class="['menu-btn', { 'hidden-btn': !expanded }]"
      :down-source="`images/menu/${imagesMap[button]}_btn_down.svg`"
      :up-source="`images/menu/${imagesMap[button]}_btn_up.svg`"
      @click="handleIconClick(button)"
    />
    <ConfirmationModal
      v-if="showModal"
      :visible="showModal"
      :text="confirmationText"
      @confirm="handleConfirm"
      @cancel="handleCancel" />
  </div>
</template>

<style scoped>
.menu {
  position: absolute;
  top: 2048px;
}

.menu::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 64px;
  height: 64px;
  background-color: #27292b;
  border-radius: 32px;
  transition: width 0.2s ease, border-radius 0.2s ease;
  z-index: 1;
}

.menu.open::before {
  width: v-bind(menuBarWidth);
  border-radius: 0 32px 32px 0;
}

.menu-btn {
  width: 64px;
  height: 64px;
  position: absolute;
  top: 0;
  left: 0;
  transition: transform 0.2s ease, opacity 0.2s ease;
  z-index: 2;
}

.hidden-btn {
  opacity: 0;
  pointer-events: none;
}

.menu.open {
  opacity: 1;
  pointer-events: auto;
}

.menu.open #menu-button-0 {
  transform: translateX(72px);
}

.menu.open #menu-button-1 {
  transform: translateX(144px);
}

.menu.open #menu-button-2 {
  transform: translateX(216px);
}
</style>
