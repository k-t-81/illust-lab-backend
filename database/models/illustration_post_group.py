from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TIMESTAMP
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.sql.expression import text

from database.db import Base


class IllustrationPostGroupModel(Base):
    __tablename__ = "illustration_post_groups"

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String(255), nullable=False)

    created_at = Column(TIMESTAMP, nullable=False, default=current_timestamp())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    controlnet_illustration_posts = relationship("ControlnetIllustrationPostModel", back_populates="illustration_post_group", cascade="delete, delete-orphan")
    img2img_illustration_posts = relationship("Img2ImgIllustrationPostModel", back_populates="illustration_post_group", cascade="delete, delete-orphan")
    txt2img_illustration_posts = relationship("Txt2ImgIllustrationPostModel", back_populates="illustration_post_group", cascade="delete, delete-orphan")