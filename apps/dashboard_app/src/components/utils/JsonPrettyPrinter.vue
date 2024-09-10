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
import { computed } from 'vue'

const props = defineProps<{
  name: string
  content: unknown
}>()

const prettyPrint = computed(() => {
  return JSON.stringify(props.content, null, 2)
})
</script>

<template>
  <div class="box">
    <h2>{{ props.name }}</h2>
    <pre v-html="prettyPrint"></pre>
  </div>
</template>

<style scoped>
.box {
  border: 1px solid #999;
  margin: 5px;
  padding: 10px;
}

h2 {
  margin-top: 0;
}
</style>
