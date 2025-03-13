#!/bin/bash

curl -X POST "https://api.eden.art/v2/tasks/create" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: YOUR_API_KEY \
  -d @- << 'EOF'
{
  "tool": "temple_abyss",
  "args": {
    "n_samples": 1,
    "prompt": "japanese anime style, comic book dark fantasy style, thick thick thick bold linework, illustration, An enigmatic figure in a crimson cloak stands on a mountain peak, surrounded by ancient symbols, overlooking a vast landscape, as a blue energy pulse fades into the setting sun., the overall style of the artwork is moody, with a focus on texture and light, creating a sense of depth and mystery, serene mood, tritone tritone tritone, eerie, dark shadows",
    "negative_prompt": "wobly lines, arms, screen, feminine, girly, skulls, faces, demons, creatures, bodies, people, hands, watermark, text, nude, naked, nsfw, poorly drawn face, ugly, tiling, out of frame, blurry, blurred, grainy, signature, cut off, draft",
    "seed": 139312872,
    "use_rendered_art_image": false,
    "rendered_art_image": "https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/assets/temple_abyss/steve.png",
    "background_image": "https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/assets/temple_abyss/Rare+%2B+Super+Rare+(Teal)+Design+%232%404.22x.png",
    "clan_icon": "https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/assets/temple_abyss/Grey-Ultra-Rare-Clan-Badge.png",
    "rarity_icon": "https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/assets/temple_abyss/Ultra-Rare-Jade%404.22x.png",
    "aura_icon": "https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/assets/temple_abyss/Aura-Point-ICON%404.22x.png",
    "init_image": "https://images.pexels.com/photos/28359692/pexels-photo-28359692.jpeg",
    "card_name": "Ghuda",
    "trait": "Discovery",
    "card_text": "Ghuda deciphered cryptic texts, but the loss few sacred symbols unsettle him and the Scarlet. The once hidden depths remain shrouded in mystery.",
    "rng_points": "30",
    "controlnet_strength": 0.80,
    "controlnet": "depth",
    "lora": "67a222bae707584b6d669623",
    "lora_strength": 0.68
  }
}
EOF