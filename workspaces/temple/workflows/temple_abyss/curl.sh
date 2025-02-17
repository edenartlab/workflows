#!/bin/bash

curl -X POST "https://api.eden.art/v2/tasks/create" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: YOUR_API_KEY" \
  -d @- << 'EOF'
{
  "tool": "temple_abyss",
  "args": {
    "n_samples": 1,
    "prompt": "Steve is the curmudgeonly manager of the Garden of Eden, japanese anime style, comic book dark fantasy style, thick thick thick bold linework, illustration, Steve, the dissapointed Manager of the garden of eden stares disapprovingly, obscure symbols glowing on the stone floor, shadows flickering around, candles illuminating the scene with warm light., the overall style of the artwork is moody, with a focus on texture and light, creating a sense of depth and mystery, serene mood, tritone tritone tritone, eerie, dark shadows, embedding:froyd7sinsmodel_sdxl_embeddings",
    "negative_prompt": "wobly lines, arms, screen, feminine, girly, skulls, faces, demons, creatures, bodies, people, hands, watermark, text, nude, naked, nsfw, poorly drawn face, ugly, tiling, out of frame, blurry, blurred, grainy, signature, cut off, draft",
    "seed": 214748364,
    "use_rendered_art_image": false,
    "rendered_art_image": "https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/assets/temple_abyss/steve.png",
    "background_image": "https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/assets/temple_abyss/Rare+%2B+Super+Rare+(Teal)+Design+%232%404.22x.png",
    "clan_icon": "https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/assets/temple_abyss/Grey-Ultra-Rare-Clan-Badge.png",
    "rarity_icon": "https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/assets/temple_abyss/Ultra-Rare-Jade%404.22x.png",
    "aura_icon": "https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/assets/temple_abyss/Aura-Point-ICON%404.22x.png",
    "init_image": "https://edenartlab-lfs.s3.us-east-1.amazonaws.com/comfyui/models2/assets/temple_abyss/steve.png",
    "card_name": "STEVE",
    "trait": "Eden's Manager",
    "card_text": "Steve stares you down with a look you can only interpret as disapproval. You'll later ask your therapist why it is you so desparately seek his validation.",
    "rng_points": "420",
    "controlnet_strength": 0.80,
    "controlnet": "depth",
    "lora_strength": 0.68
  }
}
EOF

