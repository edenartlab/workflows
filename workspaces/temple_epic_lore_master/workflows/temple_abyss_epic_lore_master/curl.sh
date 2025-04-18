#!/bin/bash

curl -X POST "https://api.eden.art/v2/tasks/create" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: YOUR_API_KEY" \
  -d @- << 'EOF'
{
  "tool": "temple_abyss_epic_lore_master",
  "args": {
    "n_samples": 1,
    "prompt": "Ancient sigil partially covered by vines, resting against a stone pillar, in a dim, mysterious underground realm with hints of past glory.",
    "prompt_prepend": "aesthetic anime, akira, dark fantasy, thick bold linework, illustration,",
    "prompt_append": "serene mood, contemplative, tritone, eerie, dark shadows, atmospheric, moody, highly detailed, (dramatic shadows:1.2)",
    "negative_prompt": "wobly lines, arms, screen, feminine, girly, skulls, faces, demons, creatures, bodies, people, hands, watermark, text, nude, naked, nsfw, poorly drawn face, ugly, tiling, out of frame, blurry, blurred, grainy, signature, cut off, draft",
    "seed": 42069,
    "steps": 50,
    "steps_outpaint": 35,
    "use_init_as_art_image": false,
    "use_init_as_full_art_image": false,
    "clan_name": "azure",
    "init_image": "https://d14i3advvh2bvd.cloudfront.net/0eb0ae437618bef99a49fc6c8be263e316f8e4b3bc069b4eb4196e746f88b38e_2560.webp",
    "card_name": "Gaemaeg",
    "trait": "Undisturbed Concentration",
    "card_text": "Gaemaeg is a master of unwavering concentration. He is able to focus on a single task for extended periods of time, even as the world around him crumbles.",
    "rng_points": "420",
    "controlnet_strength": 0.80,
    "controlnet": "depth",
    "lora": "67a222bae707584b6d669623",
    "lora_strength": 0.42
  }
}
EOF