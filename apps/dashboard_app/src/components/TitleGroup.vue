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
defineProps(['node'])
</script>

<template>
  <div>
    <span class="title">{{ $t(`${node}.title`) }}</span>
    <span class="subtitle">{{ $t(`${node}.subtitle`) }}</span>
  </div>
</template>

<style scoped>
.title {
  position: absolute;
  font-size: 108px;
  letter-spacing: 8.64px;
  left: 352px;
  top: 147px;
}

.subtitle {
  position: absolute;
  font-family: Lexend-ExtraLight;
  font-size: 64px;
  letter-spacing: 2.56px;
  left: 352px;
  top: 280px;
}
</style>
