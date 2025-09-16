from typing import List
from datetime import datetime
from enum import Enum

from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey, func, Enum as Sql_enum

from .base import Base
from core.models.mixins import IdPKIntMixin

# abstracts boosts
class BoostType(Enum):
    SPEED = "speed"
    DAMAGE = "damage"
    SHIELD = "shield"


class BoostSource(Enum):
    LEVEL_COMPLETION = "level"
    MANUAL = "manual"

class Player(Base, IdPKIntMixin):
    nickname: Mapped[str] = mapped_column(unique=True, nullable=False)
    first_login: Mapped[datetime] = mapped_column(default=func.now())
    last_login: Mapped[datetime] = mapped_column(default=func.now())
    points: Mapped[int] = mapped_column(default=0)

    boosts: Mapped[List["Boost"]] = relationship("Boost", back_populates="player")


class Boost(Base, IdPKIntMixin):
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"), nullable=False)
    boost_type: Mapped[BoostType] = mapped_column(Sql_enum(BoostType), nullable=False)
    boost_source: Mapped[BoostSource] = mapped_column(Sql_enum(BoostType), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=False)

    player: Mapped["Player"] = relationship("Player", back_populates="boosts")

