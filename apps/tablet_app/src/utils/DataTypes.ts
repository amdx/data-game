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

type ActionDataSet = {
  actionId: string
  actionIndex: number
  actionValues: {
    cost: number
    time: number
    efficiency: number
  }
}

const SessionState = {
  INTRODUCTION: 'INTRODUCTION',
  TEAM_NAMING: 'TEAM_NAMING',
  SCANNING: 'SCANNING',
  EVALUATION: 'EVALUATION'
}

export type { ActionDataSet }
export { SessionState }
