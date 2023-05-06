from typing import Optional

import strawberry
from strawberry.scalars import Base64
import services.illustration_generate as illustration_generate_service
import services.illustration_store as illustration_store_service
from database.db import async_session
import repositories.illustration_model as illustration_model_repository
import repositories.illustration_prompt as prompt_repository
import repositories.txt2img_illustration as txt2img_illustration_repository
import repositories.img2img_illustration as img2img_illustration_repository
import repositories.controlnet_illustration as controlnet_illustration_repository
import repositories.txt2img_illustration_image as txt2img_illustration_image_repository
import repositories.img2img_illustration_image as img2img_illustration_image_repository
import repositories.controlnet_illustration_image as controlnet_illustration_image_repository
import repositories.txt2img_illustration_post as txt2img_illustration_post_repository
import repositories.img2img_illustration_post as img2img_illustration_post_repository
import repositories.controlnet_illustration_post as controlnet_illustration_post_repository
import repositories.controlnet_model as controlnet_model_repository


# 画像生成の入力に対応するstrawberry.input
@strawberry.input
class Txt2ImgIllustrationGenerateInput:
    num_inference_steps: int
    guidance_scale: float
    height: int
    width: int
    prompt: str
    negative_prompt: str
    model: str
    seed: int
    group_id: int

# 画像生成の入力に対応するstrawberry.input
@strawberry.input
class Img2ImgIllustrationGenerateInput:
    num_inference_steps: int
    guidance_scale: float
    strength: float
    prompt: str
    negative_prompt: str
    model: str
    seed: int
    group_id: int
    # 親画像はバイナリかS3のパスのどちらかを指定する
    parent_image_binary: Optional[Base64] = None
    parent_image_path: Optional[str] = None

# 画像生成の入力に対応するstrawberry.input
@strawberry.input
class ControlnetIllustrationGenerateInput:
    num_inference_steps: int
    guidance_scale: float
    controlnet_conditioning_scale: float
    prompt: str
    negative_prompt: str
    model: str
    controlnet_model: str
    seed: int
    group_id: int
    # 親画像はバイナリかS3のパスのどちらかを指定する
    parent_image_binary: Optional[Base64] = None
    parent_image_path: Optional[str] = None


# 画像を生成しS3に保存。使ったパラメータをDBに保存。URLを返す。
async def generate_txt2img_illustration(self, input: Txt2ImgIllustrationGenerateInput) -> str:
    async with async_session.begin() as session:
        # イメージモデルを保存
        illustration_model = await illustration_model_repository.create_illustration_model(session, illustration_model_repository.CreateIllustrationModel(
            model=input.model,
        ))
        # プロンプトを保存
        prompt = await prompt_repository.create_illustration_prompt(session, prompt_repository.CreateIllustrationPrompt(
            value=input.prompt,
        ))
        # ネガティブプロンプトを保存
        negative_prompt = await prompt_repository.create_illustration_prompt(
            session,
            prompt_repository.CreateIllustrationPrompt(
                value=input.negative_prompt,
            ))
        # illustrationを保存
        illustration = await txt2img_illustration_repository.create_txt2img_illustration(session, txt2img_illustration_repository.CreateTxt2ImgIllustration(
            num_inference_steps=input.num_inference_steps,
            guidance_scale=input.guidance_scale,
            height=input.height,
            width=input.width,
            illustration_prompt_id=prompt.id,
            illustration_negative_prompt_id=negative_prompt.id,
            illustration_model_id=illustration_model.id,
        ))
        # seedとillustration.idを使って画像を検索
        illustration_image = await txt2img_illustration_image_repository.create_txt2img_illustration_image(session, txt2img_illustration_image_repository.CreateTxt2ImgIllustrationImage(
            seed=input.seed,
            txt2img_illustration_id=illustration.id,
        ))
        # 画像が存在する場合、投稿を保存し、パスを返す
        if illustration_image.id != -1:
            await txt2img_illustration_post_repository.create_txt2img_illustration_post(session, txt2img_illustration_post_repository.CreateTxt2ImgIllustrationPost(
                txt2img_illustration_image_id=illustration_image.id,
                illustration_post_group_id=input.group_id,
            ))

            return illustration_image.image

        # 画像生成APIを呼び出し画像を生成
        image_generated = illustration_generate_service.generate_txt2img_illustration(illustration_generate_service.Txt2ImgIllustrationGenerate(
            seed=input.seed,
            prompt=input.prompt,
            negative_prompt=input.negative_prompt,
            model=input.model,
            num_inference_steps=input.num_inference_steps,
            guidance_scale=input.guidance_scale,
            height=input.height,
            width=input.width,
        ))
        # 生成した画像をS3に保存
        path = illustration_store_service.upload_illustration(illustration_store_service.IllustrationUpload(
            path=f"{input.seed}.png",
            image=image_generated,
        ))
        # 生成した画像のパスを保存
        illustration_image = await txt2img_illustration_image_repository.create_txt2img_illustration_image(session, txt2img_illustration_image_repository.CreateTxt2ImgIllustrationImage(
            seed=input.seed,
            image=path,
            txt2img_illustration_id=illustration.id,
        ))
        await txt2img_illustration_post_repository.create_txt2img_illustration_post(session, txt2img_illustration_post_repository.CreateTxt2ImgIllustrationPost(
            txt2img_illustration_image_id=illustration_image.id,
            illustration_post_group_id=input.group_id,
        ))

    # 生成した画像のURLを返す
    return path


# 画像を生成しS3に保存。使ったパラメータをDBに保存。URLを返す。
async def generate_img2img_illustration(self, input: Img2ImgIllustrationGenerateInput) -> str:
    async with async_session.begin() as session:
        # parent_image_binaryとparent_image_pathが両方ない場合はエラー
        if not input.parent_image_binary and not input.parent_image_path:
            return ""
        # イメージモデルを保存
        illustration_model = await illustration_model_repository.create_illustration_model(session, illustration_model_repository.CreateIllustrationModel(
            model=input.model,
        ))
        # プロンプトを保存
        prompt = await prompt_repository.create_illustration_prompt(session, prompt_repository.CreateIllustrationPrompt(
            value=input.prompt,
        ))
        # ネガティブプロンプトを保存
        negative_prompt = await prompt_repository.create_illustration_prompt(
            session,
            prompt_repository.CreateIllustrationPrompt(
                value=input.negative_prompt,
            ))
        # parent_image_binaryがあればS3に保存
        if input.parent_image_binary:
            input.parent_image_path = illustration_store_service.upload_illustration(illustration_store_service.IllustrationUpload(
                path=f"{input.seed}.png",
                image=input.parent_image_binary,
            ))
        # parent_image_pathがあればS3から画像を取得
        elif input.parent_image_path:
            input.parent_image_binary = illustration_store_service.download_illustration(illustration_store_service.IllustrationDownload(
                path=input.parent_image_path,
            ))
        # illustrationを保存
        illustration = await img2img_illustration_repository.create_img2img_illustration(session, img2img_illustration_repository.CreateImg2ImgIllustration(
            num_inference_steps=input.num_inference_steps,
            guidance_scale=input.guidance_scale,
            strength=input.strength,
            parent_image=input.parent_image_path,
            illustration_prompt_id=prompt.id,
            illustration_negative_prompt_id=negative_prompt.id,
            illustration_model_id=illustration_model.id,
        ))
        # seedとillustration.idを使って画像を検索
        illustration_image = await img2img_illustration_image_repository.create_img2img_illustration_image(session, img2img_illustration_image_repository.CreateImg2ImgIllustrationImage(
            seed=input.seed,
            img2img_illustration_id=illustration.id,
        ))
        # 画像が存在する場合、投稿を保存し、パスを返す
        if illustration_image.id != -1:
            await img2img_illustration_post_repository.create_img2img_illustration_post(session, img2img_illustration_post_repository.CreateImg2ImgIllustrationPost(
                img2img_illustration_image_id=illustration_image.id,
                illustration_post_group_id=input.group_id,
            ))

            return illustration_image.image

        # 画像生成APIを呼び出し画像を生成
        image_generated = illustration_generate_service.generate_img2img_illustration(illustration_generate_service.Img2ImgIllustrationGenerate(
            seed=input.seed,
            prompt=input.prompt,
            negative_prompt=input.negative_prompt,
            model=input.model,
            num_inference_steps=input.num_inference_steps,
            guidance_scale=input.guidance_scale,
            strength=input.strength,
            parent_image_binary=input.parent_image_binary,
        ))
        # 生成した画像をS3に保存
        path = illustration_store_service.upload_illustration(illustration_store_service.IllustrationUpload(
            path=f"{input.seed}.png",
            image=image_generated,
        ))
        # 生成した画像のパスを保存
        illustration_image = await img2img_illustration_image_repository.create_img2img_illustration_image(session, img2img_illustration_image_repository.CreateImg2ImgIllustrationImage(
            seed=input.seed,
            image=path,
            img2img_illustration_id=illustration.id,
        ))
        await img2img_illustration_post_repository.create_img2img_illustration_post(session, img2img_illustration_post_repository.CreateImg2ImgIllustrationPost(
            img2img_illustration_image_id=illustration_image.id,
            illustration_post_group_id=input.group_id,
        ))

    # 生成した画像のURLを返す
    return path

# 画像を生成しS3に保存。使ったパラメータをDBに保存。URLを返す。
async def generate_controlnet_illustration(self, input: ControlnetIllustrationGenerateInput) -> str:
    async with async_session.begin() as session:
        # parent_image_binaryとparent_image_pathが両方ない場合はエラー
        if not input.parent_image_binary and not input.parent_image_path:
            return ""
        # イメージモデルを保存
        illustration_model = await illustration_model_repository.create_illustration_model(session, illustration_model_repository.CreateIllustrationModel(
            model=input.model,
        ))
        controlnet_model = await controlnet_model_repository.create_controlnet_model(session, controlnet_model_repository.CreateControlnetModel(
            model=input.controlnet_model,
        ))
        # プロンプトを保存
        prompt = await prompt_repository.create_illustration_prompt(session, prompt_repository.CreateIllustrationPrompt(
            value=input.prompt,
        ))
        # ネガティブプロンプトを保存
        negative_prompt = await prompt_repository.create_illustration_prompt(
            session,
            prompt_repository.CreateIllustrationPrompt(
                value=input.negative_prompt,
            ))
        # parent_image_binaryがあればS3に保存
        if input.parent_image_binary:
            input.parent_image_path = illustration_store_service.upload_illustration(illustration_store_service.IllustrationUpload(
                path=f"{input.seed}.png",
                image=input.parent_image_binary,
            ))
        # parent_image_pathがあればS3から画像を取得
        elif input.parent_image_path:
            input.parent_image_binary = illustration_store_service.download_illustration(illustration_store_service.IllustrationDownload(
                path=input.parent_image_path,
            ))
        # illustrationを保存
        illustration = await controlnet_illustration_repository.create_controlnet_illustration(session, controlnet_illustration_repository.CreateControlnetIllustration(
            num_inference_steps=input.num_inference_steps,
            guidance_scale=input.guidance_scale,
            controlnet_conditioning_scale=input.controlnet_conditioning_scale,
            parent_image=input.parent_image_path,
            illustration_prompt_id=prompt.id,
            illustration_negative_prompt_id=negative_prompt.id,
            illustration_model_id=illustration_model.id,
            controlnet_model_id=controlnet_model.id,
        ))
        # seedとillustration.idを使って画像を検索
        illustration_image = await controlnet_illustration_image_repository.create_controlnet_illustration_image(session, controlnet_illustration_image_repository.CreateControlnetIllustrationImage(
            seed=input.seed,
            controlnet_illustration_id=illustration.id,
        ))
        # 画像が存在する場合、投稿を保存し、パスを返す
        if illustration_image.id != -1:
            await controlnet_illustration_post_repository.create_controlnet_illustration_post(session, controlnet_illustration_post_repository.CreateControlnetIllustrationPost(
                controlnet_illustration_image_id=illustration_image.id,
                illustration_post_group_id=input.group_id,
            ))

            return illustration_image.image

        # 画像生成APIを呼び出し画像を生成
        image_generated = illustration_generate_service.generate_controlnet_illustration(illustration_generate_service.ControlnetIllustrationGenerate(
            seed=input.seed,
            prompt=input.prompt,
            negative_prompt=input.negative_prompt,
            model=input.model,
            controlnet_model=input.controlnet_model,
            num_inference_steps=input.num_inference_steps,
            guidance_scale=input.guidance_scale,
            controlnet_conditioning_scale=input.controlnet_conditioning_scale,
            parent_image_binary=input.parent_image_binary,
        ))
        # 生成した画像をS3に保存
        path = illustration_store_service.upload_illustration(illustration_store_service.IllustrationUpload(
            path=f"{input.seed}.png",
            image=image_generated,
        ))
        # 生成した画像のパスを保存
        illustration_image = await controlnet_illustration_image_repository.create_controlnet_illustration_image(session, controlnet_illustration_image_repository.CreateControlnetIllustrationImage(
            seed=input.seed,
            image=path,
            controlnet_illustration_id=illustration.id,
        ))
        await controlnet_illustration_post_repository.create_controlnet_illustration_post(session, controlnet_illustration_post_repository.CreateControlnetIllustrationPost(
            controlnet_illustration_image_id=illustration_image.id,
            illustration_post_group_id=input.group_id,
        ))

    # 生成した画像のURLを返す
    return path