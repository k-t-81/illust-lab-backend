from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.dialects.mysql import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.sql.expression import text

from database.db import Base


class IllustrationPromptModel(Base):
    __tablename__ = "illustration_prompts"

    id = Column(Integer, primary_key=True, autoincrement=True)

    value = Column(Text, nullable=False)
    value_hash = Column(String(64), nullable=False, unique=True)

    created_at = Column(TIMESTAMP, nullable=False, default=current_timestamp())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    controlnet_illustrations = relationship("ControlnetIllustrationModel", back_populates="illustration_prompt", cascade="delete, delete-orphan", foreign_keys="ControlnetIllustrationModel.illustration_prompt_id")
    negative_controlnet_illustrations = relationship("ControlnetIllustrationModel", back_populates="illustration_negative_prompt", cascade="delete, delete-orphan", foreign_keys="ControlnetIllustrationModel.illustration_negative_prompt_id")
    img2img_illustrations = relationship("Img2ImgIllustrationModel", back_populates="illustration_prompt", cascade="delete, delete-orphan", foreign_keys="Img2ImgIllustrationModel.illustration_prompt_id")
    negative_img2img_illustrations = relationship("Img2ImgIllustrationModel", back_populates="illustration_negative_prompt", cascade="delete, delete-orphan", foreign_keys="Img2ImgIllustrationModel.illustration_negative_prompt_id")
    txt2img_illustrations = relationship("Txt2ImgIllustrationModel", back_populates="illustration_prompt", cascade="delete, delete-orphan", foreign_keys="Txt2ImgIllustrationModel.illustration_prompt_id")
    negative_txt2img_illustrations = relationship("Txt2ImgIllustrationModel", back_populates="illustration_negative_prompt", cascade="delete, delete-orphan", foreign_keys="Txt2ImgIllustrationModel.illustration_negative_prompt_id")