from typing import Optional

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import ControlnetIllustrationImageModel


# database/models/controlnet_illustration_image.pyに対応するpydanticモデル
class ControlnetIllustrationImageCreate(BaseModel):
    id: int
    seed: int
    image: str
    controlnet_illustration_id: int

    class Config:
        orm_mode = True

    @staticmethod
    def empty():
        return ControlnetIllustrationImageCreate(id=-1, seed=0, image='', controlnet_illustration_id=0)

# database/models/controlnet_illustration_image.pyを作成するpydanticモデル
class CreateControlnetIllustrationImage(BaseModel):
    seed: int
    image: Optional[str] = None
    controlnet_illustration_id: int

# database/models/controlnet_illustration_image.pyを作成する関数
async def create_controlnet_illustration_image(db: AsyncSession, controlnet_illustration_image: CreateControlnetIllustrationImage) -> ControlnetIllustrationImageCreate:
    # imageがNoneの場合はseedとcontrolnet_illustration_idで検索
    if not controlnet_illustration_image.image:
        result = await db.execute(select(ControlnetIllustrationImageModel).filter_by(seed=controlnet_illustration_image.seed, controlnet_illustration_id=controlnet_illustration_image.controlnet_illustration_id))
        db_illustration_image = result.scalars().first()
        if db_illustration_image:
            return ControlnetIllustrationImageCreate.from_orm(db_illustration_image)

        return ControlnetIllustrationImageCreate.empty()

    # 一致するレコードを取得
    result = await db.execute(select(ControlnetIllustrationImageModel).filter_by(**controlnet_illustration_image.dict()))
    db_illustration_image = result.scalars().first()
    if db_illustration_image:
        return ControlnetIllustrationImageCreate.from_orm(db_illustration_image)

    db_illustration_image = ControlnetIllustrationImageModel(**controlnet_illustration_image.dict())
    db.add(db_illustration_image)
    await db.flush()

    return ControlnetIllustrationImageCreate.from_orm(db_illustration_image)