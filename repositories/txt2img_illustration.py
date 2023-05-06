import datetime

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from database.models import Txt2ImgIllustrationModel
from repositories.illustration_model import IllustrationModel
from repositories.illustration_prompt import IllustrationPrompt


# database/models/txt2img_illustration.pyに対応するpydanticモデル
class Txt2ImgIllustrationCreate(BaseModel):
    id: int
    num_inference_steps: int
    guidance_scale: float
    height: int
    width: int
    illustration_prompt_id: int
    illustration_negative_prompt_id: int
    illustration_model_id: int

    class Config:
        orm_mode = True

# database/models/txt2img_illustration.pyを作成するpydanticモデル
class CreateTxt2ImgIllustration(BaseModel):
    num_inference_steps: int
    guidance_scale: float
    height: int
    width: int
    illustration_prompt_id: int
    illustration_negative_prompt_id: int
    illustration_model_id: int

# database/models/txt2img_illustration.pyに対応するpydanticモデル
class Txt2ImgIllustration(Txt2ImgIllustrationCreate):
    created_at: datetime.datetime
    updated_at: datetime.datetime
    illustration_prompt: IllustrationPrompt
    illustration_negative_prompt: IllustrationPrompt
    illustration_model: IllustrationModel

    @staticmethod
    def empty():
        return Txt2ImgIllustration(
            id=0,
            num_inference_steps=0,
            guidance_scale=0,
            height=0,
            width=0,
            illustration_prompt_id=0,
            illustration_negative_prompt_id=0,
            illustration_model_id=0,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
            illustration_prompt=IllustrationPrompt.empty(),
            illustration_negative_prompt=IllustrationPrompt.empty(),
            illustration_model=IllustrationModel.empty(),
        )

# database/models/txt2img_illustration.pyを取得する関数
async def get_txt2img_illustration(db: AsyncSession, txt2img_illustration_id: int) -> Txt2ImgIllustration:
    result = await db.execute(select(Txt2ImgIllustrationModel).filter_by(id=txt2img_illustration_id).options(
        joinedload(Txt2ImgIllustrationModel.illustration_prompt),
        joinedload(Txt2ImgIllustrationModel.illustration_negative_prompt),
        joinedload(Txt2ImgIllustrationModel.illustration_model),
    ))
    db_illustration = result.scalars().first()
    if not db_illustration:
        return Txt2ImgIllustration.empty()

    return Txt2ImgIllustration.from_orm(db_illustration)

# database/models/txt2img_illustration.pyを作成する関数
async def create_txt2img_illustration(db: AsyncSession, txt2img_illustration: CreateTxt2ImgIllustration) -> Txt2ImgIllustrationCreate:
    # 一致するレコードを取得
    result = await db.execute(select(Txt2ImgIllustrationModel).filter_by(**txt2img_illustration.dict()))
    db_illustration = result.scalars().first()
    if db_illustration:
        return Txt2ImgIllustrationCreate.from_orm(db_illustration)

    db_illustration = Txt2ImgIllustrationModel(**txt2img_illustration.dict())
    db.add(db_illustration)
    await db.flush()

    return Txt2ImgIllustrationCreate.from_orm(db_illustration)
