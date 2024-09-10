# Copyright (C) 2024 Archimedes Exhibitions GmbH,
# Saarbrücker Str. 24, Berlin, Germany
#
# This file contains proprietary source code and confidential
# information. Its contents may not be disclosed or distributed to
# third parties unless prior specific permission by Archimedes
# Exhibitions GmbH, Berlin, Germany is obtained in writing. This
# applies to copies made in any form and using any medium. It applies
# to partial as well as complete copies.
from enum import Enum
from typing import Self

from pydantic import BaseModel


class WorkshopState(Enum):
    # If you rename those, rename them in dashboard_app and tablet_app too!
    INTRODUCTION = "INTRODUCTION"
    TEAM_NAMING = "TEAM_NAMING"
    SCANNING = "SCANNING"
    EVALUATION = "EVALUATION"


class ActionCardCreate(BaseModel):
    card_id: str


class ActionCard(ActionCardCreate):
    scenario: str
    card_number: int
    cost: float
    time: float
    efficiency: float

    @classmethod
    def from_dict(cls, card_dict: dict[str]) -> Self:
        return cls(
            scenario=card_dict["scenario"],
            card_number=int(card_dict["card_number"]),
            card_id=card_dict["qr_id"],
            cost=float(card_dict["cost"]),
            time=float(card_dict["time"]),
            efficiency=float(card_dict["efficiency"]),
        )


class ActionCardsCreate(BaseModel):
    action_cards: list[ActionCardCreate]


class ActionCards(BaseModel):
    action_cards: list[ActionCard]


class WorkshopSessionCreate(BaseModel):
    scenario_id: str


class WorkshopSessionUpdate(BaseModel):
    state: WorkshopState


class WorkshopSession(WorkshopSessionCreate):
    state: WorkshopState
    id: str


class WorkshopSessionResponse(BaseModel):
    workshop_session: WorkshopSession | None


class TeamCreate(BaseModel):
    name: str


class Team(TeamCreate):
    id: str
    has_all_cards: bool
    action_cards: list[ActionCard]


class TeamResponse(BaseModel):
    team: Team


class TeamsResponse(BaseModel):
    teams: list[Team]


class TeamsEvaluation(BaseModel):
    time: list[int]
    cost: list[int]
    efficiency: list[int]


class TotalsEvaluation(BaseModel):
    time: float
    cost: float
    efficiency: float


class TeamsEvaluationResponse(BaseModel):
    teams_evaluation: TeamsEvaluation
    totals_evaluation: TotalsEvaluation
    team_names: list[str]


class MaximaScores(BaseModel):
    time: int
    cost: int
    efficiency: int


class BestScores(BaseModel):
    time: int
    cost: int
    efficiency: int


class ScenarioScoresResponse(BaseModel):
    maxima: MaximaScores
    best: BestScores
