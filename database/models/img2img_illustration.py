from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, String
from sqlalchemy.dialects.mysql import TIMESTAMP, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.sql.expression import text

from database.db import Base


class Img2ImgIllustrationModel(Base):
    __tablename__ = "img2img_illustrations"
    __table_args__ = (UniqueConstraint(
        "num_inference_steps",
        "guidance_scale",
        "strength",
        "parent_image",
        "illustration_prompt_id",
        "illustration_negative_prompt_id",
        "illustration_model_id",
        name="unique_img2img_illustrations"
    ),)

    id = Column(Integer, primary_key=True, autoincrement=True)

    num_inference_steps = Column(Integer, nullable=False)
    guidance_scale = Column(DECIMAL(precision=10, scale=4), nullable=False)

    strength = Column(DECIMAL(precision=10, scale=4), nullable=False)
    parent_image =  Column(String(255), nullable=False)

    illustration_prompt_id = Column(Integer, ForeignKey("illustration_prompts.id"), nullable=False)
    illustration_negative_prompt_id = Column(Integer, ForeignKey("illustration_prompts.id"), nullable=False)
    illustration_model_id = Column(Integer, ForeignKey("illustration_models.id"), nullable=False)

    created_at = Column(TIMESTAMP, nullable=False, default=current_timestamp())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    illustration_prompt = relationship("IllustrationPromptModel", back_populates="img2img_illustrations", foreign_keys="Img2ImgIllustrationModel.illustration_prompt_id")
    illustration_negative_prompt = relationship("IllustrationPromptModel", back_populates="negative_img2img_illustrations", foreign_keys="Img2ImgIllustrationModel.illustration_negative_prompt_id")
    illustration_model = relationship("IllustrationModelModel", back_populates="img2img_illustrations")

    img2img_illustration_images = relationship("Img2ImgIllustrationImageModel", back_populates="img2img_illustration", cascade="delete, delete-orphan")