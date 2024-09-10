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
import { onMounted, ref } from 'vue'
import { name, version } from '~build/package'
import now from '~build/time'
import { abbreviatedSha } from '~build/git'
import { useApi } from '@/composables/useApi'
import { useErrorStore } from '@/composables/useErrorStore'
import ModalWindow from '@/components/ModalWindow.vue'

defineProps(['visible'])
const emits = defineEmits(['close'])

const api = useApi()
const errorStore = useErrorStore()

const backendVersion = ref()

onMounted(async () => {
  try {
    backendVersion.value = await api.getBackendVersion()
  } catch (error) {
    errorStore.setError(`Unable to get backend version: ${error}`)
  }
})
</script>

<template>
  <ModalWindow :visible="visible" width="2000px" height="750px" @close="emits('close')">
    <div class="about">
      <div class="sidebar"><img class="logo" src="/images/amdx.svg" alt="AMDX" /></div>
      <div class="text">
        <div class="title">Futurium Datagame</div>
        <div class="copyright">&copy; 2024 Archimedes Exhibitions GmbH</div>
        <div class="builddata">
          <table>
            <tr>
              <th>Package version</th>
              <td>{{ name }} v{{ version }}</td>
            </tr>
            <tr>
              <th>Build time</th>
              <td>{{ now }}</td>
            </tr>
            <tr>
              <th>SHA</th>
              <td>{{ abbreviatedSha ? abbreviatedSha : 'N/A' }}</td>
            </tr>
            <tr>
              <th>Backend version</th>
              <td>v{{ backendVersion }}</td>
            </tr>
          </table>
        </div>
      </div>
    </div>
  </ModalWindow>
</template>

<style scoped>
.about {
  position: absolute;
  display: flex;
  gap: 50px;
  flex-direction: row;
  top: 100px;
  left: 100px;
}

.sidebar {
  width: 200px;
  padding-right: 50px;
  border-right: 1px solid #eee;
}

.title {
  font-family: Lexend-ExtraLight;
  font-size: 130px;
}

.copyright {
  font-size: 36px;
}

.builddata {
  padding-top: 100px;
  font-size: 32px;
}

.builddata th {
  width: 250px;
  height: 50px;
  text-align: right;
  padding-right: 20px;
}
</style>