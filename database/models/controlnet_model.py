from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.mysql import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.sql.expression import text

from database.db import Base


class ControlnetModelModel(Base):
    __tablename__ = "controlnet_models"

    id = Column(Integer, primary_key=True, autoincrement=True)

    model = Column(String(255), nullable=False, unique=True)

    created_at = Column(TIMESTAMP, nullable=False, default=current_timestamp())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    controlnet_illustrations = relationship("ControlnetIllustrationModel", back_populates="controlnet_model", cascade="delete, delete-orphan")