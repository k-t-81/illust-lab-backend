import datetime
import hashlib

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import IllustrationPromptModel

# database/models/illustration_prompt.pyに対応するpydanticモデル
class IllustrationPrompt(BaseModel):
    id: int
    value: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True

    @staticmethod
    def empty():
        return IllustrationPrompt(
            id=0,
            value="",
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
        )


# database/models/illustration_prompt.pyに対応するpydanticモデル
class IllustrationPromptCreate(BaseModel):
    id: int
    value: str

    class Config:
        orm_mode = True


# database/models/illustration_prompt.pyを作成するpydanticモデル
class CreateIllustrationPrompt(BaseModel):
    value: str


# sha256ハッシュ値を生成する関数
def get_hash(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


# database/models/illustration_prompt.pyを作成する関数
async def create_illustration_prompt(db: AsyncSession, illustration_prompt: CreateIllustrationPrompt) -> IllustrationPromptCreate:
    value_hash = get_hash(illustration_prompt.value)
    # ハッシュ値が一致するレコードが存在するか確認する
    result = await db.execute(select(IllustrationPromptModel).filter_by(value_hash=value_hash))
    db_illustration_prompt = result.scalars().first()
    if db_illustration_prompt:
        return IllustrationPromptCreate.from_orm(db_illustration_prompt)

    db_illustration_prompt = IllustrationPromptModel(**illustration_prompt.dict(), value_hash=value_hash)
    db.add(db_illustration_prompt)
    await db.flush()

    return IllustrationPromptCreate.from_orm(db_illustration_prompt)
