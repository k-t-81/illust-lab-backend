from typing import List

from pydantic import BaseModel
from sqlalchemy import select, literal_column, union_all, desc, column
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import count

from database.models import ControlnetIllustrationPostModel, ControlnetIllustrationImageModel, Txt2ImgIllustrationImageModel, Img2ImgIllustrationImageModel, Img2ImgIllustrationPostModel, Txt2ImgIllustrationPostModel

class IllustrationId(BaseModel):
    illustration_id: int
    type: str

    class Config:
        orm_mode = True

async def get_illustration_ids(db: AsyncSession, group_id: int, offset: int, limit: int) -> List[IllustrationId]:
    controlnet_query = select(
        literal_column("'controlnet'").label("type"),
        ControlnetIllustrationImageModel.controlnet_illustration_id.label('illustration_id'),
        ControlnetIllustrationPostModel.created_at.label('created_at'),
    ).select_from(
        ControlnetIllustrationPostModel
    ).filter_by(
        illustration_post_group_id=group_id
    ).join(
        ControlnetIllustrationImageModel
    )
    img2img_query = select(
        literal_column("'img2img'").label("type"),
        Img2ImgIllustrationImageModel.img2img_illustration_id.label('illustration_id'),
        Img2ImgIllustrationPostModel.created_at.label('created_at'),
    ).select_from(
        Img2ImgIllustrationPostModel
    ).filter_by(
        illustration_post_group_id=group_id
    ).join(
        Img2ImgIllustrationImageModel
    )
    txt2img_query = select(
        literal_column("'txt2img'").label("type"),
        Txt2ImgIllustrationImageModel.txt2img_illustration_id.label('illustration_id'),
        Txt2ImgIllustrationPostModel.created_at.label('created_at'),
    ).select_from(
        Txt2ImgIllustrationPostModel
    ).filter_by(
        illustration_post_group_id=group_id
    ).join(
        Txt2ImgIllustrationImageModel
    )
    result = await db.execute(
        select(
            column("illustration_id"),
            column("type"),
        )
        .select_from(
            union_all(
                controlnet_query,
                img2img_query,
                txt2img_query
            )
            .order_by(desc("created_at"))
        )
        .distinct()
        .offset(offset)
        .limit(limit)
    )

    db_illustration_ids = result.all()

    return [IllustrationId.from_orm(db_illustration_id) for db_illustration_id in db_illustration_ids]

async def get_illustration_id_count(db: AsyncSession, group_id: int) -> int:
    controlnet_query = select(
        ControlnetIllustrationImageModel.controlnet_illustration_id.label('illustration_id'),
    ).select_from(
        ControlnetIllustrationPostModel
    ).filter_by(
        illustration_post_group_id=group_id
    ).join(
        ControlnetIllustrationImageModel
    ).distinct()
    img2img_query = select(
        Img2ImgIllustrationImageModel.img2img_illustration_id.label('illustration_id'),
    ).select_from(
        Img2ImgIllustrationPostModel
    ).filter_by(
        illustration_post_group_id=group_id
    ).join(
        Img2ImgIllustrationImageModel
    ).distinct()
    txt2img_query = select(
        Txt2ImgIllustrationImageModel.txt2img_illustration_id.label('illustration_id'),
    ).select_from(
        Txt2ImgIllustrationPostModel
    ).filter_by(
        illustration_post_group_id=group_id
    ).join(
        Txt2ImgIllustrationImageModel
    ).distinct()
    result = await db.execute(
        select(
            count()
        ).select_from(
            union_all(
                controlnet_query,
                img2img_query,
                txt2img_query
            )
        )
    )

    db_illustration_id_count = result.scalars().first()

    return db_illustration_id_count