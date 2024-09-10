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

import type { AxiosResponse } from 'axios'
import axios from 'axios'
import { SessionState } from '@/utils/DataTypes'
import { eventBus } from '@/utils/EventBus'

class BackendHandler {
  public cardCount: number = 8
  public backendPath: string = '/api/v1'
  public pollingInterval: number = 3000
  public requestTimeout: number = 2000
  public sessionState: string | undefined = undefined
  public scenarioId: string | undefined = undefined
  public cardData:
    | {
        card_id: string
        scenario: string
        card_number: number
        cost: number
        time: number
        efficiency: number
      }[]
    | undefined = undefined
  pollerId: any | undefined = undefined
  public scannedIds: string[] = []
  _teamId: string | undefined = undefined

  constructor() {}

  get teamId() {
    const storageTeamId = localStorage.getItem('teamId')
    this._teamId =
      storageTeamId === null || storageTeamId === 'undefined' ? undefined : storageTeamId
    return this._teamId
  }

  set teamId(teamId) {
    localStorage.setItem('teamId', teamId!)
    this._teamId = teamId
  }

  getCardById(cardId: string) {
    if (this.cardData !== undefined) {
      return this.cardData.find((card) => card.card_id === cardId)
    }
    return undefined
  }

  getCardByNumber(cardNumber: number) {
    if (this.cardData !== undefined) {
      return this.cardData.find((card) => {
        return card.card_number === cardNumber && this.getCardScenario(card) === this.scenarioId
      })
    }
    return undefined
  }

  getGraphLabels() {
    this.scannedIds.sort()
    return this.scannedIds.map((id) => this.getCardById(id)!.card_number)
  }

  getCardScenario(card: any) {
    return card.card_id.split('_')[0]
  }

  getMaxCostValue() {
    return Math.max(
      ...this.cardData!.filter((card) => this.getCardScenario(card) === this.scenarioId).map(
        (card) => card.cost
      )
    )
  }

  getMaxTimeValue() {
    return Math.max(
      ...this.cardData!.filter((card) => this.getCardScenario(card) === this.scenarioId).map(
        (card) => card.time
      )
    )
  }

  getMaxEfficiencyValue() {
    return Math.max(
      ...this.cardData!.filter((card) => this.getCardScenario(card) === this.scenarioId).map(
        (card) => card.efficiency
      )
    )
  }

  getOverallCostValue() {
    if (this.cardData !== undefined) {
      const sortedValues = this.cardData!.filter(
        (card) => this.getCardScenario(card) === this.scenarioId
      )
        .map((card) => card.cost)
        .sort((a, b) => a - b)
        .reverse()
      return sortedValues.slice(0, 8).reduce((accumulator, currentValue) => {
        return accumulator + currentValue
      }, 0)
    }
    return 0
  }

  getOverallTimeValue() {
    if (this.cardData !== undefined) {
      const sortedValues = this.cardData!.filter(
        (card) => this.getCardScenario(card) === this.scenarioId
      )
        .map((card) => card.time)
        .sort((a, b) => a - b)
        .reverse()
      return sortedValues.slice(0, 8).reduce((accumulator, currentValue) => {
        return accumulator + currentValue
      }, 0)
    }
    return 0
  }

  getOverallEfficiencyValue() {
    if (this.cardData !== undefined) {
      const sortedValues = this.cardData!.filter(
        (card) => this.getCardScenario(card) === this.scenarioId
      )
        .map((card) => card.efficiency)
        .sort((a, b) => a - b)
        .reverse()
      return sortedValues.slice(0, 8).reduce((accumulator, currentValue) => {
        return accumulator + currentValue
      }, 0)
    }
    return 0
  }

  getCostSum() {
    if (this.cardData !== undefined) {
      return this.scannedIds
        .map((id) => this.getCardById(id)!.cost)
        .reduce((accumulator, currentValue) => {
          return accumulator + currentValue
        }, 0)
    }
    return 0
  }

  getTimeSum() {
    if (this.cardData !== undefined) {
      return this.scannedIds
        .map((id) => this.getCardById(id)!.time)
        .reduce((accumulator, currentValue) => {
          return accumulator + currentValue
        }, 0)
    }
    return 0
  }

  getEfficiencySum() {
    if (this.cardData !== undefined) {
      return this.scannedIds
        .map((id) => this.getCardById(id)!.efficiency)
        .reduce((accumulator, currentValue) => {
          return accumulator + currentValue
        }, 0)
    }
    return 0
  }

  getGraphDatasets(timeColor: string, costColor: string, efficiencyColor: string) {
    this.scannedIds.sort()
    return [
      {
        data: this.scannedIds.map((id) =>
          Math.round((this.getCardById(id)!.time / this.getMaxTimeValue()) * 100)
        ),
        backgroundColor: timeColor,
        borderColor: timeColor,
        borderWidth: 0,
        pointRadius: 0
      },
      {
        data: this.scannedIds.map((id) =>
          Math.round((this.getCardById(id)!.cost / this.getMaxCostValue()) * 100)
        ),
        backgroundColor: costColor,
        borderColor: costColor,
        borderWidth: 0,
        pointRadius: 0
      },
      {
        data: this.scannedIds.map((id) =>
          Math.round((this.getCardById(id)!.efficiency / this.getMaxEfficiencyValue()) * 100)
        ),
        backgroundColor: efficiencyColor,
        borderColor: efficiencyColor,
        borderWidth: 0,
        pointRadius: 0
      }
    ]
  }

  getDonutGraphDatasets(
    timeColor: string | undefined,
    costColor: string | undefined,
    efficiencyColor: string | undefined
  ) {
    this.scannedIds.sort()
    const maxTime = this.getMaxTimeValue()
    const maxCost = this.getMaxCostValue()
    const maxEfficiency = this.getMaxEfficiencyValue()
    const allData = []
    for (const id of this.scannedIds) {
      const data = []
      const backgroundColor = []
      const borderWidth = []
      let cutOutValue = 0
      if (timeColor !== undefined) {
        const value = Math.round((this.getCardById(id)!.time / maxTime) * 100)
        data.push(value)
        cutOutValue += 100 - value
        backgroundColor.push(timeColor)
        borderWidth.push(0)
      }
      if (costColor !== undefined) {
        const value = Math.round((this.getCardById(id)!.cost / maxCost) * 100)
        data.push(value)
        cutOutValue += 100 - value
        backgroundColor.push(costColor)
        borderWidth.push(0)
      }
      if (efficiencyColor !== undefined) {
        const value = Math.round((this.getCardById(id)!.efficiency / maxEfficiency) * 100)
        data.push(value)
        cutOutValue += 100 - value
        backgroundColor.push(efficiencyColor)
        borderWidth.push(0)
      }
      data.push(cutOutValue)
      backgroundColor.push('#2D2C30')
      borderWidth.push(0)

      allData.push({
        data: data,
        backgroundColor: backgroundColor,
        borderWidth: borderWidth
      })
    }
    return allData
  }

  getPolarGraphDatasets(
    timeColor: string | undefined,
    costColor: string | undefined,
    efficiencyColor: string | undefined
  ) {
    this.scannedIds.sort()
    const maxTime = this.getMaxTimeValue()
    const maxCost = this.getMaxCostValue()
    const maxEfficiency = this.getMaxEfficiencyValue()
    const data = []
    const backgroundColor = []
    const borderColor = []
    const borderWidth = []

    for (const id of this.scannedIds) {
      if (timeColor !== undefined) {
        const value = Math.round((this.getCardById(id)!.time / maxTime) * 100)
        data.push(value)
        backgroundColor.push(timeColor)
        borderColor.push(timeColor)
        borderWidth.push(0)
      }
      if (costColor !== undefined) {
        const value = Math.round((this.getCardById(id)!.cost / maxCost) * 100)
        data.push(value)
        backgroundColor.push(costColor)
        borderColor.push(costColor)
        borderWidth.push(0)
      }
      if (efficiencyColor !== undefined) {
        const value = Math.round((this.getCardById(id)!.efficiency / maxEfficiency) * 100)
        data.push(value)
        backgroundColor.push(efficiencyColor)
        borderColor.push(efficiencyColor)
        borderWidth.push(0)
      }
      data.push(0)
      backgroundColor.push('#000000')
      borderColor.push('#000000')
      borderWidth.push(0)
    }
    return {
      data: data,
      backgroundColor: backgroundColor,
      borderColor: borderColor,
      borderWidth: borderWidth
    }
  }

  startCommunication(): void {
    this.pollSession()
    this.pollerId = setInterval(this.pollSession.bind(this), this.pollingInterval)
  }

  stopCommunication(): void {
    clearInterval(this.pollerId)
  }

  pollSession(): void {
    axios({
      url: `${this.backendPath}/session`,
      method: 'get',
      timeout: this.requestTimeout
    }).then((response) => {
      const workshop_session = response.data.workshop_session
      if (workshop_session) {
        this.scenarioId = workshop_session.scenario_id
        const incommingState = SessionState[workshop_session.state as keyof typeof SessionState]
        if (incommingState !== this.sessionState) {
          this.sessionState = incommingState
          eventBus.emit('newState', incommingState)
        }
      } else {
        if (this.sessionState !== SessionState.INTRODUCTION) {
          this.sessionState = SessionState.INTRODUCTION
          eventBus.emit('newState', SessionState.INTRODUCTION)
        }
      }
    })

    if (this.cardData === undefined) {
      axios({
        url: `${this.backendPath}/action-cards`,
        method: 'get',
        timeout: this.requestTimeout
      }).then((response) => {
        this.cardData = response.data.action_cards
      })
    }
  }

  async sendTeamName(name: string): Promise<AxiosResponse | any> {
    if (this.teamId === undefined) {
      return axios({
        url: `${this.backendPath}/teams`,
        method: 'post',
        timeout: this.requestTimeout,
        data: { name: name }
      })
    } else {
      return axios({
        url: `${this.backendPath}/teams/${this.teamId}`,
        method: 'get',
        timeout: this.requestTimeout
      })
        .then((response) => {
          if (response.status === 200) {
            const error = new Error('Ihr habt bereits einen Namen gewählt!')
            return Promise.reject(error)
          } else {
            return axios({
              url: `${this.backendPath}/teams`,
              method: 'post',
              timeout: this.requestTimeout,
              data: { name: name }
            })
          }
        })
        .catch((error) => {
          if (error.response && error.response.status === 404) {
            return axios({
              url: `${this.backendPath}/teams`,
              method: 'post',
              timeout: this.requestTimeout,
              data: { name: name }
            })
          } else {
            return Promise.reject(error)
          }
        })
    }
  }

  sendTeamCards(): Promise<AxiosResponse> {
    return axios({
      url: `${this.backendPath}/teams/${this.teamId}/action-cards`,
      method: 'post',
      timeout: this.requestTimeout,
      data: { action_cards: this.scannedIds.map((cardId) => ({ card_id: cardId })) }
    })
  }
}

export const backendHandler = new BackendHandler()
