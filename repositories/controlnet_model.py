import datetime

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import ControlnetModelModel

# database/models/controlnet_model.pyを作成するpydanticモデル
class ControlnetModel(BaseModel):
    id: str
    model: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True

    @staticmethod
    def empty():
        return ControlnetModel(
            id="",
            model="",
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
        )

# database/models/controlnet_model.pyを作成するpydanticモデル
class ControlnetModelCreate(BaseModel):
    id: str
    model: str

    class Config:
        orm_mode = True


# database/models/controlnet_model.pyを作成するpydanticモデル
class CreateControlnetModel(BaseModel):
    model: str

# database/models/controlnet_model.pyを削除するpydanticモデル
class DeleteControlnetModel(BaseModel):
    id: str


# database/models/controlnet_model.pyを作成する関数
async def create_controlnet_model(db: AsyncSession, controlnet_model: CreateControlnetModel) -> ControlnetModelCreate:
    # モデルが一致するレコードが存在するか確認する
    result = await db.execute(select(ControlnetModelModel).filter_by(model=controlnet_model.model))
    db_controlnet_model = result.scalars().first()
    if db_controlnet_model:
        return ControlnetModelCreate.from_orm(db_controlnet_model)

    db_controlnet_model = ControlnetModelModel(**controlnet_model.dict())
    db.add(db_controlnet_model)
    await db.flush()

    return ControlnetModelCreate.from_orm(db_controlnet_model)


# database/models/controlnet_model.pyを削除する関数
async def delete_controlnet_model(db: AsyncSession, controlnet_model: DeleteControlnetModel) -> bool:
    # モデルIDが一致するレコードが存在するか確認する
    result = await db.execute(select(ControlnetModelModel).filter_by(**controlnet_model.dict()))
    db_controlnet_model = result.scalars().first()
    # 存在しない場合
    if not db_controlnet_model:
        return False

    await db.delete(db_controlnet_model)
    await db.flush()
    return True