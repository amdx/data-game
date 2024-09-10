<script setup lang="ts">

import {
  type WorkshopSession,
  type Team,
  type WorkshopState,
  type ActionCard,
  getSessionApiV1SessionGet,
  listGroupsApiV1TeamsGet,
  getTeamsEvaluationApiV1TeamsEvaluationGet,
  updateSessionApiV1SessionPut,
  createSessionApiV1SessionPost,
  createTeamApiV1TeamsPost,
  listScenarioActionCardsApiV1ScenarioActionCardsGet,
  addTeamActionCardsApiV1TeamsTeamIdActionCardsPost, type TeamsEvaluationResponse
} from '@/client'
import { onUnmounted, reactive } from 'vue'
import JsonPrettyPrinter from '@/components/utils/JsonPrettyPrinter.vue';

const state = reactive<{
  initialized: boolean
  session: WorkshopSession | null
  teams: Team[]
  evaluation: TeamsEvaluationResponse | null
}>({
  initialized: false,
  session: null,
  teams: [],
  evaluation: null
})

const formData = reactive<{
  wantedState: string | undefined
  wantedScenario: string | undefined
  teamName: string | undefined
}>({
  wantedState: undefined,
  wantedScenario: undefined,
  teamName: undefined
})

const teamNames = ['Foos', 'Bars', 'The Bazes', 'A quite long name', 'Brunos', 'Marios']
let currentNameIndex = 1

const poll = async () => {
  state.session = (await getSessionApiV1SessionGet()).data.workshop_session
  state.teams = (await listGroupsApiV1TeamsGet()).data.teams
  state.evaluation = (await getTeamsEvaluationApiV1TeamsEvaluationGet()).data
  formData.wantedState = state.session?.state
  formData.wantedScenario = state.session?.scenario_id
  state.initialized = true
}

const updateState = async () => {
  await updateSessionApiV1SessionPut({ body: { state: formData.wantedState as WorkshopState } })
  await poll()
}

const setScenario = async () => {
  await createSessionApiV1SessionPost({ body: { scenario_id: formData.wantedScenario as string } })
  await poll()
}

const addTeam = async () => {
  try {
    await createTeamApiV1TeamsPost({ body: { name: formData.teamName as string } })
  } catch (error) {
    console.log(error)
  }
  formData.teamName = teamNames[currentNameIndex]
  currentNameIndex = (currentNameIndex + 1) % teamNames.length
  await poll()
}

const addRandomCards = async (team: Team, partial: Boolean) => {
  try {
    const actionCards = (await listScenarioActionCardsApiV1ScenarioActionCardsGet()).data.action_cards
    const selectedCards: ActionCard[] = []
    const usedIndices: Set<number> = new Set()

    let extractions = 8
    if (partial) {
      extractions = Math.floor(Math.random() * 8)
    }
    while (selectedCards.length < extractions) {
      const randomIndex = Math.floor(Math.random() * actionCards.length)
      if (!usedIndices.has(randomIndex)) {
        usedIndices.add(randomIndex)
        selectedCards.push(actionCards[randomIndex])
      }
    }

    await addTeamActionCardsApiV1TeamsTeamIdActionCardsPost({
      path: { team_id: team.id },
      body: { action_cards: selectedCards.map(card => ({card_id: card.card_id})) }
    })
  } catch (error) {
    console.log(error)
  }
}

formData.teamName = teamNames[0]
poll()

const intervalId = setInterval(poll, 1000)
poll()

onUnmounted(() => {
  clearInterval(intervalId)
})
</script>

<template>
  <div v-if="state.initialized" class="main">
    <div class="modder">
      <h1>Deus ex machina</h1>
      <div class="form-container">
        <form @submit.prevent="setScenario">
          <div class="form-group">
            <label for="state">Set scenario</label>
            <select id="state" v-model="formData.wantedScenario" @change="setScenario">
              <option
                v-for="scenario in ['001', '002', '003']"
                :key="scenario" :value="scenario">
                {{ scenario }}
              </option>
            </select>
            <button type="submit">Force update</button>
          </div>
        </form>
      </div>
      <div class="form-container">
        <form @submit.prevent="updateState">
          <div class="form-group">
            <label for="state">Update state</label>
            <select id="state" v-model="formData.wantedState" @change="updateState">
              <option
                v-for="state in ['INTRODUCTION', 'TEAM_NAMING', 'SCANNING', 'EVALUATION']"
                :key="state" :value="state">
                {{ state }}
              </option>
            </select>
          </div>
        </form>
      </div>
      <div v-if="state.session?.state === 'TEAM_NAMING'" class="form-container">
        <form @submit.prevent="addTeam">
          <div class="form-group">
            <label for="name">Team name</label>
            <input v-model="formData.teamName" type="text" />
            <button type="submit">Add team</button>
          </div>
        </form>
      </div>
      <div v-if="state.session?.state === 'SCANNING'" class="form-container">
        <div class="form-group">
          <label>Action cards</label>
          <div v-for="(team, index) in state.teams" :key="index" class="team-container">
            <span>Team {{ index + 1 }} : {{ team.name }}</span>
            <button @click="addRandomCards(team, true)">Add some cards</button>
            <button @click="addRandomCards(team, false)">Add all cards</button>
          </div>
        </div>
      </div>
    </div>
    <div>
      <h1>The dump</h1>
      <div class="dump-container">
        <div class="column">
          <JsonPrettyPrinter name="Session" :content="state.session" />
          <JsonPrettyPrinter name="Teams" :content="state.teams" />
        </div>
        <div>
          <JsonPrettyPrinter name="Evaluation" :content="state.evaluation" />
        </div>
      </div>
    </div>
  </div>
  <div v-else>Loading..</div>
</template>

<style scoped>
.main {
  display: flex;
  flex-flow: row;
}

.modder {
  margin-left: 20px;
  margin-right: 50px;
  width: 30%;
}

.form-container {
}

.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 15px;
}

label {
  margin-bottom: 5px;
  font-weight: bold;
}

select, input {
  padding: 8px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

select:focus {
  border-color: #007BFF;
  outline: none;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

.dump-container {
  display: grid;
  grid-template-columns: 1fr 1fr; /* Two equal-width columns */
  gap: 20px; /* Space between columns */
}

.column {
  display: flex;
  flex-direction: column;
  gap: 10px; /* Space between the boxes in the column */
}

.team-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-bottom: 10px;
}

.team-container span {
  flex-grow: 1;
}
</style>
