classDiagram
direction TB
class alembic_version {
   varchar(32) version_num
}
class controlnet_illustration_images {
   int seed
   varchar(255) image
   timestamp created_at
   timestamp updated_at
   int controlnet_illustration_id
   int id
}
class controlnet_illustration_posts {
   timestamp created_at
   timestamp updated_at
   int controlnet_illustration_image_id
   int illustration_post_group_id
   int id
}
class controlnet_illustrations {
   int num_inference_steps
   decimal(10,4) guidance_scale
   decimal(10,4) controlnet_conditioning_scale
   varchar(255) image
   timestamp created_at
   timestamp updated_at
   int illustration_prompt_id
   int illustration_negative_prompt_id
   int illustration_model_id
   int id
}
class illustration_models {
   varchar(255) model
   timestamp created_at
   timestamp updated_at
   int id
}
class illustration_post_groups {
   varchar(255) name
   timestamp created_at
   timestamp updated_at
   int id
}
class illustration_prompts {
   text value
   varchar(64) value_hash
   timestamp created_at
   timestamp updated_at
   int id
}
class img2img_illustration_images {
   int seed
   varchar(255) image
   timestamp created_at
   timestamp updated_at
   int img2img_illustration_id
   int id
}
class img2img_illustration_posts {
   timestamp created_at
   timestamp updated_at
   int img2img_illustration_image_id
   int illustration_post_group_id
   int id
}
class img2img_illustrations {
   int num_inference_steps
   decimal(10,4) guidance_scale
   decimal(10,4) strength
   varchar(255) image
   timestamp created_at
   timestamp updated_at
   int illustration_prompt_id
   int illustration_negative_prompt_id
   int illustration_model_id
   int id
}
class txt2img_illustration_images {
   int seed
   varchar(255) image
   timestamp created_at
   timestamp updated_at
   int txt2img_illustration_id
   int id
}
class txt2img_illustration_posts {
   timestamp created_at
   timestamp updated_at
   int txt2img_illustration_image_id
   int illustration_post_group_id
   int id
}
class txt2img_illustrations {
   int num_inference_steps
   decimal(10,4) guidance_scale
   int height
   int width
   timestamp created_at
   timestamp updated_at
   int illustration_prompt_id
   int illustration_negative_prompt_id
   int illustration_model_id
   int id
}

controlnet_illustration_images  -->  controlnet_illustrations : controlnet_illustration_id:id
controlnet_illustration_posts  -->  controlnet_illustration_images : controlnet_illustration_image_id:id
controlnet_illustration_posts  -->  illustration_post_groups : illustration_post_group_id:id
controlnet_illustrations  -->  illustration_models : illustration_model_id:id
controlnet_illustrations  -->  illustration_prompts : illustration_prompt_id:id
controlnet_illustrations  -->  illustration_prompts : illustration_negative_prompt_id:id
img2img_illustration_images  -->  img2img_illustrations : img2img_illustration_id:id
img2img_illustration_posts  -->  illustration_post_groups : illustration_post_group_id:id
img2img_illustration_posts  -->  img2img_illustration_images : img2img_illustration_image_id:id
img2img_illustrations  -->  illustration_models : illustration_model_id:id
img2img_illustrations  -->  illustration_prompts : illustration_prompt_id:id
img2img_illustrations  -->  illustration_prompts : illustration_negative_prompt_id:id
txt2img_illustration_images  -->  txt2img_illustrations : txt2img_illustration_id:id
txt2img_illustration_posts  -->  illustration_post_groups : illustration_post_group_id:id
txt2img_illustration_posts  -->  txt2img_illustration_images : txt2img_illustration_image_id:id
txt2img_illustrations  -->  illustration_models : illustration_model_id:id
txt2img_illustrations  -->  illustration_prompts : illustration_negative_prompt_id:id
txt2img_illustrations  -->  illustration_prompts : illustration_prompt_id:id
