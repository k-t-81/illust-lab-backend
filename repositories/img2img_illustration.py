import datetime

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from database.models import Img2ImgIllustrationModel
from repositories.illustration_model import IllustrationModel
from repositories.illustration_prompt import IllustrationPrompt


# database/models/img2img_illustration.pyに対応するpydanticモデル
class Img2ImgIllustrationCreate(BaseModel):
    id: int
    num_inference_steps: int
    guidance_scale: float
    strength: float
    parent_image: str
    illustration_prompt_id: int
    illustration_negative_prompt_id: int
    illustration_model_id: int

    class Config:
        orm_mode = True



# database/models/img2img_illustration.pyを作成するpydanticモデル
class CreateImg2ImgIllustration(BaseModel):
    num_inference_steps: int
    guidance_scale: float
    strength: float
    parent_image: str
    illustration_prompt_id: int
    illustration_negative_prompt_id: int
    illustration_model_id: int

# database/models/img2img_illustration.pyに対応するpydanticモデル
class Img2ImgIllustration(Img2ImgIllustrationCreate):
    created_at: datetime.datetime
    updated_at: datetime.datetime
    illustration_prompt: IllustrationPrompt
    illustration_negative_prompt: IllustrationPrompt
    illustration_model: IllustrationModel

    @staticmethod
    def empty():
        return Img2ImgIllustration(
            id=-1,
            num_inference_steps=0,
            guidance_scale=0,
            strength=0,
            parent_image="",
            illustration_prompt_id=0,
            illustration_negative_prompt_id=0,
            illustration_model_id=0,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
            illustration_prompt=IllustrationPrompt.empty(),
            illustration_negative_prompt=IllustrationPrompt.empty(),
            illustration_model=IllustrationModel.empty(),
        )


# database/models/img2img_illustration.pyを取得する関数
async def get_img2img_illustration(db: AsyncSession, img2img_illustration_id: int) -> Img2ImgIllustration:
    result = await db.execute(select(Img2ImgIllustrationModel).filter_by(id=img2img_illustration_id).options(
        joinedload(Img2ImgIllustrationModel.illustration_prompt),
        joinedload(Img2ImgIllustrationModel.illustration_negative_prompt),
        joinedload(Img2ImgIllustrationModel.illustration_model),
    ))
    db_illustration = result.scalars().first()
    if not db_illustration:
        return Img2ImgIllustration.empty()

    return Img2ImgIllustration.from_orm(db_illustration)

# database/models/img2img_illustration.pyを作成する関数
async def create_img2img_illustration(db: AsyncSession, img2img_illustration: CreateImg2ImgIllustration) -> Img2ImgIllustrationCreate:
    # 一致するレコードを取得
    result = await db.execute(select(Img2ImgIllustrationModel).filter_by(**img2img_illustration.dict()))
    db_illustration = result.scalars().first()
    if db_illustration:
        return Img2ImgIllustrationCreate.from_orm(db_illustration)

    db_illustration = Img2ImgIllustrationModel(**img2img_illustration.dict())
    db.add(db_illustration)
    await db.flush()

    return Img2ImgIllustrationCreate.from_orm(db_illustration)