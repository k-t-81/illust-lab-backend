from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TIMESTAMP
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.sql.expression import text

from database.db import Base


class Img2ImgIllustrationPostModel(Base):
    __tablename__ = "img2img_illustration_posts"
    __table_args__ = (UniqueConstraint(
        "img2img_illustration_image_id",
        "illustration_post_group_id",
        name="unique_img2img_illustration_posts"
    ),)

    id = Column(Integer, primary_key=True, autoincrement=True)

    img2img_illustration_image_id = Column(Integer, ForeignKey('img2img_illustration_images.id'), nullable=False)
    illustration_post_group_id = Column(Integer, ForeignKey('illustration_post_groups.id'), nullable=False)

    created_at = Column(TIMESTAMP, nullable=False, default=current_timestamp())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    img2img_illustration_image = relationship("Img2ImgIllustrationImageModel", back_populates="img2img_illustration_posts")
    illustration_post_group = relationship("IllustrationPostGroupModel", back_populates="img2img_illustration_posts")