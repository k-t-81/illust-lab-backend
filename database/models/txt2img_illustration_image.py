from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TIMESTAMP
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.sql.expression import text

from database.db import Base


class Txt2ImgIllustrationImageModel(Base):
    __tablename__ = "txt2img_illustration_images"
    __table_args__ = (UniqueConstraint(
        "seed",
        "txt2img_illustration_id",
        name="unique_txt2img_illustration_images"
    ),)

    id = Column(Integer, primary_key=True, autoincrement=True)

    seed = Column(Integer, nullable=False)
    image = Column(String(255), nullable=False, unique=True)

    txt2img_illustration_id = Column(Integer, ForeignKey('txt2img_illustrations.id'), nullable=False)

    created_at = Column(TIMESTAMP, nullable=False, default=current_timestamp())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    txt2img_illustration = relationship("Txt2ImgIllustrationModel", back_populates="txt2img_illustration_images")

    txt2img_illustration_posts = relationship("Txt2ImgIllustrationPostModel", back_populates="txt2img_illustration_image", cascade="delete, delete-orphan")