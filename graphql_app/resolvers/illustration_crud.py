import asyncio
from datetime import datetime
from typing import List, Union

import strawberry

from repositories import illustration_id, illustration_post_group, controlnet_illustration_post, img2img_illustration_post, txt2img_illustration_post, controlnet_illustration, img2img_illustration, txt2img_illustration
from database.db import async_session


@strawberry.type
class IllustrationPrompt:
    id: int
    value: str
    created_at: datetime
    updated_at: datetime

@strawberry.type
class IllustrationModel:
    id: int
    model: str
    created_at: datetime
    updated_at: datetime


@strawberry.type
class ControlnetIllustration:
    id: int
    num_inference_steps: int
    guidance_scale: float
    controlnet_conditioning_scale: float
    parent_image: str
    illustration_prompt_id: int
    illustration_negative_prompt_id: int
    illustration_model_id: int
    created_at: datetime
    updated_at: datetime
    illustration_prompt: IllustrationPrompt
    illustration_negative_prompt: IllustrationPrompt
    illustration_model: IllustrationModel

@strawberry.type
class ControlnetIllustrationPost:
    id: int
    seed: int
    image: str

@strawberry.type
class Img2ImgIllustration:
    id: int
    num_inference_steps: int
    guidance_scale: float
    strength: float
    parent_image: str
    illustration_prompt_id: int
    illustration_negative_prompt_id: int
    illustration_model_id: int
    created_at: datetime
    updated_at: datetime
    illustration_prompt: IllustrationPrompt
    illustration_negative_prompt: IllustrationPrompt
    illustration_model: IllustrationModel

@strawberry.type
class Img2ImgIllustrationPost:
    id: int
    seed: int
    image: str

@strawberry.type
class Txt2ImgIllustration:
    id: int
    num_inference_steps: int
    guidance_scale: float
    height: int
    width: int
    illustration_prompt_id: int
    illustration_negative_prompt_id: int
    illustration_model_id: int
    created_at: datetime
    updated_at: datetime
    illustration_prompt: IllustrationPrompt
    illustration_negative_prompt: IllustrationPrompt
    illustration_model: IllustrationModel

@strawberry.type
class Txt2ImgIllustrationPost:
    id: int
    seed: int
    image: str

@strawberry.type
class ControlnetIllustrationType:
    illustration: ControlnetIllustration
    posts: List[ControlnetIllustrationPost]

@strawberry.type
class Img2ImgIllustrationType:
    illustration: Img2ImgIllustration
    posts: List[Img2ImgIllustrationPost]

@strawberry.type
class Txt2ImgIllustrationType:
    illustration: Txt2ImgIllustration
    posts: List[Txt2ImgIllustrationPost]

# repositories/schemas/parameter_group.pyに対応するstrawberry.type
@strawberry.type
class IllustrationPostGroup:
    id: int
    name: str
    created_at: datetime
    updated_at: datetime

@strawberry.type
class IllustrationPostGroups:
    illustration_post_groups: List[IllustrationPostGroup]
    offset: int
    limit: int

@strawberry.type
class Illustrations:
    illustrations: List[Union[ControlnetIllustrationType, Img2ImgIllustrationType, Txt2ImgIllustrationType]]
    offset: int
    limit: int

# イラストをすべて取得する
async def read_illustrations(self, group_id: int, offset: int) -> Illustrations:
    async with async_session.begin() as session:
        limit = 5
        if offset % limit != 0:
            offset = 0
        sources = await illustration_id.get_illustration_ids(session, group_id, offset, limit)
        async def fetch_illustration(source):
            if source.type == "controlnet":
                illustration = await controlnet_illustration.get_controlnet_illustration(session, source.illustration_id)
                posts = await controlnet_illustration_post.get_controlnet_illustration_posts(session, source.illustration_id, group_id)
                return ControlnetIllustrationType(illustration=illustration, posts=posts)
            elif source.type == "txt2img":
                illustration = await txt2img_illustration.get_txt2img_illustration(session, source.illustration_id)
                posts = await txt2img_illustration_post.get_txt2img_illustration_posts(session, source.illustration_id, group_id)
                return Txt2ImgIllustrationType(illustration=illustration, posts=posts)
            else:
                illustration = await img2img_illustration.get_img2img_illustration(session, source.illustration_id)
                posts = await img2img_illustration_post.get_img2img_illustration_posts(session, source.illustration_id, group_id)
                return Img2ImgIllustrationType(illustration=illustration, posts=posts)

        tasks = [fetch_illustration(source) for source in sources]
        fetched_illustrations = await asyncio.gather(*tasks)

        return Illustrations(illustrations=fetched_illustrations, offset=offset, limit=limit)


# イラストの件数を取得する
async def read_illustrations_count(self, group_id: int) -> int:
    async with async_session.begin() as session:
        return await illustration_id.get_illustration_id_count(session, group_id)

# グループをすべて取得する
async def read_illustration_groups(self, offset: int) -> IllustrationPostGroups:
    async with async_session.begin() as session:
        limit = 10
        if offset % limit != 0:
            offset = 0
        illustration_post_groups = await illustration_post_group.get_illustration_post_groups(session, offset, limit)
        return IllustrationPostGroups(illustration_post_groups=illustration_post_groups, offset=offset, limit=limit)

async def read_illustration_group(self, id: int) -> IllustrationPostGroup:
    async with async_session.begin() as session:
        return await illustration_post_group.get_illustration_post_group(session, id)

# グループの件数を取得する
async def read_illustration_groups_count(self) -> int:
    async with async_session.begin() as session:
        return await illustration_post_group.get_illustration_post_groups_count(session)


# repositories/parameter_group.pyのcreate_parameter_groupに対応するstrawberry.input
@strawberry.input
class CreateIllustrationPostGroupInput:
    name: str


# repositories/schemas/parameter_group.pyのParameterGroupCreateに対応するstrawberry.type
@strawberry.type
class IllustrationPostGroupCreate:
    id: int
    name: str


# repositories/parameter_group.pyのupdate_parameter_groupに対応するstrawberry.input
@strawberry.input
class UpdateIllustrationPostGroupInput:
    id: int
    name: str


# repositories/parameter_group.pyのdelete_parameter_groupに対応するstrawberry.input
@strawberry.input
class DeleteIllustrationPostGroupInput:
    id: int


# グループを作成する
async def create_illustration_group(self, input: CreateIllustrationPostGroupInput) -> IllustrationPostGroupCreate:
    async with async_session.begin() as session:
        return await illustration_post_group.create_illustration_post_group(session, illustration_post_group.CreateIllustrationPostGroup(name=input.name))


# グループを更新する
async def update_illustration_group(self, input: UpdateIllustrationPostGroupInput) -> IllustrationPostGroup:
    async with async_session.begin() as session:
        return await illustration_post_group.update_illustration_post_group(session, illustration_post_group.UpdateIllustrationPostGroup(id=input.id, name=input.name))


# グループを削除する
async def delete_illustration_group(self, input: DeleteIllustrationPostGroupInput) -> bool:
    async with async_session.begin() as session:
        return await illustration_post_group.delete_illustration_post_group(session, illustration_post_group.DeleteIllustrationPostGroup(id=input.id))
