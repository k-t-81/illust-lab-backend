from typing import Optional

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Txt2ImgIllustrationImageModel


# database/models/txt2img_illustration_image.pyに対応するpydanticモデル
class Txt2ImgIllustrationImageCreate(BaseModel):
    id: int
    seed: int
    image: str
    txt2img_illustration_id: int

    class Config:
        orm_mode = True

    @staticmethod
    def empty():
        return Txt2ImgIllustrationImageCreate(id=-1, seed=0, image='', txt2img_illustration_id=0)

# database/models/txt2img_illustration_image.pyを作成するpydanticモデル
class CreateTxt2ImgIllustrationImage(BaseModel):
    seed: int
    image: Optional[str] = None
    txt2img_illustration_id: int

# database/models/txt2img_illustration_image.pyを作成する関数
async def create_txt2img_illustration_image(db: AsyncSession, txt2img_illustration_image: CreateTxt2ImgIllustrationImage) -> Txt2ImgIllustrationImageCreate:
    # imageがNoneの場合はseedとtxt2img_illustration_idで検索
    if not txt2img_illustration_image.image:
        result = await db.execute(select(Txt2ImgIllustrationImageModel).filter_by(seed=txt2img_illustration_image.seed, txt2img_illustration_id=txt2img_illustration_image.txt2img_illustration_id))
        db_illustration_image = result.scalars().first()
        if db_illustration_image:
            return Txt2ImgIllustrationImageCreate.from_orm(db_illustration_image)

        return Txt2ImgIllustrationImageCreate.empty()

    result = await db.execute(select(Txt2ImgIllustrationImageModel).filter_by(**txt2img_illustration_image.dict()))
    db_illustration_image = result.scalars().first()
    if db_illustration_image:
        return Txt2ImgIllustrationImageCreate.from_orm(db_illustration_image)

    db_illustration_image = Txt2ImgIllustrationImageModel(**txt2img_illustration_image.dict())
    db.add(db_illustration_image)
    await db.flush()

    return Txt2ImgIllustrationImageCreate.from_orm(db_illustration_image)
