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
import { useErrorStore } from '@/composables/useErrorStore'
import { useRouter } from 'vue-router'

const errorStore = useErrorStore()
const router = useRouter()

const hide = () => {
  errorStore.clearError()
  router.push('/')
}
</script>

<template>
  <div v-if="errorStore.message.value" class="error-notification" @click="hide">
    <img src="/images/warning.svg" alt="Warning" width="80" height="80" />
    <p>{{ errorStore.message }}</p>
  </div>
</template>

<style scoped>
.error-notification {
  position: fixed;
  display: flex;
  flex-flow: row;
  top: 20px;
  right: 20px;
  background-color: red;
  color: white;
  padding: 15px;
  border-radius: 10px;
}

.error-notification p {
  font-size: 24px;
}
</style>
