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

import {
  type WorkshopState,
  createSessionApiV1SessionPost,
  getSessionApiV1SessionGet,
  listGroupsApiV1TeamsGet,
  updateSessionApiV1SessionPut,
  getTeamsEvaluationApiV1TeamsEvaluationGet,
  getScenarioScoresApiV1ScenarioScoresGet, getBackendVersionApiV1VersionGet
} from '@/client'

export {
  type Team
} from '@/client'

export type ScenarioId = '001' | '002' | '003'

const getBackendVersion = async () => {
  const response = await getBackendVersionApiV1VersionGet()
  if ('message' in response) {
    throw new Error(response.message)
  }
  return response.data
}
const startSession = async (scenario: ScenarioId) => {
  const response = await createSessionApiV1SessionPost({ body: { scenario_id: scenario } })
  if ('message' in response) {
    throw new Error(response.message)
  }
}

const getScenarioId = async () => {
  const response = (await getSessionApiV1SessionGet())
  if ('message' in response) {
    throw new Error(response.message)
  }
  return response.data.workshop_session?.scenario_id as ScenarioId
}

const getTeams = async () => {
  const response = await listGroupsApiV1TeamsGet()
  if ('message' in response) {
    throw new Error(response.message)
  }
  return response.data.teams
}

const getEvaluation = async () => {
  const response = await getTeamsEvaluationApiV1TeamsEvaluationGet()
  if ('message' in response) {
    throw new Error(response.message)
  }
  return response.data
}

const setState = async (state: WorkshopState) => {
  const response = await updateSessionApiV1SessionPut({ body: { state: state } })
  if ('message' in response) {
    throw new Error(response.message)
  }
  return response.data
}

const getScenarioScores = async () => {
  const response = await getScenarioScoresApiV1ScenarioScoresGet()
  if ('message' in response) {
    throw new Error(response.message)
  }
  return response.data
}

export const useApi = () => ({
  getBackendVersion,
  startSession,
  getScenarioId,
  getTeams,
  getEvaluation,
  setState,
  getScenarioScores
})
