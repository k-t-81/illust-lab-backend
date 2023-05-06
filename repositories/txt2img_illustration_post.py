import datetime
from typing import List

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Txt2ImgIllustrationPostModel, Txt2ImgIllustrationImageModel


# database/models/txt2img_illustration_post.pyに対応するpydanticモデル
class Txt2ImgIllustrationPostCreate(BaseModel):
    id: int
    txt2img_illustration_image_id: int
    illustration_post_group_id: int

    class Config:
        orm_mode = True

# database/models/txt2img_illustration_post.pyを作成するpydanticモデル
class CreateTxt2ImgIllustrationPost(BaseModel):
    txt2img_illustration_image_id: int
    illustration_post_group_id: int

# database/models/txt2img_illustration_post.pyに対応するpydanticモデル
class Txt2ImgIllustrationPost(Txt2ImgIllustrationPostCreate):
    created_at: datetime.datetime
    updated_at: datetime.datetime
    seed: int
    image: str

    @staticmethod
    def empty():
        return Txt2ImgIllustrationPost(
            id=-1,
            txt2img_illustration_image_id=0,
            illustration_post_group_id=0,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
            seed=0,
            image="",
        )

# database/models/txt2img_illustration_post.pyを取得する関数
async def get_txt2img_illustration_posts(db: AsyncSession, txt2img_illustration_id: int, illustration_post_group_id: int) -> List[Txt2ImgIllustrationPost]:
    result = await db.execute(
        select(
            Txt2ImgIllustrationPostModel.id,
            Txt2ImgIllustrationPostModel.txt2img_illustration_image_id,
            Txt2ImgIllustrationPostModel.illustration_post_group_id,
            Txt2ImgIllustrationPostModel.created_at,
            Txt2ImgIllustrationPostModel.updated_at,
            Txt2ImgIllustrationImageModel.seed,
            Txt2ImgIllustrationImageModel.image,
        ).
        select_from(Txt2ImgIllustrationPostModel).
        filter_by(illustration_post_group_id=illustration_post_group_id).
        join(Txt2ImgIllustrationImageModel).
        filter_by(txt2img_illustration_id=txt2img_illustration_id).
        order_by(Txt2ImgIllustrationImageModel.seed.desc())
    )
    db_illustration_posts = result.all()

    return [Txt2ImgIllustrationPost.from_orm(db_illustration_post) for db_illustration_post in db_illustration_posts]

# database/models/txt2img_illustration_post.pyを作成する関数
async def create_txt2img_illustration_post(db: AsyncSession, txt2img_illustration_post: CreateTxt2ImgIllustrationPost) -> Txt2ImgIllustrationPostCreate:
    # 一致するレコードを取得
    result = await db.execute(select(Txt2ImgIllustrationPostModel).filter_by(**txt2img_illustration_post.dict()))
    db_illustration_post = result.scalars().first()
    if db_illustration_post:
        return Txt2ImgIllustrationPostCreate.from_orm(db_illustration_post)

    db_illustration_post = Txt2ImgIllustrationPostModel(**txt2img_illustration_post.dict())
    db.add(db_illustration_post)
    await db.flush()

    return Txt2ImgIllustrationPostCreate.from_orm(db_illustration_post)
