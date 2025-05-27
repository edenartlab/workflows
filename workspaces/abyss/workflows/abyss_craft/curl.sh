#!/bin/bash

curl -X POST "https://api.eden.art/v2/tasks/create" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: YOUR_API_KEY" \
  -d @- << 'EOF'
{
  "tool": "abyss_craft",
  "args": {
    "n_samples": 1,
    "prompt_init_image": "An ancient rusted sword with blue-tinted metal blade emerging from a pool of swirling crimson liquid, dramatic lighting, dark fantasy, high detail, weathered metal texture with azure patina, ominous atmosphere, flowing red energy surrounding the blade, cinematic composition, 8k, photorealistic rendering, dark background, artifact photography, sharp focus, volumetric lighting",
    "prompt_prepend": "in the style of (embedding:froyd7sinsmodel_sdxl_embeddings.safetensors), japanese anime style, comic book dark fantasy style, thick thick thick bold linework, illustration, ",
    "prompt": "An ancient rusted sword with blue-tinted metal blade emerging from a pool of swirling crimson liquid, dramatic lighting, dark fantasy, high detail, weathered metal texture with azure patina, ominous atmosphere, flowing red energy surrounding the blade, cinematic composition, 8k, photorealistic rendering, dark background, artifact photography, sharp focus, volumetric lighting",
    "prompt_append": ",  the overall style of the artwork is moody, with a focus on texture and light, creating a sense of depth and mystery, serene mood, tritone tritone tritone, eerie, dark shadows, ",
    "negative_prompt": "wobly lines, arms, screen, feminine, girly, skulls, faces, demons, creatures, bodies, people, hands, watermark, text, nude, naked, nsfw, poorly drawn face, ugly, tiling, out of frame, blurry, blurred, grainy, signature, cut off, draft",
    "steps": 50,
    "use_init_as_controlnet": false,
    "use_init_as_art_image": false,
    "use_init_as_full_art_image": false,
    "card_name": "",
    "clan_name": "azure",
    "trait": "Sword of Virginity",
    "card_text": "While you partied, I studied the blade. We are not the same.",
    "rng_points": "420",
    "controlnet_strength": 0.8,
    "controlnet": "depth",
    "lora": "67a222bae707584b6d669623",
    "lora_strength": 0.55,
    "denoise": 0.95,
    "essence": "ancient",
    "variation": "brutal_swirl",
    "item": "weapon",
    "rarity": "ultrarare"
  }
}
EOF