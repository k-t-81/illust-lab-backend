from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, String
from sqlalchemy.dialects.mysql import TIMESTAMP, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.sql.expression import text

from database.db import Base


class ControlnetIllustrationModel(Base):
    __tablename__ = "controlnet_illustrations"
    __table_args__ = (UniqueConstraint(
        "num_inference_steps",
        "guidance_scale",
        "controlnet_conditioning_scale",
        "parent_image",
        "illustration_prompt_id",
        "illustration_negative_prompt_id",
        "illustration_model_id",
        "controlnet_model_id",
        name="unique_controlnet_illustrations"
    ),)

    id = Column(Integer, primary_key=True, autoincrement=True)

    num_inference_steps = Column(Integer, nullable=False)
    guidance_scale = Column(DECIMAL(precision=10, scale=4), nullable=False)

    controlnet_conditioning_scale = Column(DECIMAL(precision=10, scale=4), nullable=False)
    parent_image =  Column(String(255), nullable=False)

    illustration_prompt_id = Column(Integer, ForeignKey("illustration_prompts.id"), nullable=False)
    illustration_negative_prompt_id = Column(Integer, ForeignKey("illustration_prompts.id"), nullable=False)
    illustration_model_id = Column(Integer, ForeignKey("illustration_models.id"), nullable=False)
    controlnet_model_id = Column(Integer, ForeignKey("controlnet_models.id"), nullable=False)

    created_at = Column(TIMESTAMP, nullable=False, default=current_timestamp())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    illustration_prompt = relationship("IllustrationPromptModel", back_populates="controlnet_illustrations", foreign_keys="ControlnetIllustrationModel.illustration_prompt_id")
    illustration_negative_prompt = relationship("IllustrationPromptModel", back_populates="negative_controlnet_illustrations", foreign_keys="ControlnetIllustrationModel.illustration_negative_prompt_id")
    illustration_model = relationship("IllustrationModelModel", back_populates="controlnet_illustrations")
    controlnet_model = relationship("ControlnetModelModel", back_populates="controlnet_illustrations")

    controlnet_illustration_images = relationship("ControlnetIllustrationImageModel", back_populates="controlnet_illustration", cascade="delete, delete-orphan")