from typing import Optional

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Img2ImgIllustrationImageModel


# database/models/img2img_illustration_image.pyに対応するpydanticモデル
class Img2ImgIllustrationImageCreate(BaseModel):
    id: int
    seed: int
    image: str
    img2img_illustration_id: int

    class Config:
        orm_mode = True

    @staticmethod
    def empty():
        return Img2ImgIllustrationImageCreate(id=-1, seed=0, image='', img2img_illustration_id=0)

# database/models/img2img_illustration_image.pyを作成するpydanticモデル
class CreateImg2ImgIllustrationImage(BaseModel):
    seed: int
    image: Optional[str] = None
    img2img_illustration_id: int

# database/models/img2img_illustration_image.pyを作成する関数
async def create_img2img_illustration_image(db: AsyncSession, img2img_illustration_image: CreateImg2ImgIllustrationImage) -> Img2ImgIllustrationImageCreate:
    # imageがNoneの場合はseedとimg2img_illustration_idで検索
    if not img2img_illustration_image.image:
        result = await db.execute(select(Img2ImgIllustrationImageModel).filter_by(seed=img2img_illustration_image.seed, img2img_illustration_id=img2img_illustration_image.img2img_illustration_id))
        db_illustration_image = result.scalars().first()
        if db_illustration_image:
            return Img2ImgIllustrationImageCreate.from_orm(db_illustration_image)

        return Img2ImgIllustrationImageCreate.empty()

    # 一致するレコードを取得
    result = await db.execute(select(Img2ImgIllustrationImageModel).filter_by(**img2img_illustration_image.dict()))
    db_illustration_image = result.scalars().first()
    if db_illustration_image:
        return Img2ImgIllustrationImageCreate.from_orm(db_illustration_image)

    db_illustration_image = Img2ImgIllustrationImageModel(**img2img_illustration_image.dict())
    db.add(db_illustration_image)
    await db.flush()

    return Img2ImgIllustrationImageCreate.from_orm(db_illustration_image)