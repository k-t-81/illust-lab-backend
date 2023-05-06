import datetime
from typing import List

from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import IllustrationPostGroupModel

# database/models/illustration_post_group.pyを作成する関数の戻り値に対応するpydanticモデル
class IllustrationPostGroupCreate(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


# database/models/illustration_post_group.pyに対応するpydanticモデル
class IllustrationPostGroup(IllustrationPostGroupCreate):
    created_at: datetime.datetime
    updated_at: datetime.datetime

    # 空のIllustrationGroupを返す
    @staticmethod
    def empty():
        return IllustrationPostGroup(
            id=-1,
            name="",
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now()
        )


# database/models/illustration_post_group.pyを作成するpydanticモデル
class CreateIllustrationPostGroup(BaseModel):
    name: str


# database/models/illustration_post_group.pyを更新するpydanticモデル
class UpdateIllustrationPostGroup(BaseModel):
    id: int
    name: str


# database/models/illustration_post_group.pyを取得するpydanticモデル
class GetIllustrationPostGroup(BaseModel):
    id: int

# database/models/illustration_post_group.pyを削除するpydanticモデル
class DeleteIllustrationPostGroup(BaseModel):
    id: int


# database/models/illustration_post_group.pyをすべて取得する関数
async def get_illustration_post_groups(db: AsyncSession, offset: int, limit: int) -> List[IllustrationPostGroup]:
    db_illustration_post_groups = await db.execute(
        select(IllustrationPostGroupModel).order_by(IllustrationPostGroupModel.created_at.desc()).limit(limit).offset(offset))
    db_illustration_post_groups = db_illustration_post_groups.scalars().all()
    return [IllustrationPostGroup.from_orm(db_parameter_group) for db_parameter_group in db_illustration_post_groups]

async def get_illustration_post_group(db: AsyncSession, id: int) -> IllustrationPostGroup:
    db_illustration_post_group = await db.execute(select(IllustrationPostGroupModel).filter_by(id=id))
    db_illustration_post_group = db_illustration_post_group.scalars().first()
    # 存在しない場合
    if not db_illustration_post_group:
        return IllustrationPostGroup.empty()

    return IllustrationPostGroup.from_orm(db_illustration_post_group)


# database/models/illustration_post_group.pyの件数を取得する関数
async def get_illustration_post_groups_count(db: AsyncSession) -> int:
    db_illustration_post_groups_count = await db.execute(select(func.count(IllustrationPostGroupModel.id)))
    db_illustration_post_groups_count = db_illustration_post_groups_count.scalars().first()
    return db_illustration_post_groups_count


# database/models/illustration_post_group.pyを作成する関数
async def create_illustration_post_group(db: AsyncSession, illustration_post_group: CreateIllustrationPostGroup) -> IllustrationPostGroupCreate:
    db_illustration_post_group = IllustrationPostGroupModel(**illustration_post_group.dict())
    db.add(db_illustration_post_group)
    await db.flush()

    return IllustrationPostGroupCreate.from_orm(db_illustration_post_group)


# database/models/illustration_post_group.pyを更新する関数
async def update_illustration_post_group(db: AsyncSession, illustration_post_group: UpdateIllustrationPostGroup) -> IllustrationPostGroup:
    db_illustration_post_group = await db.execute(select(IllustrationPostGroupModel).filter_by(id=illustration_post_group.id))
    db_illustration_post_group = db_illustration_post_group.scalars().first()
    # 存在しない場合
    if not db_illustration_post_group:
        return IllustrationPostGroup.empty()

    db_illustration_post_group.name = illustration_post_group.name
    await db.flush()

    return IllustrationPostGroup.from_orm(db_illustration_post_group)


# database/models/illustration_post_group.pyを削除する関数
async def delete_illustration_post_group(db: AsyncSession, illustration_post_group: DeleteIllustrationPostGroup) -> bool:
    db_illustration_post_group = await db.execute(select(IllustrationPostGroupModel).filter_by(**illustration_post_group.dict()))
    db_illustration_post_group = db_illustration_post_group.scalars().first()
    # 存在しない場合
    if not db_illustration_post_group:
        return False

    await db.delete(db_illustration_post_group)
    await db.flush()

    return True