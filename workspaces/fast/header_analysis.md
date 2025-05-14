# Workflow Header Analysis Report

## Analysis of 29 workflows

Workflows analyzed:
- HelloMeme_image_mono
- HelloMeme_video_mono
- animate_3D_mono
- audio_split_stems_mono
- background_removal_mono
- background_removal_video_mono
- face_styler_mono
- flux_dev_mono
- flux_inpainting_mono
- flux_redux_mono
- frame_interpolation_mono
- frame_interpolation_movie_mono
- img2vid_mono
- layer_diffusion_mono
- mars-id_mono
- ominicontrol_mono
- outpaint_mono
- remix_flux_schnell_mono
- remix_mono
- sd3_txt2img_mono
- stable_audio_mono
- storydiffusion_mono
- texture_flow_mono
- txt2img_mono2
- txt2vid_mono
- upscaler_mono
- vid2vid_sdxl_mono
- video_FX_mono
- video_upscaler_mono

## Individual Field Analysis

### base_model

| Workflow | Value |
|----------|-------|
| HelloMeme_image_mono | hellomeme |
| HelloMeme_video_mono | hellomeme |
| animate_3D_mono | sd15 |
| audio_split_stems_mono | librosa |
| background_removal_mono | inspyrenet-rembg |
| background_removal_video_mono | inspyrenet-rembg |
| face_styler_mono | sdxl |
| flux_dev_mono | flux-dev |
| flux_inpainting_mono | flux-dev |
| flux_redux_mono | flux-dev |
| frame_interpolation_mono | sdxl |
| frame_interpolation_movie_mono | sdxl |
| img2vid_mono | sd15 |
| layer_diffusion_mono | sdxl |
| mars-id_mono | flux-schnell |
| ominicontrol_mono | flux-dev |
| outpaint_mono | sd15 |
| remix_flux_schnell_mono | flux-schnell |
| remix_mono | sdxl |
| sd3_txt2img_mono | sd35 |
| stable_audio_mono | stable-audio-open |
| storydiffusion_mono | sdxl |
| texture_flow_mono | sd15 |
| txt2img_mono2 | sdxl |
| txt2vid_mono | sd15 |
| upscaler_mono | sd15 |
| vid2vid_sdxl_mono | sdxl |
| video_FX_mono | sd15 |
| video_upscaler_mono | sd15 |


### cost_estimate

| Workflow | Value |
|----------|-------|
| HelloMeme_image_mono | 1 |
| HelloMeme_video_mono | 100 |
| animate_3D_mono | n_seconds * 6 * n_steps/6 * resolution/1024 |
| audio_split_stems_mono | 1 |
| background_removal_mono | 1 |
| background_removal_video_mono | 5 |
| face_styler_mono | 1 * n_samples |
| flux_dev_mono | 2 * n_samples |
| flux_inpainting_mono | 3 * n_samples |
| flux_redux_mono | 2.0 * n_samples |
| frame_interpolation_mono | interpolation_frames |
| frame_interpolation_movie_mono | 30 |
| img2vid_mono | 0.5 * num_frames |
| layer_diffusion_mono | 1 * n_samples |
| mars-id_mono | 1.0 * n_samples |
| ominicontrol_mono | 2 * n_samples |
| outpaint_mono | 2 * n_samples |
| remix_flux_schnell_mono | 1.0 * n_samples |
| remix_mono | 1 * n_samples |
| sd3_txt2img_mono | 2 * n_samples |
| stable_audio_mono | (1 + 0.1 * duration) * n_samples |
| storydiffusion_mono | 1 * scene_prompts.length |
| texture_flow_mono | 0.4 * (1 + n_seconds) * (width + height)/(2*640) * (2 + n_steps) * (upscale ? 1.75 : 1) |
| txt2img_mono2 | 1 * n_samples |
| txt2vid_mono | 0.5 * n_frames |
| upscaler_mono | 2 * n_samples |
| vid2vid_sdxl_mono | 1.5 * frame_cap * resolution/896 |
| video_FX_mono | 0.75 * n_seconds * 12 * resolution/1024 |
| video_upscaler_mono | 50 |


### description

| Workflow | Value |
|----------|-------|
| HelloMeme_image_mono | Apply the expression from one face to another |
| HelloMeme_video_mono | Apply the expression from one face to another |
| animate_3D_mono | Creative image animation using 3D-zoom. |
| audio_split_stems_mono | Generate isolated audio stem tracks from a mixed song |
| background_removal_mono | Remove the background from an image, returning a png with transparency. |
| background_removal_video_mono | Remove the background from a video. |
| face_styler_mono | Generate a stylized image featuring a specific person. |
| flux_dev_mono | Generate an image from text using Flux. |
| flux_inpainting_mono | Select and replace anything in an image (FLUX) |
| flux_redux_mono | Blend or Remix Image(s) (using FLUX-redux). |
| frame_interpolation_mono | Create a video from keyframe images through visual interpolation. |
| frame_interpolation_movie_mono | Apply interpolation to add in-between frames to a video, creating a slow motion movie. |
| img2vid_mono | Creative image animation (using AnimateDiff) |
| layer_diffusion_mono | Generate a .png image with alpha channel. |
| mars-id_mono | Create a Student ID. |
| ominicontrol_mono | Take a single example subject image and a prompt to reimagine that subject into a new context. |
| outpaint_mono | Expand an image to a different aspect ratio by outpainting. |
| remix_flux_schnell_mono | Create variations of an image (using FLUX-schnell). |
| remix_mono | Generate variations of a given input image. |
| sd3_txt2img_mono | Generate an image with SD3.5 Large |
| stable_audio_mono | Generate sound effects with Stable Audio. |
| storydiffusion_mono | A multi-prompt to multi-image workflow that uses storydiffusion to generate consistent characters across images without LoRa. |
| texture_flow_mono | Mix multiple images into a video, optionally add a driving motion or shape. |
| txt2img_mono2 | Generate an image from text using the classic SDXL model and trained concepts (LoRAs). |
| txt2vid_mono | Creative, abstract text-driven animations. |
| upscaler_mono | Increase the resolution and detail of an image. |
| vid2vid_sdxl_mono | Apply a new style to an existing video. |
| video_FX_mono | Apply AI effects to regions of a video |
| video_upscaler_mono | Upscales a video to a higher resolution and framerate, improving the quality and details of the video. |


### handler

| Workflow | Value |
|----------|-------|
| HelloMeme_image_mono | comfyui |
| HelloMeme_video_mono | comfyui |
| animate_3D_mono | comfyui |
| audio_split_stems_mono | comfyui |
| background_removal_mono | comfyui |
| background_removal_video_mono | comfyui |
| face_styler_mono | comfyui |
| flux_dev_mono | comfyui |
| flux_inpainting_mono | comfyui |
| flux_redux_mono | comfyui |
| frame_interpolation_mono | comfyui |
| frame_interpolation_movie_mono | comfyui |
| img2vid_mono | comfyui |
| layer_diffusion_mono | comfyui |
| mars-id_mono | comfyui |
| ominicontrol_mono | comfyui |
| outpaint_mono | comfyui |
| remix_flux_schnell_mono | comfyui |
| remix_mono | comfyui |
| sd3_txt2img_mono | comfyui |
| stable_audio_mono | comfyui |
| storydiffusion_mono | comfyui |
| texture_flow_mono | comfyui |
| txt2img_mono2 | comfyui |
| txt2vid_mono | comfyui |
| upscaler_mono | comfyui |
| vid2vid_sdxl_mono | comfyui |
| video_FX_mono | comfyui |
| video_upscaler_mono | comfyui |


### name

| Workflow | Value |
|----------|-------|
| HelloMeme_image_mono | Face Expression Image Transfer (mono) |
| HelloMeme_video_mono | Face Expression Video Transfer (mono) |
| animate_3D_mono | Animate an image with depth (mono) |
| audio_split_stems_mono | Split Audio Stems (mono) |
| background_removal_mono | Remove background (mono) |
| background_removal_video_mono | Remove background (Video) (mono) |
| face_styler_mono | Create a stylized selfie (mono) |
| flux_dev_mono | Create an image (Advanced) (mono) |
| flux_inpainting_mono | Replace part of an image (Inpaint) (mono) |
| flux_redux_mono | Remix Style Blend (mono) |
| frame_interpolation_mono | Keyframe Interpolation (mono) |
| frame_interpolation_movie_mono | Slow Motion Video (mono) |
| img2vid_mono | Animate an image (mono) |
| layer_diffusion_mono | Create an image with transparency (mono) |
| mars-id_mono | ID Generator (mono) |
| ominicontrol_mono | Instant LoRA (mono) |
| outpaint_mono | Extend an image (Outpaint) (mono) |
| remix_flux_schnell_mono | Remix an Image (mono) |
| remix_mono | Remix an image (mono) |
| sd3_txt2img_mono | Create an image (SD3.5) (mono) |
| stable_audio_mono | Create sound effects (mono) |
| storydiffusion_mono | Story Diffusion (mono) |
| texture_flow_mono | TextureFlow (mono) |
| txt2img_mono2 | Create an image (SDXL) (mono) |
| txt2vid_mono | Create a video from text (mono) |
| upscaler_mono | Upscale an image (mono) |
| vid2vid_sdxl_mono | Stylize a video (mono) |
| video_FX_mono | AI video effects (mono) |
| video_upscaler_mono | Upscale a video (mono) |


### output_type

| Workflow | Value |
|----------|-------|
| HelloMeme_image_mono | image |
| HelloMeme_video_mono | video |
| animate_3D_mono | video |
| audio_split_stems_mono | audio |
| background_removal_mono | image |
| background_removal_video_mono | video |
| face_styler_mono | image |
| flux_dev_mono | image |
| flux_inpainting_mono | image |
| flux_redux_mono | image |
| frame_interpolation_mono | video |
| frame_interpolation_movie_mono | video |
| img2vid_mono | video |
| layer_diffusion_mono | image |
| mars-id_mono | image |
| ominicontrol_mono | image |
| outpaint_mono | image |
| remix_flux_schnell_mono | image |
| remix_mono | image |
| sd3_txt2img_mono | image |
| stable_audio_mono | audio |
| storydiffusion_mono | image |
| texture_flow_mono | video |
| txt2img_mono2 | image |
| txt2vid_mono | video |
| upscaler_mono | image |
| vid2vid_sdxl_mono | video |
| video_FX_mono | video |
| video_upscaler_mono | video |


### resolutions

| Workflow | Value |
|----------|-------|
| HelloMeme_image_mono | ❌ Missing |
| HelloMeme_video_mono | ❌ Missing |
| animate_3D_mono | ❌ Missing |
| audio_split_stems_mono | ❌ Missing |
| background_removal_mono | ❌ Missing |
| background_removal_video_mono | ❌ Missing |
| face_styler_mono | - 21-9_1536x640<br>- 16-9_1344x768<br>- 3-2_1216x832<br>- 4-3_1152x896<br>- 1-1_1024x1024<br>- 3-4_896x1152<br>- 2-3_832x1216<br>- 9-16_768x1344<br>- 9-21_640x1536 |
| flux_dev_mono | - 21-9_1536x640<br>- 16-9_1344x768<br>- 3-2_1216x832<br>- 4-3_1152x896<br>- 1-1_1024x1024<br>- 3-4_896x1152<br>- 2-3_832x1216<br>- 9-16_768x1344<br>- 9-21_640x1536 |
| flux_inpainting_mono | ❌ Missing |
| flux_redux_mono | - 21-9_1536x640<br>- 16-9_1344x768<br>- 3-2_1216x832<br>- 4-3_1152x896<br>- 1-1_1024x1024<br>- 3-4_896x1152<br>- 2-3_832x1216<br>- 9x16_1152x2048<br>- 9-21_640x1536 |
| frame_interpolation_mono | ❌ Missing |
| frame_interpolation_movie_mono | ❌ Missing |
| img2vid_mono | [] |
| layer_diffusion_mono | - 16-9_1344x768<br>- 3-2_1216x832<br>- 4-3_1152x896<br>- 1-1_1024x1024<br>- 3-4_896x1152<br>- 2-3_832x1216<br>- 9-16_768x1344 |
| mars-id_mono | [] |
| ominicontrol_mono | ❌ Missing |
| outpaint_mono | ❌ Missing |
| remix_flux_schnell_mono | - 21-9_1536x640<br>- 16-9_1344x768<br>- 3-2_1216x832<br>- 4-3_1152x896<br>- 1-1_1024x1024<br>- 3-4_896x1152<br>- 2-3_832x1216<br>- 9x16_1152x2048<br>- 9-21_640x1536 |
| remix_mono | - 21-9_1536x640<br>- 16-9_1344x768<br>- 3-2_1216x832<br>- 4-3_1152x896<br>- 1-1_1024x1024<br>- 3-4_896x1152<br>- 2-3_832x1216<br>- 9-16_768x1344<br>- 9-21_640x1536 |
| sd3_txt2img_mono | - 21-9_1536x640<br>- 16-9_1344x768<br>- 3-2_1216x832<br>- 4-3_1152x896<br>- 5-4_1088x896<br>- 1-1_1024x1024<br>- 4-5_896x1088<br>- 3-4_896x1152<br>- 2-3_832x1216<br>- 9-16_768x1344<br>- 9-21_640x1536 |
| stable_audio_mono | ❌ Missing |
| storydiffusion_mono | - 21-9_1536x640<br>- 16-9_1344x768<br>- 3-2_1216x832<br>- 4-3_1152x896<br>- 1-1_1024x1024<br>- 3-4_896x1152<br>- 2-3_832x1216<br>- 9-16_768x1344<br>- 9-21_640x1536 |
| texture_flow_mono | - 16-9_1024x576<br>- 3-2_864x576<br>- 1-1_640x640<br>- 2-3_576x864<br>- 9-16_576x1024 |
| txt2img_mono2 | - 21-9_1536x640<br>- 16-9_1344x768<br>- 3-2_1216x832<br>- 4-3_1152x896<br>- 5-4_1088x896<br>- 1-1_1024x1024<br>- 4-5_896x1088<br>- 3-4_896x1152<br>- 2-3_832x1216<br>- 9-16_768x1344<br>- 9-21_640x1536 |
| txt2vid_mono | - 16-9_2048x1152<br>- 3-2_1782x1024<br>- 1-1_1024x1024<br>- 2-3_1024x1782<br>- 9-16_1152x2048 |
| upscaler_mono | ❌ Missing |
| vid2vid_sdxl_mono | ❌ Missing |
| video_FX_mono | ❌ Missing |
| video_upscaler_mono | ❌ Missing |


### status

| Workflow | Value |
|----------|-------|
| HelloMeme_image_mono | stage |
| HelloMeme_video_mono | stage |
| animate_3D_mono | prod |
| audio_split_stems_mono | stage |
| background_removal_mono | prod |
| background_removal_video_mono | inactive |
| face_styler_mono | prod |
| flux_dev_mono | prod |
| flux_inpainting_mono | prod |
| flux_redux_mono | prod |
| frame_interpolation_mono | prod |
| frame_interpolation_movie_mono | prod |
| img2vid_mono | inactive |
| layer_diffusion_mono | prod |
| mars-id_mono | prod |
| ominicontrol_mono | prod |
| outpaint_mono | prod |
| remix_flux_schnell_mono | prod |
| remix_mono | inactive |
| sd3_txt2img_mono | prod |
| stable_audio_mono | prod |
| storydiffusion_mono | inactive |
| texture_flow_mono | prod |
| txt2img_mono2 | prod |
| txt2vid_mono | prod |
| upscaler_mono | prod |
| vid2vid_sdxl_mono | prod |
| video_FX_mono | prod |
| video_upscaler_mono | stage |


### thumbnail

| Workflow | Value |
|----------|-------|
| HelloMeme_image_mono | app/face-expression-transfer-image-opt.mp4 |
| HelloMeme_video_mono | app/HelloMeme.mp4 |
| animate_3D_mono | app/animate_3D_opt.mp4 |
| audio_split_stems_mono | app/audio_separate_stems.png |
| background_removal_mono | app/background_removal_opt.mp4 |
| background_removal_video_mono | app/video-rem-bg-opt.mp4 |
| face_styler_mono | app/face_styler.mp4 |
| flux_dev_mono | app/flux.png |
| flux_inpainting_mono | app/flux-inpaint-opt.mp4 |
| flux_redux_mono | app/flux-redux_opt.mp4 |
| frame_interpolation_mono | app/frame_interpolation_opt.mp4 |
| frame_interpolation_movie_mono | app/slow-motion-video.mp4 |
| img2vid_mono | app/img2vid_opt.mp4 |
| layer_diffusion_mono | app/layer_diffusion.png |
| mars-id_mono | app/mars-id_opt.jpg |
| ominicontrol_mono | app/instant_lora.jpg |
| outpaint_mono | app/outpaint_edit_opt.mp4 |
| remix_flux_schnell_mono | app/remix-flux-schnell_opt.png |
| remix_mono | app/remix-opt.png |
| sd3_txt2img_mono | ❌ Missing |
| stable_audio_mono | app/audio_craft_opt.mp4 |
| storydiffusion_mono | ❌ Missing |
| texture_flow_mono | app/style_mixing_opt.mp4 |
| txt2img_mono2 | app/txt2img.png |
| txt2vid_mono | app/txt2vid_lora_opt.mp4 |
| upscaler_mono | app/upscale_beta_opt.mp4 |
| vid2vid_sdxl_mono | app/vid2vid_sdxl_opt.mp4 |
| video_FX_mono | app/video_FX_thumbnail.mp4 |
| video_upscaler_mono | app/video-upscale-v2-opt.mp4 |


### tip

| Workflow | Value |
|----------|-------|
| HelloMeme_image_mono | Use this endpoint to transfer the facial expression and emotion from an input image to a target image. The model used is HelloMeme, which will limit all outputs to 512x512 square results. The task will fail if a valid face isn't recognized in both inputs. Optimal input images have a clear face occupying at least 30 percent of the image. |
| HelloMeme_video_mono | Use this endpoint to transfer the facial expression and emotion from an input image to a target image. The model used is HelloMeme, which will limit all outputs to 512x512 square results. The task will fail if a valid face isn't recognized in both inputs. |
| animate_3D_mono | Creative image animation using AnimateDiff. This should only be used for creating subtly animated versions of artworks with very minimal motion and is not suited for creating stories or prompt driven motion (if a user requests specific motion, always use the runway tool which takes an input prompt).<br>With default settings this tool will a subtle 3D-zoom effect to an input image, adding some motion to the background, minimal motion to the foreground (subject) and optionally apply a style effect.<br>If the image has a detail sensitive or very specific foreground subject (like a human face or character), a lower foreground_denoise strength can be used to avoid corrupting the small details. This tool is pretty slow and typically used to create minimally animated versions of beautiful still art. |
| audio_split_stems_mono | This tool takes a fully mixed audio track and splits it into isolated vocal, drums, bass, other tracks and an instrumental track without vocals. This is useful for removing vocals from a track, isolating vocals, or getting individual elements for further processing, mixing etc. |
| background_removal_mono | Background removal can do a great job of isolating a foreground subject, returns a .png image with an alpha channel where the background is removed. This tool is a good choice for isolating a subject from an image, and is often used in conjunction with other tools to generate images with a clean background. Keep in mind that a non-technical user may not have the vocabulary to describe what they want, and interpret their request with your best judgement as to whether or not the background removal is what they are requesting, considering terms like alpha, transparency, or other requests for an image with no background as a suggestion to consider this tool when provided with such a request and an image to operate on. |
| background_removal_video_mono | Background removal can do a great job of isolating a foreground subject, returns a .png sequence video with an alpha channel where the background is removed. This tool is a good choice for isolating a subject from an movie, and is often used in conjunction with other tools to generate images with a clean background. Keep in mind that a non-technical user may not have the vocabulary to describe what they want, and interpret their request with your best judgement as to whether or not the background removal is what they are requesting, considering terms like alpha, transparency, or other requests for an video with no background as a suggestion to consider this tool when provided with such a request and a movie to operate on. |
| face_styler_mono | This pipeline takes an input picture of a person to extract their identity and a style image to extract stylistic elements / textures. It then generates an image of the same person in the referenced style.<br>This tool also takes an optional input prompt. By setting the style strength to zero and writing a good prompt, this pipeline can also be used to place the person in a specific situation without applying the style from the image, just using a prompt!<br>If a users asks something like eg "cartoonize this person", you can simply generate a cartoon image first (if not provided) and then use that as the style_image in combination with the user provided person_image. |
| flux_dev_mono | Flux is a text to image model by Black Forest Labs (ex StabilityAI employees ) that excels at prompt coherence, aesthetics and text generation. This tool is a strong choice for generating an image from text! Flux-dev can use ControlNet guidance to maintain the contours or shape outlines of the input image while generating a new style or aesthetic on top of it, and LoRA models to apply a pretrained fine tuned concept. While controlnet exists for this tool, the controlnet models released so far are considered inferior to those from SDXL, and the other tools should be preferred for shape guidance creations. Flux-dev was trained on a dataset ranging in size from .1 to 2 megapixels, and is capable of generating images at higher resolutions than Stable Diffusion without noticable artifacting. While best practice seems to dictate that Flux likes similar resolutions to Stable Diffusion (such as those in the resolutions: list), it is capable of good results higher resolutions, rounded to 64 pixels such as 1920x1088, 1408x1408, 1728x1152, 1664x1216 etc. |
| flux_inpainting_mono | This workflow edits a specific region in the given image by first applying the masking prompt to highlight a specific region of the image, and then applying the inpainting prompt to fill (re-draw) in the highlighted region. Use this tool when a user requests changes to a specific object or region in an image. |
| flux_redux_mono | Flux is a text to image model that excels at prompt coherence and text generation. The flux redux model uses clipvision to create a conditioning from an input image, creating image remix variations or a blend between multiple style images. This tool should be the default for a high quality remix of an image, or a to blende between two images with some degree of promptability. |
| frame_interpolation_mono | This workflow creates animations from a set of images that linearly connect those images into a visual, morphing video. The number of frames between each keyframe can be adjusted to create a smooth transition. The video can be looped back to the first frame to create a seamless loop. This tool should be considered when a user supplies two or more still images and requests a blend, interpolation, morph or similar effect between them. |
| frame_interpolation_movie_mono | This workflow creates a slow motion movie, by adding interpolation frames to the input video with RIFE or FILM models. It is best used to slow down and smooth the resulting creations from other video tools, resulting in an output movie that is 2, 3 or 4 times slower then the original input video. |
| img2vid_mono | This will create an abstract animation based on the content of a single content image. The resulting animation can drift away quite a bit from the source image but sometimes produces creative outputs, ideal for abstract visuals, not ideal for realistic / narrative scenes.<br>This animation tool is also not very promptable so the animation is rather undirected (hit or miss). If specific object / character motion or narrative directions are requested, use the RunWay tool instead. |
| layer_diffusion_mono | The background removal tool is the default way to produce transparency (chained after any img generation tool). However, in rare cases a fully opaque masked object may not be enough. Layer Diffusion generates transparency directly, returning a .png image with gradient alpha values per pixel which means it can generate partially transparent surfaces like glass that can then be placed on top of other images. Use this tool if a user needs a transparent image layer that is to be further composited with other images or backgrounds. In all other cases, use the background removal tool in combination with the image generation tools to produce transparency. |
| mars-id_mono | This is a tool for students of Mars College to create a Student ID card. This tool does not generate the portrait image, it requires a user supplied image to populate a generative form filled ID card template. If a user wants an image of a character or to use a LoRA or ipadapter for their portrait image, create that first with another tool and use that output as the portrait image input required by this tool. |
| ominicontrol_mono | This is a form of instant, single image lora. This means you can provide one example of a subject (perfect for toys, characters, objects and logo's) and then copy-paste that thing into a new context. A common example is placing a logo on a tshirt or coffee mug, or prompting a character or toy into a new environment. It uses the FLUX model behind the scenes and often requires a few tries with different seeds to get a good result. This tool only produces square 1024x1024 images, so for other aspect ratios you need to chain this with an outpainting tool call. This is kinda of like an instant (no-training) lora tool from a single image. |
| outpaint_mono | This model uses SD1.5, so huge resolution changes will add potentially undesirable artifacting. Choosing an SDXL resolution will result in a larger image, but not necessarily a better one. Keep in mind that a non-technical user may not have the vocabulary to describe what they want, and interpret their request with your best judgement as to whether or not the outpainting is what they are requesting, considering terms like outpaint, zoom out,expand, add to the side of this image,or other prompts for an image canvas to be larger as a suggestion to consider this tool when provided with such a request and an image to operate on. |
| remix_flux_schnell_mono | Flux is a text to image model that excels at prompt coherence and text generation. The remix endpoint creates a variation on a starting image using Flux Schnell. This is achieved by captioning the input image with Florence2, and running an img2img job through flux-schnell. This tools should be considered if a user asks for a variation on an existing image. |
| remix_mono | Use this tool to create a variation of a given image. |
| sd3_txt2img_mono | This model uses SD3.5 Large, which is a more powerful and detailed model than SD3.5 Base. It is capable of generating more detailed and intricate images, but also requires more computational resources to run. The outputs are comparable to those of FLUX, but often more creative and weird. SD3 models are good at text generation, and when compared to FLUX, better at style adherance, NSFW, and has a good knowledge of celebrities and artists. Stable Diffusion 3+ models are trained on a dataset of images approximately 1 megapixel in size, and the provided resolutions list is the set of legal resolutions for this model, and should always be used unless a user requests a specific resolution. If an aspect ratio is specifically requested, always aim for dimensions that total approximately 1 megapixel and round to numbers that are divisible by 8. |
| stable_audio_mono | This tool uses the Stable Audio Open model, which is optimized for generating short audio samples, sound effects, and production elements. Ideal for loops and stems rather than full audio arrangements. Makes good drum beats, instrument riffs, ambient sounds, foley recordings, and other audio samples. The model was trained on data from Freesound and the Free Music Archive, respecting creator rights, and natively supports clip lengths of up to 47 seconds of audio. |
| storydiffusion_mono | This is an advanced tool and should only be used when specifically requested. If the user underspecifies how the characters should look, fill in some details for them, but stay true to their vision of the character. |
| texture_flow_mono | This workflow creates smooth, trippy, artistic, or morphing animations from a set of style (texture) images (and other optional inputs). Very good for VJing.<br>One to six images form the basis of this tool, driving the texture and content of the final animation. <br>In general, the video length should be scaled proportionally with the number of style images, 3s of animation per style image is a good default.<br>The motion mapping template controls how the content of the style images is mapped onto the video (spatially).<br>When doing quick experimentation with settings you can set upscale:false to produce a fast but low resolution test render, once a sweet spot is found, <br>you can set upscale:true to generate a full HD final output video. Before using this tool, always print the settings your about to use and ask the user to confirm before executing the tool!<br>There is an optional control_input (set use_controlnet1 to true) and preprocessor1 type that can add specific shape/motion guidance to the generated video <br>like embedding the contours of a logo or word into the video or eg applying the lines or perceived depth of a projection surface when doing videomapping.<br>In general, running TextureFlow without a control_input almost always produces visually appealing results, adding a control_input is tricky.<br>The wrong combination of control_input and style images may look bad (especially when the control strength is too high),<br>but the right combo can look absolutely amazing and is one of Edens special endpoints that make our platform unique!<br><br>Some example use cases for TextureFlow:<br>- abstract, artistic image animation using a single style image <br>(this will completely deform the input image and lose lots of details but its great to generate beautiful, smooth, animated textures)<br>- mixing multiple style_images using various motion mapping modes to create slick, looping VJ content (abstract, artistic animations)<br>- using a logo image as control_input + texture image(s) can create really cool logo animations.<br>- using a simple motion input video or gif (with simple lines / edges / contours) is a great way to drive unique animations (and add new textures with style images)<br>- TextureFlow can even produce animated QR codes by setting the QR code image as control_input and using the \"None\" controlnet mode (which corresponds to a luminance controlnet).<br><br>Make sure to set the controlnet_strength1 high enough to make the QR code animation scanable." |
| txt2img_mono2 | Only use this tool for image generation if you are specifically asked to use Stable Diffusion (SDXL) or to use a Lora with SDXL as its base model. Otherwise you should always prefer one of the Flux models for image generation. Although lower quality, SDXL can produce artistic results with more unusual characteristics. |
| txt2vid_mono | Use this to make videos from text prompts. It's better to use this instead of lerp because it doesn't use AnimateDiff. |
| upscaler_mono | Upscale and add new detail to an initial image. This tool can be considered a "creative upscaler", and at high creativity strengths can hallucinate details that are not present in the original image. |
| vid2vid_sdxl_mono | This will create a new video with similar shapes / motions as the input video but a different texture corresponding to the style image input. It can be used to create stylistic re-interpretations of input videos. Only use this tool if asked to restyle an existing video with a style image. |
| video_FX_mono | This tool allows you to add creative AI effects to regions of a video. You can use this to apply cool post-effects on parts of existing videos, eg adding animated textures to a flat background, replacing bright objects (the sun, lights, etc) with motion graphics, but cannot be used to replace objects in a video. It can be tricky to achieve good results in the first go, tweaking of the settings is often required! |
| video_upscaler_mono | This will create a new video thats very similar to the input video but with higher quality. It takes a long time to run. |


### visible

| Workflow | Value |
|----------|-------|
| HelloMeme_image_mono | False |
| HelloMeme_video_mono | False |
| animate_3D_mono | ❌ Missing |
| audio_split_stems_mono | ❌ Missing |
| background_removal_mono | ❌ Missing |
| background_removal_video_mono | False |
| face_styler_mono | ❌ Missing |
| flux_dev_mono | True |
| flux_inpainting_mono | ❌ Missing |
| flux_redux_mono | True |
| frame_interpolation_mono | ❌ Missing |
| frame_interpolation_movie_mono | True |
| img2vid_mono | False |
| layer_diffusion_mono | ❌ Missing |
| mars-id_mono | ❌ Missing |
| ominicontrol_mono | ❌ Missing |
| outpaint_mono | ❌ Missing |
| remix_flux_schnell_mono | ❌ Missing |
| remix_mono | ❌ Missing |
| sd3_txt2img_mono | False |
| stable_audio_mono | ❌ Missing |
| storydiffusion_mono | False |
| texture_flow_mono | ❌ Missing |
| txt2img_mono2 | ❌ Missing |
| txt2vid_mono | ❌ Missing |
| upscaler_mono | ❌ Missing |
| vid2vid_sdxl_mono | ❌ Missing |
| video_FX_mono | ❌ Missing |
| video_upscaler_mono | False |


### Complete Field Analysis

| Workflow | base_model | cost_estimate | description | handler | name | output_type | resolutions | status | thumbnail | tip | visible |
|---|---|---|---|---|---|---|---|---|---|---|---|
| HelloMeme_image_mono | hellomeme | 1 | Apply the expression from one face to another | comfyui | Face Expression Image Transfer (mono) | image | ❌ | stage | app/face-expression-transfer-image-opt.mp4 | Use this endpoint to transfer the facial expression and emotion from an input image to a target image. The model used is HelloMeme, which will limit all outputs to 512x512 square results. The task will fail if a valid face isn't recognized in both inputs. Optimal input images have a clear face occupying at least 30 percent of the image. | False |
| HelloMeme_video_mono | hellomeme | 100 | Apply the expression from one face to another | comfyui | Face Expression Video Transfer (mono) | video | ❌ | stage | app/HelloMeme.mp4 | Use this endpoint to transfer the facial expression and emotion from an input image to a target image. The model used is HelloMeme, which will limit all outputs to 512x512 square results. The task will fail if a valid face isn't recognized in both inputs. | False |
| animate_3D_mono | sd15 | n_seconds * 6 * n_steps/6 * resolution/1024 | Creative image animation using 3D-zoom. | comfyui | Animate an image with depth (mono) | video | ❌ | prod | app/animate_3D_opt.mp4 | Creative image animation using AnimateDiff. This should only be used for creating subtly animated versions of artworks with very minimal motion and is not suited for creating stories or prompt driven motion (if a user requests specific motion, always use the runway tool which takes an input prompt).
With default settings this tool will a subtle 3D-zoom effect to an input image, adding some motion to the background, minimal motion to the foreground (subject) and optionally apply a style effect.
If the image has a detail sensitive or very specific foreground subject (like a human face or character), a lower foreground_denoise strength can be used to avoid corrupting the small details. This tool is pretty slow and typically used to create minimally animated versions of beautiful still art. | ❌ |
| audio_split_stems_mono | librosa | 1 | Generate isolated audio stem tracks from a mixed song | comfyui | Split Audio Stems (mono) | audio | ❌ | stage | app/audio_separate_stems.png | This tool takes a fully mixed audio track and splits it into isolated vocal, drums, bass, other tracks and an instrumental track without vocals. This is useful for removing vocals from a track, isolating vocals, or getting individual elements for further processing, mixing etc. | ❌ |
| background_removal_mono | inspyrenet-rembg | 1 | Remove the background from an image, returning a png with transparency. | comfyui | Remove background (mono) | image | ❌ | prod | app/background_removal_opt.mp4 | Background removal can do a great job of isolating a foreground subject, returns a .png image with an alpha channel where the background is removed. This tool is a good choice for isolating a subject from an image, and is often used in conjunction with other tools to generate images with a clean background. Keep in mind that a non-technical user may not have the vocabulary to describe what they want, and interpret their request with your best judgement as to whether or not the background removal is what they are requesting, considering terms like alpha, transparency, or other requests for an image with no background as a suggestion to consider this tool when provided with such a request and an image to operate on. | ❌ |
| background_removal_video_mono | inspyrenet-rembg | 5 | Remove the background from a video. | comfyui | Remove background (Video) (mono) | video | ❌ | inactive | app/video-rem-bg-opt.mp4 | Background removal can do a great job of isolating a foreground subject, returns a .png sequence video with an alpha channel where the background is removed. This tool is a good choice for isolating a subject from an movie, and is often used in conjunction with other tools to generate images with a clean background. Keep in mind that a non-technical user may not have the vocabulary to describe what they want, and interpret their request with your best judgement as to whether or not the background removal is what they are requesting, considering terms like alpha, transparency, or other requests for an video with no background as a suggestion to consider this tool when provided with such a request and a movie to operate on. | False |
| face_styler_mono | sdxl | 1 * n_samples | Generate a stylized image featuring a specific person. | comfyui | Create a stylized selfie (mono) | image | ✓ | prod | app/face_styler.mp4 | This pipeline takes an input picture of a person to extract their identity and a style image to extract stylistic elements / textures. It then generates an image of the same person in the referenced style.
This tool also takes an optional input prompt. By setting the style strength to zero and writing a good prompt, this pipeline can also be used to place the person in a specific situation without applying the style from the image, just using a prompt!
If a users asks something like eg "cartoonize this person", you can simply generate a cartoon image first (if not provided) and then use that as the style_image in combination with the user provided person_image. | ❌ |
| flux_dev_mono | flux-dev | 2 * n_samples | Generate an image from text using Flux. | comfyui | Create an image (Advanced) (mono) | image | ✓ | prod | app/flux.png | Flux is a text to image model by Black Forest Labs (ex StabilityAI employees ) that excels at prompt coherence, aesthetics and text generation. This tool is a strong choice for generating an image from text! Flux-dev can use ControlNet guidance to maintain the contours or shape outlines of the input image while generating a new style or aesthetic on top of it, and LoRA models to apply a pretrained fine tuned concept. While controlnet exists for this tool, the controlnet models released so far are considered inferior to those from SDXL, and the other tools should be preferred for shape guidance creations. Flux-dev was trained on a dataset ranging in size from .1 to 2 megapixels, and is capable of generating images at higher resolutions than Stable Diffusion without noticable artifacting. While best practice seems to dictate that Flux likes similar resolutions to Stable Diffusion (such as those in the resolutions: list), it is capable of good results higher resolutions, rounded to 64 pixels such as 1920x1088, 1408x1408, 1728x1152, 1664x1216 etc. | True |
| flux_inpainting_mono | flux-dev | 3 * n_samples | Select and replace anything in an image (FLUX) | comfyui | Replace part of an image (Inpaint) (mono) | image | ❌ | prod | app/flux-inpaint-opt.mp4 | This workflow edits a specific region in the given image by first applying the masking prompt to highlight a specific region of the image, and then applying the inpainting prompt to fill (re-draw) in the highlighted region. Use this tool when a user requests changes to a specific object or region in an image. | ❌ |
| flux_redux_mono | flux-dev | 2.0 * n_samples | Blend or Remix Image(s) (using FLUX-redux). | comfyui | Remix Style Blend (mono) | image | ✓ | prod | app/flux-redux_opt.mp4 | Flux is a text to image model that excels at prompt coherence and text generation. The flux redux model uses clipvision to create a conditioning from an input image, creating image remix variations or a blend between multiple style images. This tool should be the default for a high quality remix of an image, or a to blende between two images with some degree of promptability. | True |
| frame_interpolation_mono | sdxl | interpolation_frames | Create a video from keyframe images through visual interpolation. | comfyui | Keyframe Interpolation (mono) | video | ❌ | prod | app/frame_interpolation_opt.mp4 | This workflow creates animations from a set of images that linearly connect those images into a visual, morphing video. The number of frames between each keyframe can be adjusted to create a smooth transition. The video can be looped back to the first frame to create a seamless loop. This tool should be considered when a user supplies two or more still images and requests a blend, interpolation, morph or similar effect between them. | ❌ |
| frame_interpolation_movie_mono | sdxl | 30 | Apply interpolation to add in-between frames to a video, creating a slow motion movie. | comfyui | Slow Motion Video (mono) | video | ❌ | prod | app/slow-motion-video.mp4 | This workflow creates a slow motion movie, by adding interpolation frames to the input video with RIFE or FILM models. It is best used to slow down and smooth the resulting creations from other video tools, resulting in an output movie that is 2, 3 or 4 times slower then the original input video. | True |
| img2vid_mono | sd15 | 0.5 * num_frames | Creative image animation (using AnimateDiff) | comfyui | Animate an image (mono) | video | ✓ | inactive | app/img2vid_opt.mp4 | This will create an abstract animation based on the content of a single content image. The resulting animation can drift away quite a bit from the source image but sometimes produces creative outputs, ideal for abstract visuals, not ideal for realistic / narrative scenes.
This animation tool is also not very promptable so the animation is rather undirected (hit or miss). If specific object / character motion or narrative directions are requested, use the RunWay tool instead. | False |
| layer_diffusion_mono | sdxl | 1 * n_samples | Generate a .png image with alpha channel. | comfyui | Create an image with transparency (mono) | image | ✓ | prod | app/layer_diffusion.png | The background removal tool is the default way to produce transparency (chained after any img generation tool). However, in rare cases a fully opaque masked object may not be enough. Layer Diffusion generates transparency directly, returning a .png image with gradient alpha values per pixel which means it can generate partially transparent surfaces like glass that can then be placed on top of other images. Use this tool if a user needs a transparent image layer that is to be further composited with other images or backgrounds. In all other cases, use the background removal tool in combination with the image generation tools to produce transparency. | ❌ |
| mars-id_mono | flux-schnell | 1.0 * n_samples | Create a Student ID. | comfyui | ID Generator (mono) | image | ✓ | prod | app/mars-id_opt.jpg | This is a tool for students of Mars College to create a Student ID card. This tool does not generate the portrait image, it requires a user supplied image to populate a generative form filled ID card template. If a user wants an image of a character or to use a LoRA or ipadapter for their portrait image, create that first with another tool and use that output as the portrait image input required by this tool. | ❌ |
| ominicontrol_mono | flux-dev | 2 * n_samples | Take a single example subject image and a prompt to reimagine that subject into a new context. | comfyui | Instant LoRA (mono) | image | ❌ | prod | app/instant_lora.jpg | This is a form of instant, single image lora. This means you can provide one example of a subject (perfect for toys, characters, objects and logo's) and then copy-paste that thing into a new context. A common example is placing a logo on a tshirt or coffee mug, or prompting a character or toy into a new environment. It uses the FLUX model behind the scenes and often requires a few tries with different seeds to get a good result. This tool only produces square 1024x1024 images, so for other aspect ratios you need to chain this with an outpainting tool call. This is kinda of like an instant (no-training) lora tool from a single image. | ❌ |
| outpaint_mono | sd15 | 2 * n_samples | Expand an image to a different aspect ratio by outpainting. | comfyui | Extend an image (Outpaint) (mono) | image | ❌ | prod | app/outpaint_edit_opt.mp4 | This model uses SD1.5, so huge resolution changes will add potentially undesirable artifacting. Choosing an SDXL resolution will result in a larger image, but not necessarily a better one. Keep in mind that a non-technical user may not have the vocabulary to describe what they want, and interpret their request with your best judgement as to whether or not the outpainting is what they are requesting, considering terms like outpaint, zoom out,expand, add to the side of this image,or other prompts for an image canvas to be larger as a suggestion to consider this tool when provided with such a request and an image to operate on. | ❌ |
| remix_flux_schnell_mono | flux-schnell | 1.0 * n_samples | Create variations of an image (using FLUX-schnell). | comfyui | Remix an Image (mono) | image | ✓ | prod | app/remix-flux-schnell_opt.png | Flux is a text to image model that excels at prompt coherence and text generation. The remix endpoint creates a variation on a starting image using Flux Schnell. This is achieved by captioning the input image with Florence2, and running an img2img job through flux-schnell. This tools should be considered if a user asks for a variation on an existing image. | ❌ |
| remix_mono | sdxl | 1 * n_samples | Generate variations of a given input image. | comfyui | Remix an image (mono) | image | ✓ | inactive | app/remix-opt.png | Use this tool to create a variation of a given image. | ❌ |
| sd3_txt2img_mono | sd35 | 2 * n_samples | Generate an image with SD3.5 Large | comfyui | Create an image (SD3.5) (mono) | image | ✓ | prod | ❌ | This model uses SD3.5 Large, which is a more powerful and detailed model than SD3.5 Base. It is capable of generating more detailed and intricate images, but also requires more computational resources to run. The outputs are comparable to those of FLUX, but often more creative and weird. SD3 models are good at text generation, and when compared to FLUX, better at style adherance, NSFW, and has a good knowledge of celebrities and artists. Stable Diffusion 3+ models are trained on a dataset of images approximately 1 megapixel in size, and the provided resolutions list is the set of legal resolutions for this model, and should always be used unless a user requests a specific resolution. If an aspect ratio is specifically requested, always aim for dimensions that total approximately 1 megapixel and round to numbers that are divisible by 8. | False |
| stable_audio_mono | stable-audio-open | (1 + 0.1 * duration) * n_samples | Generate sound effects with Stable Audio. | comfyui | Create sound effects (mono) | audio | ❌ | prod | app/audio_craft_opt.mp4 | This tool uses the Stable Audio Open model, which is optimized for generating short audio samples, sound effects, and production elements. Ideal for loops and stems rather than full audio arrangements. Makes good drum beats, instrument riffs, ambient sounds, foley recordings, and other audio samples. The model was trained on data from Freesound and the Free Music Archive, respecting creator rights, and natively supports clip lengths of up to 47 seconds of audio. | ❌ |
| storydiffusion_mono | sdxl | 1 * scene_prompts.length | A multi-prompt to multi-image workflow that uses storydiffusion to generate consistent characters across images without LoRa. | comfyui | Story Diffusion (mono) | image | ✓ | inactive | ❌ | This is an advanced tool and should only be used when specifically requested. If the user underspecifies how the characters should look, fill in some details for them, but stay true to their vision of the character. | False |
| texture_flow_mono | sd15 | 0.4 * (1 + n_seconds) * (width + height)/(2*640) * (2 + n_steps) * (upscale ? 1.75 : 1) | Mix multiple images into a video, optionally add a driving motion or shape. | comfyui | TextureFlow (mono) | video | ✓ | prod | app/style_mixing_opt.mp4 | This workflow creates smooth, trippy, artistic, or morphing animations from a set of style (texture) images (and other optional inputs). Very good for VJing.
One to six images form the basis of this tool, driving the texture and content of the final animation. 
In general, the video length should be scaled proportionally with the number of style images, 3s of animation per style image is a good default.
The motion mapping template controls how the content of the style images is mapped onto the video (spatially).
When doing quick experimentation with settings you can set upscale:false to produce a fast but low resolution test render, once a sweet spot is found, 
you can set upscale:true to generate a full HD final output video. Before using this tool, always print the settings your about to use and ask the user to confirm before executing the tool!
There is an optional control_input (set use_controlnet1 to true) and preprocessor1 type that can add specific shape/motion guidance to the generated video 
like embedding the contours of a logo or word into the video or eg applying the lines or perceived depth of a projection surface when doing videomapping.
In general, running TextureFlow without a control_input almost always produces visually appealing results, adding a control_input is tricky.
The wrong combination of control_input and style images may look bad (especially when the control strength is too high),
but the right combo can look absolutely amazing and is one of Edens special endpoints that make our platform unique!

Some example use cases for TextureFlow:
- abstract, artistic image animation using a single style image 
(this will completely deform the input image and lose lots of details but its great to generate beautiful, smooth, animated textures)
- mixing multiple style_images using various motion mapping modes to create slick, looping VJ content (abstract, artistic animations)
- using a logo image as control_input + texture image(s) can create really cool logo animations.
- using a simple motion input video or gif (with simple lines / edges / contours) is a great way to drive unique animations (and add new textures with style images)
- TextureFlow can even produce animated QR codes by setting the QR code image as control_input and using the \"None\" controlnet mode (which corresponds to a luminance controlnet).

Make sure to set the controlnet_strength1 high enough to make the QR code animation scanable." | ❌ |
| txt2img_mono2 | sdxl | 1 * n_samples | Generate an image from text using the classic SDXL model and trained concepts (LoRAs). | comfyui | Create an image (SDXL) (mono) | image | ✓ | prod | app/txt2img.png | Only use this tool for image generation if you are specifically asked to use Stable Diffusion (SDXL) or to use a Lora with SDXL as its base model. Otherwise you should always prefer one of the Flux models for image generation. Although lower quality, SDXL can produce artistic results with more unusual characteristics. | ❌ |
| txt2vid_mono | sd15 | 0.5 * n_frames | Creative, abstract text-driven animations. | comfyui | Create a video from text (mono) | video | ✓ | prod | app/txt2vid_lora_opt.mp4 | Use this to make videos from text prompts. It's better to use this instead of lerp because it doesn't use AnimateDiff. | ❌ |
| upscaler_mono | sd15 | 2 * n_samples | Increase the resolution and detail of an image. | comfyui | Upscale an image (mono) | image | ❌ | prod | app/upscale_beta_opt.mp4 | Upscale and add new detail to an initial image. This tool can be considered a "creative upscaler", and at high creativity strengths can hallucinate details that are not present in the original image. | ❌ |
| vid2vid_sdxl_mono | sdxl | 1.5 * frame_cap * resolution/896 | Apply a new style to an existing video. | comfyui | Stylize a video (mono) | video | ❌ | prod | app/vid2vid_sdxl_opt.mp4 | This will create a new video with similar shapes / motions as the input video but a different texture corresponding to the style image input. It can be used to create stylistic re-interpretations of input videos. Only use this tool if asked to restyle an existing video with a style image. | ❌ |
| video_FX_mono | sd15 | 0.75 * n_seconds * 12 * resolution/1024 | Apply AI effects to regions of a video | comfyui | AI video effects (mono) | video | ❌ | prod | app/video_FX_thumbnail.mp4 | This tool allows you to add creative AI effects to regions of a video. You can use this to apply cool post-effects on parts of existing videos, eg adding animated textures to a flat background, replacing bright objects (the sun, lights, etc) with motion graphics, but cannot be used to replace objects in a video. It can be tricky to achieve good results in the first go, tweaking of the settings is often required! | ❌ |
| video_upscaler_mono | sd15 | 50 | Upscales a video to a higher resolution and framerate, improving the quality and details of the video. | comfyui | Upscale a video (mono) | video | ❌ | stage | app/video-upscale-v2-opt.mp4 | This will create a new video thats very similar to the input video but with higher quality. It takes a long time to run. | False |
