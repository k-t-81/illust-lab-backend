from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TIMESTAMP
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.sql.expression import text

from database.db import Base


class Img2ImgIllustrationImageModel(Base):
    __tablename__ = "img2img_illustration_images"
    __table_args__ = (UniqueConstraint(
        "seed",
        "img2img_illustration_id",
        name="unique_img2img_illustration_images"
    ),)

    id = Column(Integer, primary_key=True, autoincrement=True)

    seed = Column(Integer, nullable=False)
    image = Column(String(255), nullable=False, unique=True)

    img2img_illustration_id = Column(Integer, ForeignKey('img2img_illustrations.id'), nullable=False)

    created_at = Column(TIMESTAMP, nullable=False, default=current_timestamp())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    img2img_illustration = relationship("Img2ImgIllustrationModel", back_populates="img2img_illustration_images")

    img2img_illustration_posts = relationship("Img2ImgIllustrationPostModel", back_populates="img2img_illustration_image", cascade="delete, delete-orphan")