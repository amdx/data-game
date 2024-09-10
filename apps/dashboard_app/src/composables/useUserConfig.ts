/*
 * Copyright (C) 2024. Archimedes Exhibitions GmbH,
 * Saarbrücker Str. 24, Berlin, Germany
 *
 * This file contains proprietary source code and confidential
 * information. Its contents may not be disclosed or distributed to
 * third parties unless prior specific permission by Archimedes
 * Exhibitions GmbH, Berlin, Germany is obtained in writing. This applies
 * to copies made in any form and using any medium. It applies to
 * partial as well as complete copies.
 */

import { ref, inject, type Ref, type App } from 'vue'

const userConfigSymbol = Symbol('userConfig')

export type Category = 'time' | 'cost' | 'efficiency'

interface UserConfig {
  graphs: {
    colors: Record<Category, string>
    categories: Category[]
  },
  dotlottie: {
    wasmUrl: string
  }
}

const config = ref<UserConfig | null>(null)

async function loadConfig() {
  const response = await fetch('config.json')
  const data: UserConfig = await response.json()
  config.value = data
}

export async function provideUserConfig(app: App) {
  app.provide(userConfigSymbol, config)
  await loadConfig().catch(console.error)
}

export function useUserConfig() {
  const config = inject<Ref<UserConfig | null>>(userConfigSymbol)
  if (!config) {
    throw new Error('useUserConfig must be used after provideUserConfig')
  }
  return config
}
