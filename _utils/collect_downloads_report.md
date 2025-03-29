# Downloads Collection Report

## Summary

- Total unique assets: 132
- Total unique workflows: 12

## Assets by Type

### No extension

| Asset | Origin Workflow | Used In | Source |
|-------|----------------|----------|--------|
| `models/LLM/Florence-2-large` | flux | flux | git clone https://huggingface.co/microsoft/Florence-2-large |
| `models/flux/OminiControl` | flux | flux | git clone https://huggingface.co/Yuanshi/OminiControl |

### .1-schnell

| Asset | Origin Workflow | Used In | Source |
|-------|----------------|----------|--------|
| `models/flux/FLUX.1-schnell` | flux | flux | git clone https://huggingface.co/black-forest-labs/FLUX.1-schnell |

### .bin

| Asset | Origin Workflow | Used In | Source |
|-------|----------------|----------|--------|
| `inpaint/PowerPaint-v2-1/pytorch_model.bin` | txt2img | outpaint, txt2img | https://huggingface.co/JunhaoZhuang/PowerPaint-v2-1/resolve/main/PowerPaint_Brushnet/pytorch_model.bin |

### .ckpt

| Asset | Origin Workflow | Used In | Source |
|-------|----------------|----------|--------|
| `models/animatediff_models/AnimateLCM_sd15_t2v.ckpt` | video | video | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/animatediff_models/AnimateLCM_sd15_t2v.ckpt |
| `models/animatediff_models/mm_sd_v15_v2.ckpt` | video | video | https://huggingface.co/guoyww/animatediff/resolve/main/mm_sd_v15_v2.ckpt?download=true |
| `models/animatediff_models/sd15_t2v_beta.ckpt` | video | video | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/animatediff_models/sd15_t2v_beta.ckpt |
| `models/animatediff_models/v3_sd15_mm.ckpt` | video | video | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/animatediff_models/v3_sd15_mm.ckpt |
| `models/checkpoints/nullModel.ckpt` | remix_flux_schnell | remix_flux_schnell | https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/checkpoints/nullModel.ckpt |
| `models/controlnet/adiff_ControlGIF_controlnet.ckpt` | video | video | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/controlnet/adiff_ControlGIF_controlnet.ckpt |
| `models/controlnet/controlnet_checkpoint.ckpt` | video | video | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/controlnet/controlnet_checkpoint.ckpt |
| `models/controlnet/v3_sd15_sparsectrl_rgb.ckpt` | video | video | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/controlnet/v3_sd15_sparsectrl_rgb.ckpt |
| `models/controlnet/v3_sd15_sparsectrl_scribble.ckpt` | video | video | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/controlnet/v3_sd15_sparsectrl_scribble.ckpt |
| `models/loras/v3_sd15_adapter.ckpt` | video | video | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/loras/v3_sd15_adapter.ckpt |

### .jpg

| Asset | Origin Workflow | Used In | Source |
|-------|----------------|----------|--------|
| `input/A_black_image.jpg` | flux | flux, flux_dev, flux_inpainting, img_tools, temple, txt2img, video | https://upload.wikimedia.org/wikipedia/commons/4/49/A_black_image.jpg |
| `input/A_white_image.jpg` | video | video | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/assets/A_white_image.jpg |
| `input/black_dummy.jpg` | flux | flux, flux_redux, temple | https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/assets/black_dummy.jpg |

### .json

| Asset | Origin Workflow | Used In | Source |
|-------|----------------|----------|--------|
| `custom_nodes/ComfyUI-VideoHelperSuite/video_formats/eden-video-faststart.json` | video | video | https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/assets/eden-video-faststart.json |

### .mp4

| Asset | Origin Workflow | Used In | Source |
|-------|----------------|----------|--------|
| `input/a_black_video.mp4` | video | video | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/assets/a_black_video.mp4 |

### .onnx

| Asset | Origin Workflow | Used In | Source |
|-------|----------------|----------|--------|
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/ckpts/yzd-v/DWPose/dw-ll_ucoco_384.onnx` | flux | flux, flux_dev, flux_inpainting, img_tools, temple, txt2img | https://huggingface.co/yzd-v/DWPose/resolve/main/dw-ll_ucoco_384.onnx |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/ckpts/yzd-v/DWPose/yolox_l.onnx` | flux | flux, flux_dev, flux_inpainting, img_tools, temple, txt2img | https://huggingface.co/yzd-v/DWPose/resolve/main/yolox_l.onnx |
| `models/insightface/inswapper_128.onnx` | txt2img | face_styler, txt2img | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/insightface/inswapper_128.onnx |
| `models/insightface/models/antelopev2/1k3d68.onnx` | txt2img | face_styler, txt2img | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/insightface/models/antelopev2/1k3d68.onnx |
| `models/insightface/models/antelopev2/2d106det.onnx` | txt2img | face_styler, txt2img | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/insightface/models/antelopev2/2d106det.onnx |
| `models/insightface/models/antelopev2/genderage.onnx` | txt2img | face_styler, txt2img | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/insightface/models/antelopev2/genderage.onnx |
| `models/insightface/models/antelopev2/glintr100.onnx` | txt2img | face_styler, txt2img | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/insightface/models/antelopev2/glintr100.onnx |
| `models/insightface/models/antelopev2/scrfd_10g_bnkps.onnx` | txt2img | face_styler, txt2img | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/insightface/models/antelopev2/scrfd_10g_bnkps.onnx |

### .png

| Asset | Origin Workflow | Used In | Source |
|-------|----------------|----------|--------|
| `input/barcode.png` | mars_exclusive | mars_exclusive | https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/assets/mars-id-assets/barcode.png |
| `input/frame-grayscale-no-text.png` | mars_exclusive | mars_exclusive | https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/assets/mars-id-assets/frame-grayscale-no-text.png |
| `input/id-portrait-mask.png` | mars_exclusive | mars_exclusive | https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/assets/mars-id-assets/id-portrait-mask.png |
| `input/matte-alpha.png` | mars_exclusive | mars_exclusive | https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/assets/mars-id-assets/matte-alpha.png |
| `input/matte.png` | mars_exclusive | mars_exclusive | https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/assets/mars-id-assets/matte.png |
| `input/planet-alpha.png` | mars_exclusive | mars_exclusive | https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/assets/mars-id-assets/planet-alpha.png |
| `input/text_fields_bubble.png` | mars_exclusive | mars_exclusive | https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/assets/mars-id-assets/text_fields_bubble.png |

### .pt

| Asset | Origin Workflow | Used In | Source |
|-------|----------------|----------|--------|
| `custom_nodes/ComfyUI-Frame-Interpolation/ckpts/film/film_net_fp32.pt` | batch_tools | batch_tools, frame_interpolation, frame_interpolation_movie | https://github.com/dajes/frame-interpolation-pytorch/releases/download/v1.0.0/film_net_fp32.pt |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/Annotators/dpt_hybrid-midas-501f0c75.pt` | flux | flux, flux_dev, flux_inpainting, img_tools, temple, txt2img | https://huggingface.co/lllyasviel/ControlNet/resolve/main/annotator/ckpts/dpt_hybrid-midas-501f0c75.pt |
| `models/embeddings/NEG_EMBED_STABLE_YOGI_V3.pt` | video | video | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/embeddings/NEG_EMBED_STABLE_YOGI_V3.pt |

### .pth

| Asset | Origin Workflow | Used In | Source |
|-------|----------------|----------|--------|
| `custom_nodes/ComfyUI-Frame-Interpolation/ckpts/rife/rife47.pth` | batch_tools | batch_tools, frame_interpolation, frame_interpolation_movie, mochi_preview, video, video2, video_mochi | https://github.com/styler00dollar/VSGAN-tensorrt-docker/releases/download/models/rife47.pth |
| `custom_nodes/ComfyUI-Frame-Interpolation/ckpts/rife/rife49.pth` | batch_tools | batch_tools, frame_interpolation, frame_interpolation_movie | https://github.com/styler00dollar/VSGAN-tensorrt-docker/releases/download/models/rife49.pth |
| `custom_nodes/comfyui_controlnet_aux/ckpts/TheMistoAI/MistoLine/Anyline/MTEED.pth` | flux | flux, flux_dev, flux_inpainting, img_tools, temple, txt2img | https://huggingface.co/TheMistoAI/MistoLine/resolve/main/Anyline/MTEED.pth |
| `custom_nodes/comfyui_controlnet_aux/ckpts/depth-anything/Depth-Anything-V2-Large/depth_anything_v2_vitl.pth` | img_tools | img_tools, temple, txt2img, video | https://huggingface.co/depth-anything/Depth-Anything-V2-Large/resolve/main/depth_anything_v2_vitl.pth |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/Annotators/ControlNetHED.pth` | flux | flux, flux_dev, flux_inpainting, img_tools, temple, txt2img | https://huggingface.co/lllyasviel/Annotators/resolve/main/ControlNetHED.pth |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/Annotators/body_pose_model.pth` | flux | flux, flux_dev, flux_inpainting, img_tools, temple, txt2img | https://huggingface.co/lllyasviel/ControlNet/resolve/main/annotator/ckpts/body_pose_model.pth |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/Annotators/facenet.pth` | flux | flux, flux_dev, flux_inpainting, img_tools, temple, txt2img | https://huggingface.co/lllyasviel/Annotators/resolve/main/facenet.pth |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/Annotators/hand_pose_model.pth` | flux | flux, flux_dev, flux_inpainting, img_tools, temple, txt2img | https://huggingface.co/lllyasviel/ControlNet/resolve/main/annotator/ckpts/hand_pose_model.pth |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/Annotators/sk_model.pth` | flux | flux, flux_dev, flux_inpainting, img_tools, temple, txt2img | https://huggingface.co/lllyasviel/Annotators/resolve/main/sk_model.pth |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/Annotators/sk_model2.pth` | flux | flux, flux_dev, flux_inpainting, img_tools, temple, txt2img | https://huggingface.co/lllyasviel/Annotators/resolve/main/sk_model2.pth |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/Annotators/table5_pidinet.pth` | img_tools | img_tools, temple, txt2img | https://huggingface.co/TencentARC/T2I-Adapter/resolve/main/third-party-models/table5_pidinet.pth |
| `models/controlnet/control_v11f1p_sd15_depth.pth` | video | video | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/controlnet/control_v11f1p_sd15_depth.pth |
| `models/controlnet/control_v11p_sd15_canny.pth` | video | video | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/controlnet/control_v11p_sd15_canny.pth |
| `models/controlnet/control_v11p_sd15_lineart.pth` | video | video | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/controlnet/control_v11p_sd15_lineart.pth |
| `models/controlnet/control_v11p_sd15_openpose.pth` | video | video | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/controlnet/control_v11p_sd15_openpose.pth |
| `models/controlnet/control_v11p_sd15_scribble.pth` | video | video | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/controlnet/control_v11p_sd15_scribble.pth |
| `models/upscale_models/RealESRGAN_x2plus.pth` | txt2img | mochi_preview, txt2img, video, video2, video_mochi | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/upscale_models/RealESRGAN_x2plus.pth |
| `root/.cache/torch/hub/checkpoints/alexnet-owt-7be5be79.pth` | video | video | https://download.pytorch.org/models/alexnet-owt-7be5be79.pth |

### .safetensors

| Asset | Origin Workflow | Used In | Source |
|-------|----------------|----------|--------|
| `inpaint/PowerPaint-v2-1/diffusion_pytorch_model.safetensors` | txt2img | outpaint, txt2img | https://huggingface.co/JunhaoZhuang/PowerPaint-v2-1/resolve/main/PowerPaint_Brushnet/diffusion_pytorch_model.safetensors |
| `models/animatediff_models/hsxl_temporal_layers.f16.safetensors` | video | video | https://huggingface.co/hotshotco/Hotshot-XL/resolve/main/hsxl_temporal_layers.f16.safetensors |
| `models/checkpoints/Eden_SDXL.safetensors` | img_tools | face_styler, img_tools, layer_diffusion, remix, storydiffusion, temple, txt2img, video | https://edenartlab-lfs.s3.amazonaws.com/models/checkpoints/Eden_SDXL.safetensors |
| `models/checkpoints/SD15/LCM/realismBYSTABLEYOGI_v4LCM.safetensors` | video | video | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/checkpoints/realismBYSTABLEYOGI_v4LCM.safetensors |
| `models/checkpoints/dreamshaperXL_lightningDPMSDE.safetensors` | txt2img | txt2img | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/checkpoints/dreamshaperXL_lightningDPMSDE.safetensors |
| `models/checkpoints/flux1-dev-fp8.safetensors` | flux | flux, flux_dev, flux_inpainting | https://huggingface.co/Comfy-Org/flux1-dev/resolve/main/flux1-dev-fp8.safetensors |
| `models/checkpoints/flux1-schnell-fp8.safetensors` | flux | flux, flux_inpainting, mars_exclusive, remix_flux_schnell | https://huggingface.co/Comfy-Org/flux1-schnell/resolve/main/flux1-schnell-fp8.safetensors |
| `models/checkpoints/juggernautXL_version2.safetensors` | txt2img | txt2img | https://edenartlab-lfs.s3.amazonaws.com/models2/checkpoints/juggernautXL_version2.safetensors |
| `models/checkpoints/juggernautXL_version6Rundiffusion.safetensors` | img_tools | img_tools, temple | https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/checkpoints/juggernautXL_version6Rundiffusion.safetensors |
| `models/checkpoints/juggernaut_reborn-inpainting.safetensors` | video | video | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/checkpoints/juggernaut_reborn-inpainting.safetensors |
| `models/checkpoints/juggernaut_reborn.safetensors` | img_tools | img_tools, outpaint, txt2img, upscaler, video | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/checkpoints/juggernaut_reborn.safetensors |
| `models/checkpoints/juggerxlInpaint_juggerInpaintV8.safetensors` | txt2img | txt2img, video | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/checkpoints/juggerxlInpaint_juggerInpaintV8.safetensors |
| `models/checkpoints/mochi_preview_fp8_scaled3.safetensors` | video2 | video2, video_mochi | https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/checkpoints/mochi_preview_fp8_scaled.safetensors |
| `models/checkpoints/sd3.5_large_fp8_scaled.safetensors` | sd3 | sd3 | https://huggingface.co/Comfy-Org/stable-diffusion-3.5-fp8/resolve/main/sd3.5_large_fp8_scaled.safetensors |
| `models/checkpoints/stable_audio_open_1.0.safetensors` | audio | audio, stable_audio | https://edenartlab-lfs.s3.amazonaws.com/models/stable_audio_open_1.0.safetensors |
| `models/checkpoints/zavychromaxl_v80.safetensors` | video | video | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/checkpoints/zavychromaxl_v80.safetensors |
| `models/clip/clip_l.safetensors` | flux | flux, flux_dev, flux_inpainting, flux_redux, remix_flux_schnell | https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors |
| `models/clip/model.fp16.safetensors` | txt2img | outpaint, txt2img | https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/text_encoder/model.fp16.safetensors |
| `models/clip/t5_base.safetensors` | audio | audio, stable_audio | https://huggingface.co/google-t5/t5-base/resolve/main/model.safetensors |
| `models/clip/t5xxl_fp16.safetensors` | flux | flux, flux_redux | https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/t5xxl_fp16.safetensors |
| `models/clip/t5xxl_fp8_e4m3fn.safetensors` | flux | flux, flux_inpainting, remix_flux_schnell | https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/t5xxl_fp8_e4m3fn.safetensors |
| `models/clip_vision/CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors` | img_tools | face_styler, img_tools, outpaint, remix, temple, txt2img, upscaler, video | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/clip_vision/CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors |
| `models/clip_vision/clip-vit-large-patch14/model.safetensors` | flux | flux, flux_dev, flux_inpainting | https://huggingface.co/openai/clip-vit-large-patch14/resolve/main/model.safetensors |
| `models/clip_vision/sigclip_vision_patch14_384.safetensors` | flux | flux, flux_dev, flux_redux | https://huggingface.co/Comfy-Org/sigclip_vision_384/resolve/main/sigclip_vision_patch14_384.safetensors |
| `models/controlnet/FLUX.1-dev-ControlNet-Union-Pro.safetensors` | flux | flux, flux_dev, flux_inpainting | https://huggingface.co/InstantX/FLUX.1-dev-Controlnet-Union/resolve/main/diffusion_pytorch_model.safetensors |
| `models/controlnet/FLUX.1-dev-Controlnet-Inpainting-Alpha.safetensors.safetensors` | flux | flux, flux_inpainting | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/controlnet/FLUX.1-dev-Controlnet-Inpainting-Alpha.safetensors.safetensors |
| `models/controlnet/SDXL/controlnet-canny-sdxl-1.0/diffusion_pytorch_model_V2.safetensors` | video | video | https://huggingface.co/xinsir/controlnet-canny-sdxl-1.0/resolve/main/diffusion_pytorch_model_V2.safetensors |
| `models/controlnet/SDXL/controlnet-depth-sdxl-1.0/diffusion_pytorch_model.safetensors` | video | video | https://huggingface.co/xinsir/controlnet-depth-sdxl-1.0/resolve/main/diffusion_pytorch_model.safetensors |
| `models/controlnet/control_v11f1e_sd15_tile_fp16.safetensors` | img_tools | img_tools, upscaler | https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11f1e_sd15_tile_fp16.safetensors |
| `models/controlnet/control_v11p_sd15_canny_fp16.safetensors` | video | video | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/controlnet/control_v11p_sd15_canny_fp16.safetensors |
| `models/controlnet/controlnet-canny-sdxl-1.0/diffusion_pytorch_model_V2.safetensors` | img_tools | img_tools, temple, txt2img | https://huggingface.co/xinsir/controlnet-canny-sdxl-1.0/resolve/main/diffusion_pytorch_model_V2.safetensors |
| `models/controlnet/controlnet-depth-sdxl-1.0/diffusion_pytorch_model.safetensors` | img_tools | img_tools, temple, txt2img | https://huggingface.co/xinsir/controlnet-depth-sdxl-1.0/resolve/main/diffusion_pytorch_model.safetensors |
| `models/controlnet/controlnet-openpose-sdxl-1.0/diffusion_pytorch_model.safetensors` | img_tools | img_tools, temple, txt2img | https://huggingface.co/xinsir/controlnet-openpose-sdxl-1.0/resolve/main/diffusion_pytorch_model.safetensors |
| `models/controlnet/controlnet-scribble-sdxl-1.0/diffusion_pytorch_model.safetensors` | img_tools | img_tools, temple, txt2img | https://huggingface.co/xinsir/controlnet-scribble-sdxl-1.0/resolve/main/diffusion_pytorch_model.safetensors |
| `models/controlnet/controlnetQRPatternQR_v2Sd15.safetensors` | video | video | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/controlnet/controlnetQRPatternQR_v2Sd15.safetensors |
| `models/controlnet/diffusers_xl_canny_full.safetensors` | img_tools | img_tools, temple, txt2img | https://huggingface.co/lllyasviel/sd_control_collection/resolve/d1b278d0d1103a3a7c4f7c2c327d236b082a75b1/diffusers_xl_canny_full.safetensors |
| `models/controlnet/t2i-adapter-lineart-sdxl-1.0/diffusion_pytorch_model.safetensors` | img_tools | img_tools, temple, txt2img | https://huggingface.co/TencentARC/t2i-adapter-lineart-sdxl-1.0/resolve/main/diffusion_pytorch_model.safetensors |
| `models/depthanything/depth_anything_v2_vitl_fp16.safetensors` | video | video | https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/depthanything/depth_anything_v2_vitl_fp16.safetensors |
| `models/diffusion_models/mochi_preview_fp8_scaled.safetensors` | mochi_preview | mochi_preview | https://huggingface.co/Comfy-Org/mochi_preview_repackaged/blob/main/all_in_one/mochi_preview_fp8_scaled.safetensors |
| `models/embeddings/EasyNegative.safetensors` | txt2img | outpaint, txt2img | https://huggingface.co/datasets/gsdf/EasyNegative/resolve/main/EasyNegative.safetensors |
| `models/embeddings/froyd7sinsmodel_sdxl_embeddings.safetensors` | temple | temple | https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/assets/temple_abyss/froyd7sinsmodel_sdxl_embeddings.safetensors |
| `models/embeddings/negativeXL_D.safetensors` | img_tools | img_tools, temple, txt2img | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/embeddings/negativeXL_D.safetensors |
| `models/ipadapter/ip-adapter-plus_sd15.safetensors` | img_tools | face_styler, img_tools, outpaint, remix, temple, txt2img, upscaler, video | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/ipadapter/ip-adapter-plus_sd15.safetensors |
| `models/ipadapter/ip-adapter-plus_sdxl_vit-h.safetensors` | img_tools | face_styler, img_tools, outpaint, remix, temple, txt2img, upscaler, video | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/ipadapter/ip-adapter-plus_sdxl_vit-h.safetensors |
| `models/layer_model/layer_xl_transparent_conv.safetensors` | img_tools | img_tools, layer_diffusion | https://huggingface.co/LayerDiffusion/layerdiffusion-v1/resolve/main/layer_xl_transparent_conv.safetensors |
| `models/loras/20241218_1348_banny_best-step00003000.safetensors` | flux | flux | https://storage.googleapis.com/public-assets-xander/Random/remove/flux_loras/20241218_1348_banny_best-step00003000.safetensors |
| `models/loras/20241218_1715_xander-step00003000.safetensors` | flux | flux | https://storage.googleapis.com/public-assets-xander/Random/remove/flux_loras/20241218_1715_xander-step00003000.safetensors |
| `models/loras/Hyper-FLUX.1-dev-16steps-lora.safetensors` | flux | flux, flux_dev, flux_inpainting | https://huggingface.co/ByteDance/Hyper-SD/resolve/main/Hyper-FLUX.1-dev-16steps-lora.safetensors |
| `models/loras/SDXL_lora_xander.safetensors` | img_tools | img_tools, txt2img | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/loras/SDXL_lora_xander.safetensors |
| `models/loras/SDXLrender_v2.0.safetensors` | img_tools | img_tools, upscaler | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/loras/SDXLrender_v2.0.safetensors |
| `models/loras/anime_lora_comfy_converted.safetensors` | flux | flux, flux_dev, flux_inpainting | https://huggingface.co/XLabs-AI/flux-lora-collection/resolve/main/anime_lora_comfy_converted.safetensors |
| `models/loras/art_lora_comfy_converted.safetensors` | flux | flux, flux_dev, flux_inpainting | https://huggingface.co/XLabs-AI/flux-lora-collection/resolve/main/art_lora_comfy_converted.safetensors |
| `models/loras/flux1-canny-dev-lora.safetensors` | flux | flux, flux_dev | https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/checkpoints/flux1-canny-dev-lora.safetensors |
| `models/loras/flux1-depth-dev-lora.safetensors` | flux | flux, flux_dev | https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/checkpoints/flux1-depth-dev-lora.safetensors |
| `models/loras/froyd7sinsmodel_sdxl_lora.safetensors` | temple | temple | https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/assets/temple_abyss/froyd7sinsmodel_sdxl_lora.safetensors |
| `models/loras/mjv6_lora_comfy_converted.safetensors` | flux | flux, flux_dev, flux_inpainting | https://huggingface.co/XLabs-AI/flux-lora-collection/resolve/main/mjv6_lora_comfy_converted.safetensors |
| `models/loras/more_details.safetensors` | img_tools | img_tools, upscaler | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/loras/SDXLrender_v2.0.safetensors |
| `models/loras/realism_lora_comfy_converted.safetensors` | flux | flux, flux_dev, flux_inpainting | https://huggingface.co/XLabs-AI/flux-lora-collection/resolve/main/realism_lora_comfy_converted.safetensors |
| `models/loras/scenery_lora_comfy_converted.safetensors` | flux | flux, flux_dev, flux_inpainting | https://huggingface.co/XLabs-AI/flux-lora-collection/resolve/main/scenery_lora_comfy_converted.safetensors |
| `models/mmaudio/apple_DFN5B-CLIP-ViT-H-14-384_fp16.safetensors` | audio | audio | https://huggingface.co/Kijai/MMAudio_safetensors/resolve/main/apple_DFN5B-CLIP-ViT-H-14-384_fp16.safetensors |
| `models/mmaudio/apple_DFN5B-CLIP-ViT-H-14-384_fp32.safetensors` | audio | audio | https://huggingface.co/Kijai/MMAudio_safetensors/resolve/main/apple_DFN5B-CLIP-ViT-H-14-384_fp32.safetensors |
| `models/mmaudio/mmaudio_large_44k_v2_fp16.safetensors` | audio | audio | https://huggingface.co/Kijai/MMAudio_safetensors/resolve/main/mmaudio_large_44k_v2_fp16.safetensors |
| `models/mmaudio/mmaudio_large_44k_v2_fp32.safetensors` | audio | audio | https://huggingface.co/Kijai/MMAudio_safetensors/resolve/main/mmaudio_large_44k_v2_fp32.safetensors |
| `models/mmaudio/mmaudio_synchformer_fp16.safetensors` | audio | audio | https://huggingface.co/Kijai/MMAudio_safetensors/resolve/main/mmaudio_synchformer_fp16.safetensors |
| `models/mmaudio/mmaudio_synchformer_fp32.safetensors` | audio | audio | https://huggingface.co/Kijai/MMAudio_safetensors/resolve/main/mmaudio_synchformer_fp32.safetensors |
| `models/mmaudio/mmaudio_vae_44k_fp16.safetensors` | audio | audio | https://huggingface.co/Kijai/MMAudio_safetensors/resolve/main/mmaudio_vae_44k_fp16.safetensors |
| `models/mmaudio/mmaudio_vae_44k_fp32.safetensors` | audio | audio | https://huggingface.co/Kijai/MMAudio_safetensors/resolve/main/mmaudio_vae_44k_fp32.safetensors |
| `models/pulid/ip-adapter_pulid_sdxl_fp16.safetensors` | txt2img | face_styler, txt2img | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/pulid/ip-adapter_pulid_sdxl_fp16.safetensors |
| `models/style_models/flux1-redux-dev.safetensors` | flux | flux, flux_dev, flux_redux | https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/checkpoints/flux1-redux-dev.safetensors |
| `models/unet/flux1-dev-fp8.safetensors` | flux | flux, flux_redux | https://huggingface.co/Comfy-Org/flux1-dev/resolve/main/flux1-dev-fp8.safetensors |
| `models/unet/flux1-dev.safetensors` | flux | flux, flux_redux | https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/checkpoints/flux1-dev.safetensors |
| `models/unet/flux1-schnell.safetensors` | flux | flux, flux_inpainting, remix_flux_schnell | https://huggingface.co/black-forest-labs/FLUX.1-schnell/resolve/main/flux1-schnell.safetensors |
| `models/upscale_models/4xNomosUniDAT_otf.safetensors` | img_tools | img_tools, upscaler | https://github.com/Phhofm/models/releases/download/4xNomosUniDAT_otf/4xNomosUniDAT_otf.safetensors |
| `models/vae/ae.safetensors` | flux | flux, flux_inpainting, flux_redux, remix_flux_schnell | https://huggingface.co/black-forest-labs/FLUX.1-schnell/resolve/main/ae.safetensors |
| `models/xlabs/ipadapters/flux-ip-adapter.safetensors` | flux | flux, flux_dev, flux_inpainting | https://huggingface.co/yzd-v/DWPose/resolve/main/yolox_l.onnx |
| `models/xlabs/ipadapters/ip_adapter.safetensors` | flux | flux, flux_dev | https://huggingface.co/XLabs-AI/flux-ip-adapter/resolve/main/ip_adapter.safetensors |

### .ttf

| Asset | Origin Workflow | Used In | Source |
|-------|----------------|----------|--------|
| `custom_nodes/ComfyUI_essentials/fonts/Oswald-Bold.ttf` | mars_exclusive | mars_exclusive | https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/assets/Oswald-Bold.ttf |

## Workflows and their Assets

### audio

| Asset | Is Origin | Source |
|-------|-----------|--------|
| `models/checkpoints/stable_audio_open_1.0.safetensors` | Yes | https://edenartlab-lfs.s3.amazonaws.com/models/stable_audio_open_1.0.safetensors |
| `models/clip/t5_base.safetensors` | Yes | https://huggingface.co/google-t5/t5-base/resolve/main/model.safetensors |
| `models/mmaudio/apple_DFN5B-CLIP-ViT-H-14-384_fp16.safetensors` | Yes | https://huggingface.co/Kijai/MMAudio_safetensors/resolve/main/apple_DFN5B-CLIP-ViT-H-14-384_fp16.safetensors |
| `models/mmaudio/apple_DFN5B-CLIP-ViT-H-14-384_fp32.safetensors` | Yes | https://huggingface.co/Kijai/MMAudio_safetensors/resolve/main/apple_DFN5B-CLIP-ViT-H-14-384_fp32.safetensors |
| `models/mmaudio/mmaudio_large_44k_v2_fp16.safetensors` | Yes | https://huggingface.co/Kijai/MMAudio_safetensors/resolve/main/mmaudio_large_44k_v2_fp16.safetensors |
| `models/mmaudio/mmaudio_large_44k_v2_fp32.safetensors` | Yes | https://huggingface.co/Kijai/MMAudio_safetensors/resolve/main/mmaudio_large_44k_v2_fp32.safetensors |
| `models/mmaudio/mmaudio_synchformer_fp16.safetensors` | Yes | https://huggingface.co/Kijai/MMAudio_safetensors/resolve/main/mmaudio_synchformer_fp16.safetensors |
| `models/mmaudio/mmaudio_synchformer_fp32.safetensors` | Yes | https://huggingface.co/Kijai/MMAudio_safetensors/resolve/main/mmaudio_synchformer_fp32.safetensors |
| `models/mmaudio/mmaudio_vae_44k_fp16.safetensors` | Yes | https://huggingface.co/Kijai/MMAudio_safetensors/resolve/main/mmaudio_vae_44k_fp16.safetensors |
| `models/mmaudio/mmaudio_vae_44k_fp32.safetensors` | Yes | https://huggingface.co/Kijai/MMAudio_safetensors/resolve/main/mmaudio_vae_44k_fp32.safetensors |

### batch_tools

| Asset | Is Origin | Source |
|-------|-----------|--------|
| `custom_nodes/ComfyUI-Frame-Interpolation/ckpts/film/film_net_fp32.pt` | Yes | https://github.com/dajes/frame-interpolation-pytorch/releases/download/v1.0.0/film_net_fp32.pt |
| `custom_nodes/ComfyUI-Frame-Interpolation/ckpts/rife/rife47.pth` | Yes | https://github.com/styler00dollar/VSGAN-tensorrt-docker/releases/download/models/rife47.pth |
| `custom_nodes/ComfyUI-Frame-Interpolation/ckpts/rife/rife49.pth` | Yes | https://github.com/styler00dollar/VSGAN-tensorrt-docker/releases/download/models/rife49.pth |

### flux

| Asset | Is Origin | Source |
|-------|-----------|--------|
| `custom_nodes/comfyui_controlnet_aux/ckpts/TheMistoAI/MistoLine/Anyline/MTEED.pth` | Yes | https://huggingface.co/TheMistoAI/MistoLine/resolve/main/Anyline/MTEED.pth |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/Annotators/ControlNetHED.pth` | Yes | https://huggingface.co/lllyasviel/Annotators/resolve/main/ControlNetHED.pth |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/Annotators/body_pose_model.pth` | Yes | https://huggingface.co/lllyasviel/ControlNet/resolve/main/annotator/ckpts/body_pose_model.pth |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/Annotators/dpt_hybrid-midas-501f0c75.pt` | Yes | https://huggingface.co/lllyasviel/ControlNet/resolve/main/annotator/ckpts/dpt_hybrid-midas-501f0c75.pt |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/Annotators/facenet.pth` | Yes | https://huggingface.co/lllyasviel/Annotators/resolve/main/facenet.pth |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/Annotators/hand_pose_model.pth` | Yes | https://huggingface.co/lllyasviel/ControlNet/resolve/main/annotator/ckpts/hand_pose_model.pth |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/Annotators/sk_model.pth` | Yes | https://huggingface.co/lllyasviel/Annotators/resolve/main/sk_model.pth |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/Annotators/sk_model2.pth` | Yes | https://huggingface.co/lllyasviel/Annotators/resolve/main/sk_model2.pth |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/ckpts/yzd-v/DWPose/dw-ll_ucoco_384.onnx` | Yes | https://huggingface.co/yzd-v/DWPose/resolve/main/dw-ll_ucoco_384.onnx |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/ckpts/yzd-v/DWPose/yolox_l.onnx` | Yes | https://huggingface.co/yzd-v/DWPose/resolve/main/yolox_l.onnx |
| `input/A_black_image.jpg` | Yes | https://upload.wikimedia.org/wikipedia/commons/4/49/A_black_image.jpg |
| `input/black_dummy.jpg` | Yes | https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/assets/black_dummy.jpg |
| `models/LLM/Florence-2-large` | Yes | git clone https://huggingface.co/microsoft/Florence-2-large |
| `models/checkpoints/flux1-dev-fp8.safetensors` | Yes | https://huggingface.co/Comfy-Org/flux1-dev/resolve/main/flux1-dev-fp8.safetensors |
| `models/checkpoints/flux1-schnell-fp8.safetensors` | Yes | https://huggingface.co/Comfy-Org/flux1-schnell/resolve/main/flux1-schnell-fp8.safetensors |
| `models/clip/clip_l.safetensors` | Yes | https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors |
| `models/clip/t5xxl_fp16.safetensors` | Yes | https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/t5xxl_fp16.safetensors |
| `models/clip/t5xxl_fp8_e4m3fn.safetensors` | Yes | https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/t5xxl_fp8_e4m3fn.safetensors |
| `models/clip_vision/clip-vit-large-patch14/model.safetensors` | Yes | https://huggingface.co/openai/clip-vit-large-patch14/resolve/main/model.safetensors |
| `models/clip_vision/sigclip_vision_patch14_384.safetensors` | Yes | https://huggingface.co/Comfy-Org/sigclip_vision_384/resolve/main/sigclip_vision_patch14_384.safetensors |
| `models/controlnet/FLUX.1-dev-ControlNet-Union-Pro.safetensors` | Yes | https://huggingface.co/InstantX/FLUX.1-dev-Controlnet-Union/resolve/main/diffusion_pytorch_model.safetensors |
| `models/controlnet/FLUX.1-dev-Controlnet-Inpainting-Alpha.safetensors.safetensors` | Yes | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/controlnet/FLUX.1-dev-Controlnet-Inpainting-Alpha.safetensors.safetensors |
| `models/flux/FLUX.1-schnell` | Yes | git clone https://huggingface.co/black-forest-labs/FLUX.1-schnell |
| `models/flux/OminiControl` | Yes | git clone https://huggingface.co/Yuanshi/OminiControl |
| `models/loras/20241218_1348_banny_best-step00003000.safetensors` | Yes | https://storage.googleapis.com/public-assets-xander/Random/remove/flux_loras/20241218_1348_banny_best-step00003000.safetensors |
| `models/loras/20241218_1715_xander-step00003000.safetensors` | Yes | https://storage.googleapis.com/public-assets-xander/Random/remove/flux_loras/20241218_1715_xander-step00003000.safetensors |
| `models/loras/Hyper-FLUX.1-dev-16steps-lora.safetensors` | Yes | https://huggingface.co/ByteDance/Hyper-SD/resolve/main/Hyper-FLUX.1-dev-16steps-lora.safetensors |
| `models/loras/anime_lora_comfy_converted.safetensors` | Yes | https://huggingface.co/XLabs-AI/flux-lora-collection/resolve/main/anime_lora_comfy_converted.safetensors |
| `models/loras/art_lora_comfy_converted.safetensors` | Yes | https://huggingface.co/XLabs-AI/flux-lora-collection/resolve/main/art_lora_comfy_converted.safetensors |
| `models/loras/flux1-canny-dev-lora.safetensors` | Yes | https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/checkpoints/flux1-canny-dev-lora.safetensors |
| `models/loras/flux1-depth-dev-lora.safetensors` | Yes | https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/checkpoints/flux1-depth-dev-lora.safetensors |
| `models/loras/mjv6_lora_comfy_converted.safetensors` | Yes | https://huggingface.co/XLabs-AI/flux-lora-collection/resolve/main/mjv6_lora_comfy_converted.safetensors |
| `models/loras/realism_lora_comfy_converted.safetensors` | Yes | https://huggingface.co/XLabs-AI/flux-lora-collection/resolve/main/realism_lora_comfy_converted.safetensors |
| `models/loras/scenery_lora_comfy_converted.safetensors` | Yes | https://huggingface.co/XLabs-AI/flux-lora-collection/resolve/main/scenery_lora_comfy_converted.safetensors |
| `models/style_models/flux1-redux-dev.safetensors` | Yes | https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/checkpoints/flux1-redux-dev.safetensors |
| `models/unet/flux1-dev-fp8.safetensors` | Yes | https://huggingface.co/Comfy-Org/flux1-dev/resolve/main/flux1-dev-fp8.safetensors |
| `models/unet/flux1-dev.safetensors` | Yes | https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/checkpoints/flux1-dev.safetensors |
| `models/unet/flux1-schnell.safetensors` | Yes | https://huggingface.co/black-forest-labs/FLUX.1-schnell/resolve/main/flux1-schnell.safetensors |
| `models/vae/ae.safetensors` | Yes | https://huggingface.co/black-forest-labs/FLUX.1-schnell/resolve/main/ae.safetensors |
| `models/xlabs/ipadapters/flux-ip-adapter.safetensors` | Yes | https://huggingface.co/yzd-v/DWPose/resolve/main/yolox_l.onnx |
| `models/xlabs/ipadapters/ip_adapter.safetensors` | Yes | https://huggingface.co/XLabs-AI/flux-ip-adapter/resolve/main/ip_adapter.safetensors |

### img_tools

| Asset | Is Origin | Source |
|-------|-----------|--------|
| `custom_nodes/comfyui_controlnet_aux/ckpts/TheMistoAI/MistoLine/Anyline/MTEED.pth` | No | https://huggingface.co/TheMistoAI/MistoLine/resolve/main/Anyline/MTEED.pth |
| `custom_nodes/comfyui_controlnet_aux/ckpts/depth-anything/Depth-Anything-V2-Large/depth_anything_v2_vitl.pth` | Yes | https://huggingface.co/depth-anything/Depth-Anything-V2-Large/resolve/main/depth_anything_v2_vitl.pth |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/Annotators/ControlNetHED.pth` | No | https://huggingface.co/lllyasviel/Annotators/resolve/main/ControlNetHED.pth |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/Annotators/body_pose_model.pth` | No | https://huggingface.co/lllyasviel/ControlNet/resolve/main/annotator/ckpts/body_pose_model.pth |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/Annotators/dpt_hybrid-midas-501f0c75.pt` | No | https://huggingface.co/lllyasviel/ControlNet/resolve/main/annotator/ckpts/dpt_hybrid-midas-501f0c75.pt |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/Annotators/facenet.pth` | No | https://huggingface.co/lllyasviel/Annotators/resolve/main/facenet.pth |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/Annotators/hand_pose_model.pth` | No | https://huggingface.co/lllyasviel/ControlNet/resolve/main/annotator/ckpts/hand_pose_model.pth |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/Annotators/sk_model.pth` | No | https://huggingface.co/lllyasviel/Annotators/resolve/main/sk_model.pth |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/Annotators/sk_model2.pth` | No | https://huggingface.co/lllyasviel/Annotators/resolve/main/sk_model2.pth |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/Annotators/table5_pidinet.pth` | Yes | https://huggingface.co/TencentARC/T2I-Adapter/resolve/main/third-party-models/table5_pidinet.pth |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/ckpts/yzd-v/DWPose/dw-ll_ucoco_384.onnx` | No | https://huggingface.co/yzd-v/DWPose/resolve/main/dw-ll_ucoco_384.onnx |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/ckpts/yzd-v/DWPose/yolox_l.onnx` | No | https://huggingface.co/yzd-v/DWPose/resolve/main/yolox_l.onnx |
| `input/A_black_image.jpg` | No | https://upload.wikimedia.org/wikipedia/commons/4/49/A_black_image.jpg |
| `models/checkpoints/Eden_SDXL.safetensors` | Yes | https://edenartlab-lfs.s3.amazonaws.com/models/checkpoints/Eden_SDXL.safetensors |
| `models/checkpoints/juggernautXL_version6Rundiffusion.safetensors` | Yes | https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/checkpoints/juggernautXL_version6Rundiffusion.safetensors |
| `models/checkpoints/juggernaut_reborn.safetensors` | Yes | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/checkpoints/juggernaut_reborn.safetensors |
| `models/clip_vision/CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors` | Yes | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/clip_vision/CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors |
| `models/controlnet/control_v11f1e_sd15_tile_fp16.safetensors` | Yes | https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11f1e_sd15_tile_fp16.safetensors |
| `models/controlnet/controlnet-canny-sdxl-1.0/diffusion_pytorch_model_V2.safetensors` | Yes | https://huggingface.co/xinsir/controlnet-canny-sdxl-1.0/resolve/main/diffusion_pytorch_model_V2.safetensors |
| `models/controlnet/controlnet-depth-sdxl-1.0/diffusion_pytorch_model.safetensors` | Yes | https://huggingface.co/xinsir/controlnet-depth-sdxl-1.0/resolve/main/diffusion_pytorch_model.safetensors |
| `models/controlnet/controlnet-openpose-sdxl-1.0/diffusion_pytorch_model.safetensors` | Yes | https://huggingface.co/xinsir/controlnet-openpose-sdxl-1.0/resolve/main/diffusion_pytorch_model.safetensors |
| `models/controlnet/controlnet-scribble-sdxl-1.0/diffusion_pytorch_model.safetensors` | Yes | https://huggingface.co/xinsir/controlnet-scribble-sdxl-1.0/resolve/main/diffusion_pytorch_model.safetensors |
| `models/controlnet/diffusers_xl_canny_full.safetensors` | Yes | https://huggingface.co/lllyasviel/sd_control_collection/resolve/d1b278d0d1103a3a7c4f7c2c327d236b082a75b1/diffusers_xl_canny_full.safetensors |
| `models/controlnet/t2i-adapter-lineart-sdxl-1.0/diffusion_pytorch_model.safetensors` | Yes | https://huggingface.co/TencentARC/t2i-adapter-lineart-sdxl-1.0/resolve/main/diffusion_pytorch_model.safetensors |
| `models/embeddings/negativeXL_D.safetensors` | Yes | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/embeddings/negativeXL_D.safetensors |
| `models/ipadapter/ip-adapter-plus_sd15.safetensors` | Yes | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/ipadapter/ip-adapter-plus_sd15.safetensors |
| `models/ipadapter/ip-adapter-plus_sdxl_vit-h.safetensors` | Yes | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/ipadapter/ip-adapter-plus_sdxl_vit-h.safetensors |
| `models/layer_model/layer_xl_transparent_conv.safetensors` | Yes | https://huggingface.co/LayerDiffusion/layerdiffusion-v1/resolve/main/layer_xl_transparent_conv.safetensors |
| `models/loras/SDXL_lora_xander.safetensors` | Yes | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/loras/SDXL_lora_xander.safetensors |
| `models/loras/SDXLrender_v2.0.safetensors` | Yes | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/loras/SDXLrender_v2.0.safetensors |
| `models/loras/more_details.safetensors` | Yes | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/loras/SDXLrender_v2.0.safetensors |
| `models/upscale_models/4xNomosUniDAT_otf.safetensors` | Yes | https://github.com/Phhofm/models/releases/download/4xNomosUniDAT_otf/4xNomosUniDAT_otf.safetensors |

### mars_exclusive

| Asset | Is Origin | Source |
|-------|-----------|--------|
| `custom_nodes/ComfyUI_essentials/fonts/Oswald-Bold.ttf` | Yes | https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/assets/Oswald-Bold.ttf |
| `input/barcode.png` | Yes | https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/assets/mars-id-assets/barcode.png |
| `input/frame-grayscale-no-text.png` | Yes | https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/assets/mars-id-assets/frame-grayscale-no-text.png |
| `input/id-portrait-mask.png` | Yes | https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/assets/mars-id-assets/id-portrait-mask.png |
| `input/matte-alpha.png` | Yes | https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/assets/mars-id-assets/matte-alpha.png |
| `input/matte.png` | Yes | https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/assets/mars-id-assets/matte.png |
| `input/planet-alpha.png` | Yes | https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/assets/mars-id-assets/planet-alpha.png |
| `input/text_fields_bubble.png` | Yes | https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/assets/mars-id-assets/text_fields_bubble.png |
| `models/checkpoints/flux1-schnell-fp8.safetensors` | No | https://huggingface.co/Comfy-Org/flux1-schnell/resolve/main/flux1-schnell-fp8.safetensors |

### mochi_preview

| Asset | Is Origin | Source |
|-------|-----------|--------|
| `custom_nodes/ComfyUI-Frame-Interpolation/ckpts/rife/rife47.pth` | No | https://github.com/styler00dollar/VSGAN-tensorrt-docker/releases/download/models/rife47.pth |
| `models/diffusion_models/mochi_preview_fp8_scaled.safetensors` | Yes | https://huggingface.co/Comfy-Org/mochi_preview_repackaged/blob/main/all_in_one/mochi_preview_fp8_scaled.safetensors |
| `models/upscale_models/RealESRGAN_x2plus.pth` | No | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/upscale_models/RealESRGAN_x2plus.pth |

### remix_flux_schnell

| Asset | Is Origin | Source |
|-------|-----------|--------|
| `models/checkpoints/flux1-schnell-fp8.safetensors` | No | https://huggingface.co/Comfy-Org/flux1-schnell/resolve/main/flux1-schnell-fp8.safetensors |
| `models/checkpoints/nullModel.ckpt` | Yes | https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/checkpoints/nullModel.ckpt |
| `models/clip/clip_l.safetensors` | No | https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors |
| `models/clip/t5xxl_fp8_e4m3fn.safetensors` | No | https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/t5xxl_fp8_e4m3fn.safetensors |
| `models/unet/flux1-schnell.safetensors` | No | https://huggingface.co/black-forest-labs/FLUX.1-schnell/resolve/main/flux1-schnell.safetensors |
| `models/vae/ae.safetensors` | No | https://huggingface.co/black-forest-labs/FLUX.1-schnell/resolve/main/ae.safetensors |

### sd3

| Asset | Is Origin | Source |
|-------|-----------|--------|
| `models/checkpoints/sd3.5_large_fp8_scaled.safetensors` | Yes | https://huggingface.co/Comfy-Org/stable-diffusion-3.5-fp8/resolve/main/sd3.5_large_fp8_scaled.safetensors |

### temple

| Asset | Is Origin | Source |
|-------|-----------|--------|
| `custom_nodes/comfyui_controlnet_aux/ckpts/TheMistoAI/MistoLine/Anyline/MTEED.pth` | No | https://huggingface.co/TheMistoAI/MistoLine/resolve/main/Anyline/MTEED.pth |
| `custom_nodes/comfyui_controlnet_aux/ckpts/depth-anything/Depth-Anything-V2-Large/depth_anything_v2_vitl.pth` | No | https://huggingface.co/depth-anything/Depth-Anything-V2-Large/resolve/main/depth_anything_v2_vitl.pth |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/Annotators/ControlNetHED.pth` | No | https://huggingface.co/lllyasviel/Annotators/resolve/main/ControlNetHED.pth |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/Annotators/body_pose_model.pth` | No | https://huggingface.co/lllyasviel/ControlNet/resolve/main/annotator/ckpts/body_pose_model.pth |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/Annotators/dpt_hybrid-midas-501f0c75.pt` | No | https://huggingface.co/lllyasviel/ControlNet/resolve/main/annotator/ckpts/dpt_hybrid-midas-501f0c75.pt |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/Annotators/facenet.pth` | No | https://huggingface.co/lllyasviel/Annotators/resolve/main/facenet.pth |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/Annotators/hand_pose_model.pth` | No | https://huggingface.co/lllyasviel/ControlNet/resolve/main/annotator/ckpts/hand_pose_model.pth |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/Annotators/sk_model.pth` | No | https://huggingface.co/lllyasviel/Annotators/resolve/main/sk_model.pth |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/Annotators/sk_model2.pth` | No | https://huggingface.co/lllyasviel/Annotators/resolve/main/sk_model2.pth |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/Annotators/table5_pidinet.pth` | No | https://huggingface.co/TencentARC/T2I-Adapter/resolve/main/third-party-models/table5_pidinet.pth |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/ckpts/yzd-v/DWPose/dw-ll_ucoco_384.onnx` | No | https://huggingface.co/yzd-v/DWPose/resolve/main/dw-ll_ucoco_384.onnx |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/ckpts/yzd-v/DWPose/yolox_l.onnx` | No | https://huggingface.co/yzd-v/DWPose/resolve/main/yolox_l.onnx |
| `input/A_black_image.jpg` | No | https://upload.wikimedia.org/wikipedia/commons/4/49/A_black_image.jpg |
| `input/black_dummy.jpg` | No | https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/assets/black_dummy.jpg |
| `models/checkpoints/Eden_SDXL.safetensors` | No | https://edenartlab-lfs.s3.amazonaws.com/models/checkpoints/Eden_SDXL.safetensors |
| `models/checkpoints/juggernautXL_version6Rundiffusion.safetensors` | No | https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/checkpoints/juggernautXL_version6Rundiffusion.safetensors |
| `models/clip_vision/CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors` | No | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/clip_vision/CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors |
| `models/controlnet/controlnet-canny-sdxl-1.0/diffusion_pytorch_model_V2.safetensors` | No | https://huggingface.co/xinsir/controlnet-canny-sdxl-1.0/resolve/main/diffusion_pytorch_model_V2.safetensors |
| `models/controlnet/controlnet-depth-sdxl-1.0/diffusion_pytorch_model.safetensors` | No | https://huggingface.co/xinsir/controlnet-depth-sdxl-1.0/resolve/main/diffusion_pytorch_model.safetensors |
| `models/controlnet/controlnet-openpose-sdxl-1.0/diffusion_pytorch_model.safetensors` | No | https://huggingface.co/xinsir/controlnet-openpose-sdxl-1.0/resolve/main/diffusion_pytorch_model.safetensors |
| `models/controlnet/controlnet-scribble-sdxl-1.0/diffusion_pytorch_model.safetensors` | No | https://huggingface.co/xinsir/controlnet-scribble-sdxl-1.0/resolve/main/diffusion_pytorch_model.safetensors |
| `models/controlnet/diffusers_xl_canny_full.safetensors` | No | https://huggingface.co/lllyasviel/sd_control_collection/resolve/d1b278d0d1103a3a7c4f7c2c327d236b082a75b1/diffusers_xl_canny_full.safetensors |
| `models/controlnet/t2i-adapter-lineart-sdxl-1.0/diffusion_pytorch_model.safetensors` | No | https://huggingface.co/TencentARC/t2i-adapter-lineart-sdxl-1.0/resolve/main/diffusion_pytorch_model.safetensors |
| `models/embeddings/froyd7sinsmodel_sdxl_embeddings.safetensors` | Yes | https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/assets/temple_abyss/froyd7sinsmodel_sdxl_embeddings.safetensors |
| `models/embeddings/negativeXL_D.safetensors` | No | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/embeddings/negativeXL_D.safetensors |
| `models/ipadapter/ip-adapter-plus_sd15.safetensors` | No | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/ipadapter/ip-adapter-plus_sd15.safetensors |
| `models/ipadapter/ip-adapter-plus_sdxl_vit-h.safetensors` | No | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/ipadapter/ip-adapter-plus_sdxl_vit-h.safetensors |
| `models/loras/froyd7sinsmodel_sdxl_lora.safetensors` | Yes | https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/assets/temple_abyss/froyd7sinsmodel_sdxl_lora.safetensors |

### txt2img

| Asset | Is Origin | Source |
|-------|-----------|--------|
| `custom_nodes/comfyui_controlnet_aux/ckpts/TheMistoAI/MistoLine/Anyline/MTEED.pth` | No | https://huggingface.co/TheMistoAI/MistoLine/resolve/main/Anyline/MTEED.pth |
| `custom_nodes/comfyui_controlnet_aux/ckpts/depth-anything/Depth-Anything-V2-Large/depth_anything_v2_vitl.pth` | No | https://huggingface.co/depth-anything/Depth-Anything-V2-Large/resolve/main/depth_anything_v2_vitl.pth |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/Annotators/ControlNetHED.pth` | No | https://huggingface.co/lllyasviel/Annotators/resolve/main/ControlNetHED.pth |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/Annotators/body_pose_model.pth` | No | https://huggingface.co/lllyasviel/ControlNet/resolve/main/annotator/ckpts/body_pose_model.pth |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/Annotators/dpt_hybrid-midas-501f0c75.pt` | No | https://huggingface.co/lllyasviel/ControlNet/resolve/main/annotator/ckpts/dpt_hybrid-midas-501f0c75.pt |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/Annotators/facenet.pth` | No | https://huggingface.co/lllyasviel/Annotators/resolve/main/facenet.pth |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/Annotators/hand_pose_model.pth` | No | https://huggingface.co/lllyasviel/ControlNet/resolve/main/annotator/ckpts/hand_pose_model.pth |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/Annotators/sk_model.pth` | No | https://huggingface.co/lllyasviel/Annotators/resolve/main/sk_model.pth |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/Annotators/sk_model2.pth` | No | https://huggingface.co/lllyasviel/Annotators/resolve/main/sk_model2.pth |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/Annotators/table5_pidinet.pth` | No | https://huggingface.co/TencentARC/T2I-Adapter/resolve/main/third-party-models/table5_pidinet.pth |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/ckpts/yzd-v/DWPose/dw-ll_ucoco_384.onnx` | No | https://huggingface.co/yzd-v/DWPose/resolve/main/dw-ll_ucoco_384.onnx |
| `custom_nodes/comfyui_controlnet_aux/ckpts/lllyasviel/ckpts/yzd-v/DWPose/yolox_l.onnx` | No | https://huggingface.co/yzd-v/DWPose/resolve/main/yolox_l.onnx |
| `inpaint/PowerPaint-v2-1/diffusion_pytorch_model.safetensors` | Yes | https://huggingface.co/JunhaoZhuang/PowerPaint-v2-1/resolve/main/PowerPaint_Brushnet/diffusion_pytorch_model.safetensors |
| `inpaint/PowerPaint-v2-1/pytorch_model.bin` | Yes | https://huggingface.co/JunhaoZhuang/PowerPaint-v2-1/resolve/main/PowerPaint_Brushnet/pytorch_model.bin |
| `input/A_black_image.jpg` | No | https://upload.wikimedia.org/wikipedia/commons/4/49/A_black_image.jpg |
| `models/checkpoints/Eden_SDXL.safetensors` | No | https://edenartlab-lfs.s3.amazonaws.com/models/checkpoints/Eden_SDXL.safetensors |
| `models/checkpoints/dreamshaperXL_lightningDPMSDE.safetensors` | Yes | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/checkpoints/dreamshaperXL_lightningDPMSDE.safetensors |
| `models/checkpoints/juggernautXL_version2.safetensors` | Yes | https://edenartlab-lfs.s3.amazonaws.com/models2/checkpoints/juggernautXL_version2.safetensors |
| `models/checkpoints/juggernaut_reborn.safetensors` | No | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/checkpoints/juggernaut_reborn.safetensors |
| `models/checkpoints/juggerxlInpaint_juggerInpaintV8.safetensors` | Yes | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/checkpoints/juggerxlInpaint_juggerInpaintV8.safetensors |
| `models/clip/model.fp16.safetensors` | Yes | https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/text_encoder/model.fp16.safetensors |
| `models/clip_vision/CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors` | No | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/clip_vision/CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors |
| `models/controlnet/controlnet-canny-sdxl-1.0/diffusion_pytorch_model_V2.safetensors` | No | https://huggingface.co/xinsir/controlnet-canny-sdxl-1.0/resolve/main/diffusion_pytorch_model_V2.safetensors |
| `models/controlnet/controlnet-depth-sdxl-1.0/diffusion_pytorch_model.safetensors` | No | https://huggingface.co/xinsir/controlnet-depth-sdxl-1.0/resolve/main/diffusion_pytorch_model.safetensors |
| `models/controlnet/controlnet-openpose-sdxl-1.0/diffusion_pytorch_model.safetensors` | No | https://huggingface.co/xinsir/controlnet-openpose-sdxl-1.0/resolve/main/diffusion_pytorch_model.safetensors |
| `models/controlnet/controlnet-scribble-sdxl-1.0/diffusion_pytorch_model.safetensors` | No | https://huggingface.co/xinsir/controlnet-scribble-sdxl-1.0/resolve/main/diffusion_pytorch_model.safetensors |
| `models/controlnet/diffusers_xl_canny_full.safetensors` | No | https://huggingface.co/lllyasviel/sd_control_collection/resolve/d1b278d0d1103a3a7c4f7c2c327d236b082a75b1/diffusers_xl_canny_full.safetensors |
| `models/controlnet/t2i-adapter-lineart-sdxl-1.0/diffusion_pytorch_model.safetensors` | No | https://huggingface.co/TencentARC/t2i-adapter-lineart-sdxl-1.0/resolve/main/diffusion_pytorch_model.safetensors |
| `models/embeddings/EasyNegative.safetensors` | Yes | https://huggingface.co/datasets/gsdf/EasyNegative/resolve/main/EasyNegative.safetensors |
| `models/embeddings/negativeXL_D.safetensors` | No | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/embeddings/negativeXL_D.safetensors |
| `models/insightface/inswapper_128.onnx` | Yes | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/insightface/inswapper_128.onnx |
| `models/insightface/models/antelopev2/1k3d68.onnx` | Yes | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/insightface/models/antelopev2/1k3d68.onnx |
| `models/insightface/models/antelopev2/2d106det.onnx` | Yes | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/insightface/models/antelopev2/2d106det.onnx |
| `models/insightface/models/antelopev2/genderage.onnx` | Yes | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/insightface/models/antelopev2/genderage.onnx |
| `models/insightface/models/antelopev2/glintr100.onnx` | Yes | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/insightface/models/antelopev2/glintr100.onnx |
| `models/insightface/models/antelopev2/scrfd_10g_bnkps.onnx` | Yes | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/insightface/models/antelopev2/scrfd_10g_bnkps.onnx |
| `models/ipadapter/ip-adapter-plus_sd15.safetensors` | No | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/ipadapter/ip-adapter-plus_sd15.safetensors |
| `models/ipadapter/ip-adapter-plus_sdxl_vit-h.safetensors` | No | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/ipadapter/ip-adapter-plus_sdxl_vit-h.safetensors |
| `models/loras/SDXL_lora_xander.safetensors` | No | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/loras/SDXL_lora_xander.safetensors |
| `models/pulid/ip-adapter_pulid_sdxl_fp16.safetensors` | Yes | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/pulid/ip-adapter_pulid_sdxl_fp16.safetensors |
| `models/upscale_models/RealESRGAN_x2plus.pth` | Yes | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/upscale_models/RealESRGAN_x2plus.pth |

### video

| Asset | Is Origin | Source |
|-------|-----------|--------|
| `custom_nodes/ComfyUI-Frame-Interpolation/ckpts/rife/rife47.pth` | No | https://github.com/styler00dollar/VSGAN-tensorrt-docker/releases/download/models/rife47.pth |
| `custom_nodes/ComfyUI-VideoHelperSuite/video_formats/eden-video-faststart.json` | Yes | https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/assets/eden-video-faststart.json |
| `custom_nodes/comfyui_controlnet_aux/ckpts/depth-anything/Depth-Anything-V2-Large/depth_anything_v2_vitl.pth` | No | https://huggingface.co/depth-anything/Depth-Anything-V2-Large/resolve/main/depth_anything_v2_vitl.pth |
| `input/A_black_image.jpg` | No | https://upload.wikimedia.org/wikipedia/commons/4/49/A_black_image.jpg |
| `input/A_white_image.jpg` | Yes | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/assets/A_white_image.jpg |
| `input/a_black_video.mp4` | Yes | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/assets/a_black_video.mp4 |
| `models/animatediff_models/AnimateLCM_sd15_t2v.ckpt` | Yes | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/animatediff_models/AnimateLCM_sd15_t2v.ckpt |
| `models/animatediff_models/hsxl_temporal_layers.f16.safetensors` | Yes | https://huggingface.co/hotshotco/Hotshot-XL/resolve/main/hsxl_temporal_layers.f16.safetensors |
| `models/animatediff_models/mm_sd_v15_v2.ckpt` | Yes | https://huggingface.co/guoyww/animatediff/resolve/main/mm_sd_v15_v2.ckpt?download=true |
| `models/animatediff_models/sd15_t2v_beta.ckpt` | Yes | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/animatediff_models/sd15_t2v_beta.ckpt |
| `models/animatediff_models/v3_sd15_mm.ckpt` | Yes | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/animatediff_models/v3_sd15_mm.ckpt |
| `models/checkpoints/Eden_SDXL.safetensors` | No | https://edenartlab-lfs.s3.amazonaws.com/models/checkpoints/Eden_SDXL.safetensors |
| `models/checkpoints/SD15/LCM/realismBYSTABLEYOGI_v4LCM.safetensors` | Yes | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/checkpoints/realismBYSTABLEYOGI_v4LCM.safetensors |
| `models/checkpoints/juggernaut_reborn-inpainting.safetensors` | Yes | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/checkpoints/juggernaut_reborn-inpainting.safetensors |
| `models/checkpoints/juggernaut_reborn.safetensors` | No | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/checkpoints/juggernaut_reborn.safetensors |
| `models/checkpoints/juggerxlInpaint_juggerInpaintV8.safetensors` | No | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/checkpoints/juggerxlInpaint_juggerInpaintV8.safetensors |
| `models/checkpoints/zavychromaxl_v80.safetensors` | Yes | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/checkpoints/zavychromaxl_v80.safetensors |
| `models/clip_vision/CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors` | No | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/clip_vision/CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors |
| `models/controlnet/SDXL/controlnet-canny-sdxl-1.0/diffusion_pytorch_model_V2.safetensors` | Yes | https://huggingface.co/xinsir/controlnet-canny-sdxl-1.0/resolve/main/diffusion_pytorch_model_V2.safetensors |
| `models/controlnet/SDXL/controlnet-depth-sdxl-1.0/diffusion_pytorch_model.safetensors` | Yes | https://huggingface.co/xinsir/controlnet-depth-sdxl-1.0/resolve/main/diffusion_pytorch_model.safetensors |
| `models/controlnet/adiff_ControlGIF_controlnet.ckpt` | Yes | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/controlnet/adiff_ControlGIF_controlnet.ckpt |
| `models/controlnet/control_v11f1p_sd15_depth.pth` | Yes | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/controlnet/control_v11f1p_sd15_depth.pth |
| `models/controlnet/control_v11p_sd15_canny.pth` | Yes | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/controlnet/control_v11p_sd15_canny.pth |
| `models/controlnet/control_v11p_sd15_canny_fp16.safetensors` | Yes | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/controlnet/control_v11p_sd15_canny_fp16.safetensors |
| `models/controlnet/control_v11p_sd15_lineart.pth` | Yes | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/controlnet/control_v11p_sd15_lineart.pth |
| `models/controlnet/control_v11p_sd15_openpose.pth` | Yes | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/controlnet/control_v11p_sd15_openpose.pth |
| `models/controlnet/control_v11p_sd15_scribble.pth` | Yes | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/controlnet/control_v11p_sd15_scribble.pth |
| `models/controlnet/controlnetQRPatternQR_v2Sd15.safetensors` | Yes | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/controlnet/controlnetQRPatternQR_v2Sd15.safetensors |
| `models/controlnet/controlnet_checkpoint.ckpt` | Yes | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/controlnet/controlnet_checkpoint.ckpt |
| `models/controlnet/v3_sd15_sparsectrl_rgb.ckpt` | Yes | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/controlnet/v3_sd15_sparsectrl_rgb.ckpt |
| `models/controlnet/v3_sd15_sparsectrl_scribble.ckpt` | Yes | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/controlnet/v3_sd15_sparsectrl_scribble.ckpt |
| `models/depthanything/depth_anything_v2_vitl_fp16.safetensors` | Yes | https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/depthanything/depth_anything_v2_vitl_fp16.safetensors |
| `models/embeddings/NEG_EMBED_STABLE_YOGI_V3.pt` | Yes | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/embeddings/NEG_EMBED_STABLE_YOGI_V3.pt |
| `models/ipadapter/ip-adapter-plus_sd15.safetensors` | No | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/ipadapter/ip-adapter-plus_sd15.safetensors |
| `models/ipadapter/ip-adapter-plus_sdxl_vit-h.safetensors` | No | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/ipadapter/ip-adapter-plus_sdxl_vit-h.safetensors |
| `models/loras/v3_sd15_adapter.ckpt` | Yes | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/loras/v3_sd15_adapter.ckpt |
| `models/upscale_models/RealESRGAN_x2plus.pth` | No | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/upscale_models/RealESRGAN_x2plus.pth |
| `root/.cache/torch/hub/checkpoints/alexnet-owt-7be5be79.pth` | Yes | https://download.pytorch.org/models/alexnet-owt-7be5be79.pth |

### video2

| Asset | Is Origin | Source |
|-------|-----------|--------|
| `custom_nodes/ComfyUI-Frame-Interpolation/ckpts/rife/rife47.pth` | No | https://github.com/styler00dollar/VSGAN-tensorrt-docker/releases/download/models/rife47.pth |
| `models/checkpoints/mochi_preview_fp8_scaled3.safetensors` | Yes | https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/checkpoints/mochi_preview_fp8_scaled.safetensors |
| `models/upscale_models/RealESRGAN_x2plus.pth` | No | https://edenartlab-lfs.s3.amazonaws.com/comfyui/models2/upscale_models/RealESRGAN_x2plus.pth |

