import strawberry
from .resolvers.illustration_crud import read_illustrations, read_illustration_groups, read_illustration_group, \
    read_illustrations_count, read_illustration_groups_count, \
    create_illustration_group, update_illustration_group, delete_illustration_group
from .resolvers.illustration_generate import generate_txt2img_illustration, generate_img2img_illustration, generate_controlnet_illustration


@strawberry.type
class Query:
    read_illustrations = strawberry.field(resolver=read_illustrations)
    read_illustrations_count = strawberry.field(resolver=read_illustrations_count)
    read_illustration_groups = strawberry.field(resolver=read_illustration_groups)
    read_illustration_group = strawberry.field(resolver=read_illustration_group)
    read_illustration_groups_count = strawberry.field(resolver=read_illustration_groups_count)


@strawberry.type
class Mutation:
    generate_txt2img_illustration = strawberry.field(resolver=generate_txt2img_illustration)
    generate_img2img_illustration = strawberry.field(resolver=generate_img2img_illustration)
    generate_controlnet_illustration = strawberry.field(resolver=generate_controlnet_illustration)
    create_illustration_group = strawberry.field(resolver=create_illustration_group)
    update_illustration_group = strawberry.field(resolver=update_illustration_group)
    delete_illustration_group = strawberry.field(resolver=delete_illustration_group)


schema = strawberry.Schema(query=Query, mutation=Mutation)
