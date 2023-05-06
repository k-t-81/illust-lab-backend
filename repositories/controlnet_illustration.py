import datetime

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from database.models import ControlnetIllustrationModel
from repositories.controlnet_model import ControlnetModel
from repositories.illustration_model import IllustrationModel
from repositories.illustration_prompt import IllustrationPrompt


# database/models/controlnet_illustration.pyに対応するpydanticモデル
class ControlnetIllustrationCreate(BaseModel):
    id: int
    num_inference_steps: int
    guidance_scale: float
    controlnet_conditioning_scale: float
    parent_image: str
    illustration_prompt_id: int
    illustration_negative_prompt_id: int
    illustration_model_id: int
    controlnet_model_id: int

    class Config:
        orm_mode = True

# database/models/controlnet_illustration.pyを作成するpydanticモデル
class CreateControlnetIllustration(BaseModel):
    num_inference_steps: int
    guidance_scale: float
    controlnet_conditioning_scale: float
    parent_image: str
    illustration_prompt_id: int
    illustration_negative_prompt_id: int
    illustration_model_id: int
    controlnet_model_id: int

# database/models/controlnet_illustration.pyに対応するpydanticモデル
class ControlnetIllustration(ControlnetIllustrationCreate):
    created_at: datetime.datetime
    updated_at: datetime.datetime
    illustration_prompt: IllustrationPrompt
    illustration_negative_prompt: IllustrationPrompt
    illustration_model: IllustrationModel
    controlnet_model: ControlnetModel

    @staticmethod
    def empty():
        return ControlnetIllustration(
            id=-1,
            num_inference_steps=0,
            guidance_scale=0,
            controlnet_conditioning_scale=0,
            parent_image="",
            illustration_prompt_id=0,
            illustration_negative_prompt_id=0,
            illustration_model_id=0,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
            illustration_prompt=IllustrationPrompt.empty(),
            illustration_negative_prompt=IllustrationPrompt.empty(),
            illustration_model=IllustrationModel.empty(),
            controlnet_model=ControlnetModel.empty(),
        )

# database/models/controlnet_illustration.pyを取得する関数
async def get_controlnet_illustration(db: AsyncSession, controlnet_illustration_id: int) -> ControlnetIllustration:
    result = await db.execute(select(ControlnetIllustrationModel).filter_by(id=controlnet_illustration_id).options(
        joinedload(ControlnetIllustrationModel.illustration_prompt),
        joinedload(ControlnetIllustrationModel.illustration_negative_prompt),
        joinedload(ControlnetIllustrationModel.illustration_model),
        joinedload(ControlnetIllustrationModel.controlnet_model),
    ))
    db_illustration = result.scalars().first()
    if not db_illustration:
        return ControlnetIllustration.empty()

    return ControlnetIllustration.from_orm(db_illustration)

# database/models/controlnet_illustration.pyを作成する関数
async def create_controlnet_illustration(db: AsyncSession, controlnet_illustration: CreateControlnetIllustration) -> ControlnetIllustrationCreate:
    # 一致するレコードを取得
    result = await db.execute(select(ControlnetIllustrationModel).filter_by(**controlnet_illustration.dict()))
    db_illustration = result.scalars().first()
    if db_illustration:
        return ControlnetIllustrationCreate.from_orm(db_illustration)

    db_illustration = ControlnetIllustrationModel(**controlnet_illustration.dict())
    db.add(db_illustration)
    await db.flush()

    return ControlnetIllustrationCreate.from_orm(db_illustration)