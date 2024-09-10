# Copyright (C) 2024 Archimedes Exhibitions GmbH,
# Saarbrücker Str. 24, Berlin, Germany
#
# This file contains proprietary source code and confidential
# information. Its contents may not be disclosed or distributed to
# third parties unless prior specific permission by Archimedes
# Exhibitions GmbH, Berlin, Germany is obtained in writing. This
# applies to copies made in any form and using any medium. It applies
# to partial as well as complete copies.

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from dashboard_service.database import Base


class WorkshopSession(Base):
    __tablename__ = "workshop_sessions"

    id = Column(String, primary_key=True)
    scenario_id = Column(String)
    state = Column(String)


class Team(Base):
    __tablename__ = "teams"

    id = Column(String, primary_key=True)
    name = Column(String)

    action_cards = relationship("TeamActionCard", back_populates="team")


class TeamActionCard(Base):
    __tablename__ = "action_cards"

    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(String)
    team_id = Column(String, ForeignKey("teams.id"))

    team = relationship("Team", back_populates="action_cards")
