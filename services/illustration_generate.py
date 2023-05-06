import base64

import requests
from pydantic import BaseModel


# 画像生成APIにリクエストを送信するためのpydanticモデル
class Txt2ImgIllustrationGenerate(BaseModel):
    seed: int
    prompt: str
    negative_prompt: str
    model: str
    num_inference_steps: int
    guidance_scale: float
    height: int
    width: int

class Img2ImgIllustrationGenerate(BaseModel):
    seed: int
    prompt: str
    negative_prompt: str
    model: str
    num_inference_steps: int
    guidance_scale: float
    strength: float
    parent_image_binary: bytes

class ControlnetIllustrationGenerate(BaseModel):
    seed: int
    prompt: str
    negative_prompt: str
    model: str
    controlnet_model: str
    num_inference_steps: int
    guidance_scale: float
    controlnet_conditioning_scale: float
    parent_image_binary: bytes


# 画像生成APIのエンドポイント
endpoint_url = "http://localhost:8080"


# 画像生成APIにリクエストを送信し、生成された画像をバイト列で返す
def generate_txt2img_illustration(data: Txt2ImgIllustrationGenerate) -> bytes:
    response = requests.post(f"{endpoint_url}/txt2img", json={
        "model": data.model,
        "seed": data.seed,
        "prompt": data.prompt,
        "negative_prompt": data.negative_prompt,
        "height": data.height,
        "width": data.width,
        "num_inference_steps": data.num_inference_steps,
        "guidance_scale": data.guidance_scale,
    })

    if response.status_code == 200:
        return response.content

    raise Exception(response.text)

def generate_img2img_illustration(data: Img2ImgIllustrationGenerate) -> bytes:
    response = requests.post(f"{endpoint_url}/img2img", json={
        "model": data.model,
        "seed": data.seed,
        "prompt": data.prompt,
        "negative_prompt": data.negative_prompt,
        "strength": data.strength,
        "image_bytes_base64": base64.b64encode(data.parent_image_binary).decode("utf-8"),
        "num_inference_steps": data.num_inference_steps,
        "guidance_scale": data.guidance_scale,
    })

    if response.status_code == 200:
        return response.content

    raise Exception(response.text)

def generate_controlnet_illustration(data: ControlnetIllustrationGenerate) -> bytes:
    response = requests.post(f"{endpoint_url}/controlnet", json={
        "model": data.model,
        "controlnet_model": data.controlnet_model,
        "seed": data.seed,
        "prompt": data.prompt,
        "negative_prompt": data.negative_prompt,
        "controlnet_conditioning_scale": data.controlnet_conditioning_scale,
        "image_bytes_base64": base64.b64encode(data.parent_image_binary).decode("utf-8"),
        "num_inference_steps": data.num_inference_steps,
        "guidance_scale": data.guidance_scale,
    })

    if response.status_code == 200:
        return response.content

    raise Exception(response.text)