import datetime

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import IllustrationModelModel

# database/models/illustration_model.pyを作成するpydanticモデル
class IllustrationModel(BaseModel):
    id: str
    model: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True

    @staticmethod
    def empty():
        return IllustrationModel(
            id="",
            model="",
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
        )

# database/models/illustration_model.pyを作成するpydanticモデル
class IllustrationModelCreate(BaseModel):
    id: str
    model: str

    class Config:
        orm_mode = True


# database/models/illustration_model.pyを作成するpydanticモデル
class CreateIllustrationModel(BaseModel):
    model: str

# database/models/illustration_model.pyを削除するpydanticモデル
class DeleteIllustrationModel(BaseModel):
    id: str


# database/models/illustration_model.pyを作成する関数
async def create_illustration_model(db: AsyncSession, illustration_model: CreateIllustrationModel) -> IllustrationModelCreate:
    # モデルが一致するレコードが存在するか確認する
    result = await db.execute(select(IllustrationModelModel).filter_by(model=illustration_model.model))
    db_illustration_model = result.scalars().first()
    if db_illustration_model:
        return IllustrationModelCreate.from_orm(db_illustration_model)

    db_illustration_model = IllustrationModelModel(**illustration_model.dict())
    db.add(db_illustration_model)
    await db.flush()

    return IllustrationModelCreate.from_orm(db_illustration_model)


# database/models/illustration_model.pyを削除する関数
async def delete_illustration_model(db: AsyncSession, illustration_model: DeleteIllustrationModel) -> bool:
    # モデルIDが一致するレコードが存在するか確認する
    result = await db.execute(select(IllustrationModelModel).filter_by(**illustration_model.dict()))
    db_illustration_model = result.scalars().first()
    # 存在しない場合
    if not db_illustration_model:
        return False

    await db.delete(db_illustration_model)
    await db.flush()
    return True
