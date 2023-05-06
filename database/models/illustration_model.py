from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.mysql import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.sql.expression import text

from database.db import Base


class IllustrationModelModel(Base):
    __tablename__ = "illustration_models"

    id = Column(Integer, primary_key=True, autoincrement=True)

    model = Column(String(255), nullable=False, unique=True)

    created_at = Column(TIMESTAMP, nullable=False, default=current_timestamp())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    controlnet_illustrations = relationship("ControlnetIllustrationModel", back_populates="illustration_model", cascade="delete, delete-orphan")
    img2img_illustrations = relationship("Img2ImgIllustrationModel", back_populates="illustration_model", cascade="delete, delete-orphan")
    txt2img_illustrations = relationship("Txt2ImgIllustrationModel", back_populates="illustration_model", cascade="delete, delete-orphan")
