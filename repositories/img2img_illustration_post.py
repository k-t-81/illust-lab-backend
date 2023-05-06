import datetime
from typing import List

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Img2ImgIllustrationPostModel, Img2ImgIllustrationImageModel


# database/models/img2img_illustration_post.pyに対応するpydanticモデル
class Img2ImgIllustrationPostCreate(BaseModel):
    id: int
    img2img_illustration_image_id: int
    illustration_post_group_id: int

    class Config:
        orm_mode = True

# database/models/img2img_illustration_post.pyを作成するpydanticモデル
class CreateImg2ImgIllustrationPost(BaseModel):
    img2img_illustration_image_id: int
    illustration_post_group_id: int

# database/models/img2img_illustration_post.pyに対応するpydanticモデル
class Img2ImgIllustrationPost(Img2ImgIllustrationPostCreate):
    created_at: datetime.datetime
    updated_at: datetime.datetime
    seed: int
    image: str

    @staticmethod
    def empty():
        return Img2ImgIllustrationPost(
            id=-1,
            img2img_illustration_image_id=0,
            illustration_post_group_id=0,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
            seed=0,
            image="",
        )

# database/models/img2img_illustration_post.pyを取得する関数
async def get_img2img_illustration_posts(db: AsyncSession, img2img_illustration_id: int, illustration_post_group_id: int) -> List[Img2ImgIllustrationPost]:
    result = await db.execute(
        select(
            Img2ImgIllustrationPostModel.id,
            Img2ImgIllustrationPostModel.img2img_illustration_image_id,
            Img2ImgIllustrationPostModel.illustration_post_group_id,
            Img2ImgIllustrationPostModel.created_at,
            Img2ImgIllustrationPostModel.updated_at,
            Img2ImgIllustrationImageModel.seed,
            Img2ImgIllustrationImageModel.image,
        ).
        select_from(Img2ImgIllustrationPostModel).
        filter_by(illustration_post_group_id=illustration_post_group_id).
        join(Img2ImgIllustrationImageModel).
        filter_by(img2img_illustration_id=img2img_illustration_id).
        order_by(Img2ImgIllustrationImageModel.seed.desc())
    )
    db_illustration_posts = result.all()

    return [Img2ImgIllustrationPost.from_orm(db_illustration_post) for db_illustration_post in db_illustration_posts]

# database/models/img2img_illustration_post.pyを作成する関数
async def create_img2img_illustration_post(db: AsyncSession, img2img_illustration_post: CreateImg2ImgIllustrationPost) -> Img2ImgIllustrationPostCreate:
    # 一致するレコードを取得
    result = await db.execute(select(Img2ImgIllustrationPostModel).filter_by(**img2img_illustration_post.dict()))
    db_illustration_post = result.scalars().first()
    if db_illustration_post:
        return Img2ImgIllustrationPostCreate.from_orm(db_illustration_post)

    db_illustration_post = Img2ImgIllustrationPostModel(**img2img_illustration_post.dict())
    db.add(db_illustration_post)
    await db.flush()

    return Img2ImgIllustrationPostCreate.from_orm(db_illustration_post)
