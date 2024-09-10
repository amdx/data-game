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

import { createRouter, createWebHistory } from 'vue-router'
import ScenarioChooserView from '@/views/ScenarioChooserView.vue'
import WelcomeView from '@/views/WelcomeView.vue'
import InstructionsView from '@/views/InstructionsView.vue'
import HeroesView from '@/views/HeroesView.vue'
import WaitTeamsView from '@/views/WaitTeamsView.vue'
import ScanningView from '@/views/ScanningView.vue'
import EvaluationView from '@/views/EvaluationView.vue'
import AdminView from '@/views/AdminView.vue'
import GoodbyeView from '@/views/GoodbyeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/scenario'
    },
    {
      path: '/scenario',
      name: 'scenario',
      component: ScenarioChooserView
    },
    {
      path: '/welcome',
      name: 'welcome',
      component: WelcomeView
    },
    {
      path: '/instructions',
      name: 'instructions',
      component: InstructionsView
    },
    {
      path: '/heroes',
      name: 'heroes',
      component: HeroesView
    },
    {
      path: '/teams',
      name: 'teams',
      component: WaitTeamsView
    },
    {
      path: '/scan',
      name: 'scan',
      component: ScanningView
    },
    {
      path: '/evaluation',
      name: 'evaluation',
      component: EvaluationView
    },
    {
      path: '/goodbye',
      name: 'goodbye',
      component: GoodbyeView
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminView
    }
  ]
})

export default router
