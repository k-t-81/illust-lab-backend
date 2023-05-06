import datetime
from typing import List

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import ControlnetIllustrationPostModel, ControlnetIllustrationImageModel

# database/models/controlnet_illustration_post.pyに対応するpydanticモデル
class ControlnetIllustrationPostCreate(BaseModel):
    id: int
    controlnet_illustration_image_id: int
    illustration_post_group_id: int

    class Config:
        orm_mode = True

# database/models/controlnet_illustration_post.pyを作成するpydanticモデル
class CreateControlnetIllustrationPost(BaseModel):
    controlnet_illustration_image_id: int
    illustration_post_group_id: int

# database/models/controlnet_illustration_post.pyに対応するpydanticモデル
class ControlnetIllustrationPost(ControlnetIllustrationPostCreate):
    created_at: datetime.datetime
    updated_at: datetime.datetime
    seed: int
    image: str
    @staticmethod
    def empty():
        return ControlnetIllustrationPost(
            id=-1,
            controlnet_illustration_image_id=0,
            illustration_post_group_id=0,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
            seed=0,
            image="",
        )

# database/models/controlnet_illustration_post.pyを取得する関数
async def get_controlnet_illustration_posts(db: AsyncSession, controlnet_illustration_id: int, illustration_post_group_id: int) -> List[ControlnetIllustrationPost]:
    result = await db.execute(
        select(
            ControlnetIllustrationPostModel.id,
            ControlnetIllustrationPostModel.controlnet_illustration_image_id,
            ControlnetIllustrationPostModel.illustration_post_group_id,
            ControlnetIllustrationPostModel.created_at,
            ControlnetIllustrationPostModel.updated_at,
            ControlnetIllustrationImageModel.seed,
            ControlnetIllustrationImageModel.image,
        ).
        select_from(ControlnetIllustrationPostModel).
        filter_by(illustration_post_group_id=illustration_post_group_id).
        join(ControlnetIllustrationImageModel).
        filter_by(controlnet_illustration_id=controlnet_illustration_id).
        order_by(ControlnetIllustrationImageModel.seed.desc())
    )
    db_illustration_posts = result.all()

    return [ControlnetIllustrationPost.from_orm(db_illustration_post) for db_illustration_post in db_illustration_posts]


# database/models/controlnet_illustration_post.pyを作成する関数
async def create_controlnet_illustration_post(db: AsyncSession, controlnet_illustration_post: CreateControlnetIllustrationPost) -> ControlnetIllustrationPostCreate:
    # 一致するレコードを取得
    result = await db.execute(select(ControlnetIllustrationPostModel).filter_by(**controlnet_illustration_post.dict()))
    db_illustration_post = result.scalars().first()
    if db_illustration_post:
        return ControlnetIllustrationPostCreate.from_orm(db_illustration_post)

    db_illustration_post = ControlnetIllustrationPostModel(**controlnet_illustration_post.dict())
    db.add(db_illustration_post)
    await db.flush()

    return ControlnetIllustrationPostCreate.from_orm(db_illustration_post)
