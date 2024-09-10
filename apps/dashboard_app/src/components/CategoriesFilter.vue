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
import { useUserConfig } from '@/composables/useUserConfig'

defineProps(['categoryFilterFlags'])
const emit = defineEmits(['click'])

const userConfig = useUserConfig()
</script>

<template>
  <div class="categories">
    <div v-for="(category, index) in userConfig?.graphs.categories"
         :key="index"
         class="category"
         @click="emit('click', category)">
      <div class="circle"
           :style="{backgroundColor: categoryFilterFlags[category] ? userConfig?.graphs.colors[category] : '#27292B'}" />
      <div class="category-caption">{{ $t(`charts.categories.${category}`) }}</div>
    </div>
  </div>

</template>

<style scoped>
.categories {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.category {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  flex-grow: 1;
}

.circle {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: red;
}

.category-caption {
  font-size: 30px;
  letter-spacing: 1.2px;
  color: #8D9199;
  flex-grow: 1;
  padding-top: 26px;
}
</style>