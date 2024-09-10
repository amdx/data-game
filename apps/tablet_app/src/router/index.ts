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
// import type { RouteRecordNameGeneric } from 'vue-router'
import StandByView from '../views/StandByView.vue'
import WelcomeView from '@/views/WelcomeView.vue'
import TeamNameView from '@/views/TeamNameView.vue'
import ScanIntroView from '@/views/ScanIntroView.vue'
import ScanView from '@/views/ScanView.vue'
import GraphView from '@/views/GraphView.vue'
import EvaluationView from '@/views/EvaluationView.vue'

// let lastView: RouteRecordNameGeneric = undefined

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'standBy',
      component: StandByView
    },
    {
      path: '/welcome',
      name: 'welcome',
      component: WelcomeView
    },
    {
      path: '/team-name',
      name: 'teamName',
      component: TeamNameView
    },
    {
      path: '/scan-intro',
      name: 'scanIntro',
      component: ScanIntroView
    },
    {
      path: '/scan',
      name: 'scan',
      component: ScanView
    },
    {
      path: '/graph',
      name: 'graph',
      component: GraphView
    },
    {
      path: '/evaluation',
      name: 'evaluation',
      component: EvaluationView
    }
  ]
})

// router.beforeEach((to, from) => {
//   // Prevent app from going back
//   if (lastView && to.name === lastView) {
//     return false
//   }
//   lastView = from.name
//   return true
// })

export default router
