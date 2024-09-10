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

<script setup lang="ts">
import { computed, nextTick, onMounted, ref, watchEffect } from 'vue'

const props = defineProps<{ items: string[] }>()
const emit = defineEmits(['select', 'closed'])

const isExpanded = ref(false)
const tansitionClosed = ref(true)
const activeTitle = ref(props.items[0])
const dropdownBody = ref<HTMLElement | null>(null)

const onTransitionStart = () => {
  tansitionClosed.value = false
}

const onTransitionDone = () => {
  tansitionClosed.value = true
  emit('closed', props.items.indexOf(activeTitle.value))
}

const toggle = () =>  {
  isExpanded.value = !isExpanded.value
  nextTick(() => {
    if (dropdownBody.value) {
      dropdownBody.value.style.maxHeight = isExpanded.value
        ? `${dropdownBody.value.scrollHeight}px`
        : '0'
    }
  })
}

const selectItem = (item: string, index: number) => {
  activeTitle.value = item
  nextTick(() => {
    if (dropdownBody.value) {
      dropdownBody.value.style.maxHeight = '0'
    }
    isExpanded.value = false
  })
  emit('select', props.items.indexOf(item))
}

const filteredItems = computed(() => {
  return props.items.filter((item) => item !== activeTitle.value)
})

watchEffect(() => {
  if (!props.items.includes(activeTitle.value)) {
    activeTitle.value = props.items[0]
  }
})

onMounted(() => {
  if (dropdownBody.value) {
    dropdownBody.value.style.maxHeight = '0'
  }
})
</script>

<template>
  <div class="dropdown-menu">
    <div class="dropdown-header" @click="toggle">
      <span>{{ activeTitle }}</span>
      <img
        class="arrow-icon"
        :class="{ 'arrow-rotate': isExpanded }"
        src="/images/dropdown_icon_open.svg"
        alt="arrow"
      />
      <div v-if="!tansitionClosed" class="divider"></div>
    </div>
    <transition @before-enter="onTransitionStart" @after-leave="onTransitionDone" name="dropdown">
      <div v-show="isExpanded" class="dropdown-body" ref="dropdownBody">
        <div
          class="dropdown-item"
          v-for="(item, index) in filteredItems"
          :key="index"
          @click="selectItem(item, index)"
        >
          {{ item }}
          <div v-if="index < filteredItems.length - 1" class="divider"></div>
        </div>
      </div>
    </transition>
  </div>
</template>

<style scoped>
.dropdown-menu {
  width: 683px;
  position: relative; /* Ensure relative positioning for absolute arrow */
  text-align: left;
  letter-spacing: 3.2px;
  font-size: 40px;
  box-shadow: 0px 0px 5px #000000cc;
  border-radius: 4px;
  background-color: #1e1f20;
}

.dropdown-header {
  padding-left: 37px;
  padding-right: 37px;
  position: relative;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 78px;
}

.arrow-icon {
  transition: transform 0.3s ease;
  transform: rotate(90deg);
}

.arrow-rotate {
  transform: rotate(0deg);
}

.dropdown-body {
  overflow: hidden;
  transition: max-height 0.3s ease;
}

.dropdown-item {
  padding-left: 37px;
  padding-right: 37px;
  position: relative;
  color: #8d9199;
  height: 78px;
  line-height: 78px;
}

.divider {
  height: 1px;
  background-color: #5e6166;
  position: absolute;
  left: 30px;
  right: 30px;
  bottom: 0;
}

/* Transition classes */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: max-height 0.3s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
  max-height: 0;
}
</style>
