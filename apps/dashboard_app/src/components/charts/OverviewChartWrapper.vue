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
defineProps(['title'])
</script>

<template>
  <div class="outer-container">
    <span class="title">{{ title }}</span>
    <div class="chart-container">
      <slot />
    </div>
  </div>
</template>

<style scoped>
.outer-container {
  position: relative;
  width: 100%;
  height: 100%;
}

.title {
  position: absolute;
  font-size: 36px;
  letter-spacing: 2.88px;
  left: 68px;
  top: 51px;
}

.chart-container {
  width: 100%;
  height: 100%;
}
</style>
