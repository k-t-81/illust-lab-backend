from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.mysql import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.sql.expression import text

from database.db import Base


class ControlnetIllustrationImageModel(Base):
    __tablename__ = "controlnet_illustration_images"
    __table_args__ = (UniqueConstraint(
        "seed",
        "controlnet_illustration_id",
        name="unique_controlnet_illustration_images"
    ),)

    id = Column(Integer, primary_key=True, autoincrement=True)

    seed = Column(Integer, nullable=False)
    image = Column(String(255), nullable=False, unique=True)

    controlnet_illustration_id = Column(Integer, ForeignKey('controlnet_illustrations.id'), nullable=False)

    created_at = Column(TIMESTAMP, nullable=False, default=current_timestamp())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    controlnet_illustration = relationship("ControlnetIllustrationModel", back_populates="controlnet_illustration_images")

    controlnet_illustration_posts = relationship("ControlnetIllustrationPostModel", back_populates="controlnet_illustration_image", cascade="delete, delete-orphan")