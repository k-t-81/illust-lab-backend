from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TIMESTAMP
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.sql.expression import text

from database.db import Base


class ControlnetIllustrationPostModel(Base):
    __tablename__ = "controlnet_illustration_posts"
    __table_args__ = (UniqueConstraint(
        "controlnet_illustration_image_id",
        "illustration_post_group_id",
        name="unique_controlnet_illustration_posts"
    ),)

    id = Column(Integer, primary_key=True, autoincrement=True)

    controlnet_illustration_image_id = Column(Integer, ForeignKey('controlnet_illustration_images.id'), nullable=False)
    illustration_post_group_id = Column(Integer, ForeignKey('illustration_post_groups.id'), nullable=False)

    created_at = Column(TIMESTAMP, nullable=False, default=current_timestamp())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    controlnet_illustration_image = relationship("ControlnetIllustrationImageModel", back_populates="controlnet_illustration_posts")
    illustration_post_group = relationship("IllustrationPostGroupModel", back_populates="controlnet_illustration_posts")