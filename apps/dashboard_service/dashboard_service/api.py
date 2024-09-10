# Copyright (C) 2024 Archimedes Exhibitions GmbH,
# Saarbrücker Str. 24, Berlin, Germany
#
# This file contains proprietary source code and confidential
# information. Its contents may not be disclosed or distributed to
# third parties unless prior specific permission by Archimedes
# Exhibitions GmbH, Berlin, Germany is obtained in writing. This
# applies to copies made in any form and using any medium. It applies
# to partial as well as complete copies.

import csv
import logging
import uuid

import fastapi
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from dashboard_service import __version__
from dashboard_service import api_models
from dashboard_service import configs
from dashboard_service.api_models import ActionCard as ActionCardModel
from dashboard_service.api_models import ActionCards as ActionCardsModel
from dashboard_service.api_models import ActionCardsCreate
from dashboard_service.api_models import Team as TeamModel
from dashboard_service.api_models import MaximaScores as MaximaScoresModel
from dashboard_service.api_models import BestScores as BestScoresModel
from dashboard_service.api_models import (
    ScenarioScoresResponse as ScenarioScoresResponseModel,
)
from dashboard_service.api_models import TeamsEvaluation as EvaluationModel
from dashboard_service.api_models import TotalsEvaluation as TotalsEvaluationModel
from dashboard_service.api_models import TeamCreate
from dashboard_service.api_models import TeamResponse
from dashboard_service.api_models import TeamsResponse as TeamsResponseModel
from dashboard_service.api_models import WorkshopSession as WorkshopSessionModel
from dashboard_service.api_models import WorkshopSessionCreate
from dashboard_service.api_models import (
    WorkshopSessionResponse as WorkshopSessionResponseModel,
)
from dashboard_service.api_models import WorkshopSessionUpdate
from dashboard_service.api_models import WorkshopState as WorkshopStatesModel
from dashboard_service.api_models import TeamsEvaluationResponse
from dashboard_service.database import SessionLocal
from dashboard_service.database import engine
from dashboard_service.db_models import Base
from dashboard_service.db_models import Team
from dashboard_service.db_models import TeamActionCard
from dashboard_service.db_models import WorkshopSession


Base.metadata.create_all(bind=engine)

logger = logging.getLogger(__name__)

router = fastapi.APIRouter()


def get_action_cards() -> ActionCardsModel:
    config = configs.get_config()
    action_cards = []
    with open(config.data_path) as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            action_cards.append(api_models.ActionCard.from_dict(row))
    return ActionCardsModel(action_cards=action_cards)


def get_scenario_action_cards(scenario_id):
    action_cards = get_action_cards().action_cards
    return ActionCardsModel(
        action_cards=[card for card in action_cards if card.scenario == scenario_id]
    )


def get_action_card(card_id: str) -> ActionCardModel | None:
    action_cards = [c for c in get_action_cards().action_cards if c.card_id == card_id]
    if action_cards:
        return action_cards[0]
    return None


def to_percent(value):
    return round(value * 100)


def get_db():
    db = None

    try:
        db = SessionLocal()
        yield db
    finally:
        if db is not None:
            db.close()


def check_team_existance(db, team_id) -> Team:
    team = db.query(Team).filter_by(id=team_id).first()
    if team is None:
        logger.error("Team does not exist!")
        raise HTTPException(404, "Team does not exist!")
    return team


def get_team_action_cards(db, team_id):
    team_action_cards = db.query(TeamActionCard).filter_by(team_id=team_id).all()
    action_card_ids = [c.card_id for c in team_action_cards]
    action_cards = get_action_cards()
    action_cards.action_cards = [
        c for c in action_cards.action_cards if c.card_id in action_card_ids
    ]
    return action_cards


@router.get("/version")
def get_backend_version() -> str:
    return __version__.__version__


@router.get("/action-cards")
def list_action_cards() -> ActionCardsModel:
    return get_action_cards()


@router.post("/session")
def create_session(
    session_create: WorkshopSessionCreate, db: Session = Depends(get_db)
) -> WorkshopSessionResponseModel:
    # Deletes old sessions
    logger.info("Deleting old session...")
    db.query(WorkshopSession).delete()
    db.commit()
    # Deletes teams from old session
    logger.info("Deleting old teams...")
    db.query(Team).delete()
    db.commit()

    logger.info("Creating a new session...")
    workshop_session = WorkshopSession(
        id=str(uuid.uuid4()),
        scenario_id=session_create.scenario_id,
        state=WorkshopStatesModel.INTRODUCTION.name,
    )
    db.add(workshop_session)
    db.commit()
    db.refresh(workshop_session)
    logger.info(f"Created session {workshop_session.id}")
    return WorkshopSessionResponseModel(
        workshop_session=WorkshopSessionModel(
            id=workshop_session.id,
            scenario_id=workshop_session.scenario_id,
            state=workshop_session.state,
        )
    )


@router.get("/scenario/action-cards")
def list_scenario_action_cards(db: Session = Depends(get_db)) -> ActionCardsModel:
    workshop_session = db.query(WorkshopSession).first()
    if workshop_session:
        return get_scenario_action_cards(workshop_session.scenario_id)
    else:
        message = "Session not started!"
        logger.error(message)
        raise HTTPException(409, message)


@router.get("/scenario/scores")
def get_scenario_scores(db: Session = Depends(get_db)) -> ScenarioScoresResponseModel:
    workshop_session = db.query(WorkshopSession).first()
    if workshop_session:
        categories = ("time", "cost", "efficiency")
        action_cards = get_scenario_action_cards(
            workshop_session.scenario_id
        ).action_cards

        # Calculate the scenario's maximum value per category
        maxima = {
            category: max([getattr(card, category) for card in action_cards])
            for category in categories
        }

        # Calculate the scenario's overall scores for the 8 best cards per category
        best_scores = {
            category: sum(
                sorted([getattr(card, category) for card in action_cards])[-8:]
            )
            for category in categories
        }

        return ScenarioScoresResponseModel(
            maxima=MaximaScoresModel(**maxima),
            best=BestScoresModel(**best_scores),
        )
    else:
        message = "Session not started!"
        logger.error(message)
        raise HTTPException(409, message)


@router.put("/session")
def update_session(
    session_update: WorkshopSessionUpdate, db: Session = Depends(get_db)
) -> WorkshopSessionResponseModel:
    if session_update.state == WorkshopStatesModel.SCANNING:
        # Delete team cards
        logger.info("Deleting old team cards...")
        db.query(TeamActionCard).delete()
    workshop_session = db.query(WorkshopSession).first()
    logger.info(
        f"Switching session state from {workshop_session.state} to {session_update.state}..."
    )
    workshop_session.state = session_update.state.name
    db.commit()
    db.refresh(workshop_session)
    return WorkshopSessionResponseModel(
        workshop_session=WorkshopSessionModel(
            id=workshop_session.id,
            scenario_id=workshop_session.scenario_id,
            state=workshop_session.state,
        )
    )


@router.get("/session")
def get_session(db: Session = Depends(get_db)) -> WorkshopSessionResponseModel:
    workshop_session = db.query(WorkshopSession).first()
    if workshop_session:
        return WorkshopSessionResponseModel(
            workshop_session=WorkshopSessionModel(
                id=workshop_session.id,
                scenario_id=workshop_session.scenario_id,
                state=workshop_session.state,
            )
        )
    return WorkshopSessionResponseModel(workshop_session=None)


@router.get("/teams")
def list_groups(db: Session = Depends(get_db)) -> TeamsResponseModel:
    teams = db.query(Team).all()
    config = configs.get_config()
    output_teams = []
    for team in teams:
        output_teams.append(
            TeamModel(
                id=team.id,
                name=team.name,
                has_all_cards=len(team.action_cards) == config.max_card_count,
                action_cards=get_team_action_cards(db, team.id).action_cards,
            )
        )
    return TeamsResponseModel(teams=output_teams)


@router.post("/teams")
def create_team(team_create: TeamCreate, db: Session = Depends(get_db)) -> TeamResponse:
    workshop_session = db.query(WorkshopSession).first()
    if workshop_session.state != WorkshopStatesModel.TEAM_NAMING.name:
        message = "You can't add a team now!"
        logger.error(message)
        raise HTTPException(status_code=403, detail=message)

    config = configs.get_config()
    if len(db.query(Team).all()) < config.max_team_count:
        exists = db.query(Team).filter_by(name=team_create.name).first() is not None
        if exists:
            message = "Team name already exists!"
            logger.error(message)
            raise HTTPException(409, message)

        logger.info(f"Creating new team {team_create.name}...")
        team = Team(name=team_create.name, id=str(uuid.uuid4()))
        db.add(team)
        db.commit()
        db.refresh(team)
        return TeamResponse(
            team=TeamModel(
                id=team.id, name=team.name, has_all_cards=False, action_cards=[]
            )
        )
    else:
        message = "It is not allowed to add more teams!"
        logger.error(message)
        raise HTTPException(403, message)


@router.get("/teams/evaluation")
def get_teams_evaluation(db: Session = Depends(get_db)) -> TeamsEvaluationResponse:
    workshop_session = db.query(WorkshopSession).first()
    if workshop_session:
        categories = ("time", "cost", "efficiency")
        action_cards = get_scenario_action_cards(
            workshop_session.scenario_id
        ).action_cards

        # Calculate best scores per category for 8 cards
        best_scores = {
            category: sum(
                sorted([getattr(card, category) for card in action_cards])[-8:]
            )
            for category in categories
        }

        teams = db.query(Team).all()
        teams_scores = {category: [] for category in categories}

        for team in teams:
            team_action_cards = get_team_action_cards(db, team.id).action_cards
            for category in categories:
                teams_scores[category].append(
                    sum([getattr(card, category) for card in team_action_cards])
                )

        scores_pct = {
            category: [
                to_percent(score / best_scores[category])
                for score in teams_scores[category]
            ]
            for category in categories
        }

        if len(teams) > 0:
            totals_pct = {
                category: to_percent(
                    sum(teams_scores[category]) / (best_scores[category] * len(teams))
                )
                for category in categories
            }
        else:
            totals_pct = {category: 0 for category in categories}

        return TeamsEvaluationResponse(
            teams_evaluation=EvaluationModel(**scores_pct),
            totals_evaluation=TotalsEvaluationModel(**totals_pct),
            team_names=[team.name for team in teams],
        )

    else:
        message = "Session not started!"
        logger.error(message)
        raise HTTPException(409, message)


@router.get("/teams/{team_id}")
def get_team(team_id: str, db: Session = Depends(get_db)) -> TeamResponse:
    config = configs.get_config()
    team = check_team_existance(db, team_id)
    team_model = TeamModel(
        id=team.id,
        name=team.name,
        has_all_cards=len(team.action_cards) == config.max_card_count,
        action_cards=get_team_action_cards(db, team.id).action_cards,
    )
    return TeamResponse(team=team_model)


@router.delete("/teams/{team_id}")
def delete_team(team_id: str, db: Session = Depends(get_db)) -> TeamResponse:
    config = configs.get_config()
    team = check_team_existance(db, team_id)
    team_model = TeamModel(
        id=team.id,
        name=team.name,
        has_all_cards=len(team.action_cards) == config.max_card_count,
        action_cards=get_team_action_cards(db, team.id).action_cards,
    )

    db_query = db.query(Team).filter_by(id=team_id)
    db_query.delete()
    db_query = db.query(TeamActionCard).filter_by(team_id=team_id)
    db_query.delete()
    db.commit()

    return TeamResponse(team=team_model)


@router.get("/teams/{team_id}/action-cards")
def list_team_action_cards(
    team_id: str, db: Session = Depends(get_db)
) -> ActionCardsModel:
    check_team_existance(db, team_id)
    action_cards = get_team_action_cards(db, team_id)
    return action_cards


@router.post("/teams/{team_id}/action-cards")
def add_team_action_cards(
    team_id: str, action_cards_create: ActionCardsCreate, db: Session = Depends(get_db)
) -> ActionCardsModel:
    check_team_existance(db, team_id)

    card_ids = []
    workshop_session = db.query(WorkshopSession).first()

    # Check if session is in scanning state
    if workshop_session.state != WorkshopStatesModel.SCANNING.name:
        message = "You can't add a team cards now!"
        logger.error(message)
        raise HTTPException(403, message)

    # Check if to many cards where added
    config = configs.get_config()
    existing_cards = db.query(TeamActionCard).filter_by(team_id=team_id).all()
    card_count = len(existing_cards)
    if (
        card_count >= config.max_card_count
        or card_count + len(action_cards_create.action_cards) > config.max_card_count
    ):
        message = "You can not add more cards, reached max count!"
        logger.error(message)
        raise HTTPException(403, message)

    for card_create in action_cards_create.action_cards:
        # Check if scenario matches
        scenario_id = card_create.card_id.split("_")[0]
        if scenario_id != workshop_session.scenario_id:
            message = f"Card {card_create.card_id} is from wrong scenario!"
            logger.error(message)
            raise HTTPException(409, message)

        # Check if card was already added
        exists = (
            db.query(TeamActionCard)
            .filter_by(card_id=card_create.card_id, team_id=team_id)
            .first()
            is not None
        )
        if exists:
            message = f"Card {card_create.card_id} was already added to team!"
            logger.error(message)
            raise HTTPException(409, message)

        if get_action_card(card_create.card_id):
            logger.info(
                f"Adding new action card {card_create.card_id} to team {team_id}..."
            )
            db_card = TeamActionCard(card_id=card_create.card_id, team_id=team_id)
            db.add(db_card)
            db.commit()
            db.refresh(db_card)
            card_ids.append(db_card.card_id)
        else:
            message = f"Card {card_create.card_id} does not exist!"
            logger.error(message)
            raise HTTPException(404, message)

    return ActionCardsModel(action_cards=[get_action_card(c_id) for c_id in card_ids])


@router.delete("/teams/{team_id}/action-cards")
def delete_team_action_cards(
    team_id: str, action_cards_delete: ActionCardsCreate, db: Session = Depends(get_db)
) -> ActionCardsModel:
    card_ids = []

    for card_delete in action_cards_delete.action_cards:
        # Check if card was already added
        exists = (
            db.query(TeamActionCard)
            .filter_by(card_id=card_delete.card_id, team_id=team_id)
            .first()
            is not None
        )
        if exists:
            db_query = db.query(TeamActionCard).filter_by(
                card_id=card_delete.card_id, team_id=team_id
            )
            db_query.delete()
            db.commit()
            card_ids.append(card_delete.card_id)
        else:
            message = f"Card {card_delete.card_id} does not exist!"
            logger.error(message)
            raise HTTPException(404, message)

    return ActionCardsModel(action_cards=[get_action_card(c_id) for c_id in card_ids])
