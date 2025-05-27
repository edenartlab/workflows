"""
Temple Abyss Epic Lore Master Card Generator Script

This script generates custom Temple Abyss cards with epic lore master styling and AI-generated artwork.

Basic Usage:
    python api_call.py --api-key YOUR_API_KEY

Optional Parameters:
    --prompt-init-image "Your init image description" : Description for initial image generation
    --prompt "Your custom art description"           : Describe the artwork you want generated
    --prompt-prepend "Style modifiers"              : Style and aesthetic modifiers to prepend
    --prompt-append "Additional details"            : Additional details to append
    --negative-prompt "What to avoid"               : Describe what you don't want in the art
    --seed 123456789                               : Set random seed for reproducible results
    --n-samples 1                                  : Number of images to generate (1-4)
    --steps 50                                     : Number of diffusion steps (10-50)
    --use-init-as-controlnet                       : Use init image as ControlNet reference
    --use-init-as-art-image                        : Use init image as art image
    --use-init-as-full-art-image                   : Use pre-rendered full art image
    --init-image "url/to/image.png"                : Reference image for ControlNet guidance
    --clan-name [jade/scarlet/azure/grey]          : Clan affiliation for the card
    --trait "Card Trait"                           : Trait text
    --card-text "Card Description"                 : Card effect description
    --rng-points "123"                             : Point value
    --controlnet-strength 0.8                      : Strength of image guidance (0.0-1.0)
    --controlnet [none/canny/depth/etc]            : Type of image guidance
    --lora "67a222bae707584b6d669623"             : Custom LoRA model ID
    --lora-strength 0.42                           : Strength of style effect (0.0-1.0)
    --denoise 1.0                                  : Denoise strength (0.0-1.0)
    --essence [ancient/blessed/cursed/forged]      : Card essence type
    --variation [brutal_swirl/etc]                 : Background variation style
    --item [potion/scroll/spell/weapon]            : Item type for the card
    --rarity [common/ultrarare/etc]                : Card rarity level
    --sampler-name [euler/etc]                     : Sampling algorithm
    --scheduler [normal/karras/etc]                : Scheduler type
    --cfg 1.0                                      : CFG scale (1.0-20.0)

Example:
    python api_call.py --api-key abc123 --trait "Explore The Vines" --clan-name azure

The script will generate the card artwork and compose it with epic lore master styling, saving the result to ./generated_images/
"""

import requests
import time
import os
import argparse
from pathlib import Path

class EdenAIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.eden.art/v2"
        self.headers = {
            "Content-Type": "application/json",
            "X-Api-Key": api_key
        }

    def create_image(self, args):
        payload = {
            "tool": "temple_abyss_epic_lore_master",
            "args": {
                "n_samples": args.n_samples,
                "prompt_init_image": args.prompt_init_image,
                "prompt": args.prompt,
                "prompt_prepend": args.prompt_prepend,
                "prompt_append": args.prompt_append,
                "negative_prompt": args.negative_prompt,
                "seed": None if args.seed == "random" else int(args.seed),
                "steps": args.steps,
                "use_init_as_controlnet": args.use_init_as_controlnet,
                "use_init_as_art_image": args.use_init_as_art_image,
                "use_init_as_full_art_image": args.use_init_as_full_art_image,
                "init_image": args.init_image,
                "clan_name": args.clan_name,
                "trait": args.trait,
                "card_text": args.card_text,
                "rng_points": str(args.rng_points),
                "controlnet_strength": args.controlnet_strength,
                "controlnet": args.controlnet,
                "lora": args.lora,
                "lora_strength": args.lora_strength,
                "denoise": args.denoise,
                "essence": args.essence,
                "variation": args.variation,
                "item": args.item,
                "rarity": args.rarity,
                "sampler_name": args.sampler_name,
                "scheduler": args.scheduler,
                "cfg": args.cfg
            }
        }

        response = requests.post(
            f"{self.base_url}/tasks/create",
            headers=self.headers,
            json=payload
        )
        response.raise_for_status()
        
        task_id = response.json()["task"]["_id"]
        print(f"Task created with ID: {task_id}")
        return task_id

    def check_task_status(self, task_id):
        response = requests.get(
            f"{self.base_url}/tasks/{task_id}",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()["task"]

    def wait_for_completion(self, task_id, check_interval=5, timeout=300):
        start_time = time.time()
        while True:
            if time.time() - start_time > timeout:
                raise TimeoutError(f"Task did not complete within {timeout} seconds")

            task = self.check_task_status(task_id)
            current_status = task["status"]
            print(f"Current status: {current_status}")
            
            if current_status == "completed":
                return task
            elif current_status == "failed":
                raise Exception(f"Task failed: {task.get('error', 'Unknown error')}")
            
            time.sleep(check_interval)

    def download_image(self, task_id, output_dir="generated_images"):
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        task = self.check_task_status(task_id)
        if task["status"] != "completed":
            raise Exception("Task is not completed")
        
        # Wait for result to be available
        while not task["result"]:
            time.sleep(5)
            task = self.check_task_status(task_id)
            
        image_url = task["result"][0]["output"][0]["url"]
        print(f"Raw image URL: {image_url}")
        
        response = requests.get(image_url)
        response.raise_for_status()
        
        output_path = os.path.join(output_dir, f"{task_id}.png")
        with open(output_path, "wb") as f:
            f.write(response.content)
        
        print(f"Image saved to: {output_path}")
        return output_path

def main():
    parser = argparse.ArgumentParser(description='Generate images using Eden AI Epic Lore Master API')
    parser.add_argument('--api-key', required=True, help='Your Eden AI API key')
    parser.add_argument('--prompt-init-image', default="An ancient rusted sword with blue-tinted metal blade emerging from a pool of swirling crimson liquid, dramatic lighting, dark fantasy, high detail, weathered metal texture with azure patina, ominous atmosphere, flowing red energy surrounding the blade, cinematic composition, 8k, photorealistic rendering, dark background, artifact photography, sharp focus, volumetric lighting", help='Initial image prompt')
    parser.add_argument('--prompt', default="An ancient rusted sword with blue-tinted metal blade emerging from a pool of swirling crimson liquid, dramatic lighting, dark fantasy, high detail, weathered metal texture with azure patina, ominous atmosphere, flowing red energy surrounding the blade, cinematic composition, 8k, photorealistic rendering, dark background, artifact photography, sharp focus, volumetric lighting", help='Main prompt for image generation')
    parser.add_argument('--prompt-prepend', default="in the style of (embedding:froyd7sinsmodel_sdxl_embeddings.safetensors), japanese anime style, comic book dark fantasy style, thick thick thick bold linework, illustration, ", help='Style modifiers to prepend to the prompt')
    parser.add_argument('--prompt-append', default=",  the overall style of the artwork is moody, with a focus on texture and light, creating a sense of depth and mystery, serene mood, tritone tritone tritone, eerie, dark shadows, ", help='Additional details to append to the prompt')
    parser.add_argument('--negative-prompt', default="wobly lines, arms, screen, feminine, girly, skulls, faces, demons, creatures, bodies, people, hands, watermark, text, nude, naked, nsfw, poorly drawn face, ugly, tiling, out of frame, blurry, blurred, grainy, signature, cut off, draft", help='Optional custom negative prompt')
    parser.add_argument('--seed', default="123456789", help='Set random seed for reproducible results (use "random" for random seed)')
    parser.add_argument('--n-samples', type=int, default=1, choices=[1, 2, 3, 4], help='Number of images to generate')
    parser.add_argument('--steps', type=int, default=50, choices=range(10, 51), help='Number of diffusion steps (10-50)')
    parser.add_argument('--use-init-as-controlnet', action='store_true', help='Use init image as ControlNet reference')
    parser.add_argument('--use-init-as-art-image', action='store_true', help='Use init image as art image')
    parser.add_argument('--use-init-as-full-art-image', action='store_true', help='Use pre-rendered full art image')
    parser.add_argument('--init-image', default="https://d14i3advvh2bvd.cloudfront.net/0eb0ae437618bef99a49fc6c8be263e316f8e4b3bc069b4eb4196e746f88b38e_2560.webp", help='Reference image for ControlNet guidance')
    parser.add_argument('--clan-name', default="azure", choices=['jade', 'scarlet', 'azure', 'grey'], help='Clan affiliation for the card')
    parser.add_argument('--trait', default="Undisturbed Concentration", help='Trait of the card')
    parser.add_argument('--card-text', default="Gaemaeg is a master of unwavering concentration. He is able to focus on a single task for extended periods of time, even as the world around him crumbles.", help='Description text for the card')
    parser.add_argument('--rng-points', default="420", help='Point value for the card')
    parser.add_argument('--controlnet-strength', type=float, default=0.8, help='Strength of ControlNet guidance')
    parser.add_argument('--controlnet', default="depth", choices=['none', 'canny', 'depth', 'scribble', 'pose', 'threshold', 'lineart'], help='Type of ControlNet preprocessor')
    parser.add_argument('--lora', default="67a222bae707584b6d669623", help='Custom LoRA model ID')
    parser.add_argument('--lora-strength', type=float, default=0.42, help='Strength of the LoRA effect')
    parser.add_argument('--denoise', type=float, default=1.0, help='Denoise strength (0.0-1.0)')
    parser.add_argument('--essence', default="ancient", choices=['ancient', 'blessed', 'cursed', 'forged'], help='Card essence type')
    parser.add_argument('--variation', default="brutal_swirl", choices=['brutal_swirl', 'cruel_claws', 'cursed_curves', 'darknight_rises', 'lost_river', 'night_tiger', 'raw_and_ripped', 'ripsofthe_void', 'torn_beyond', 'whirling_void'], help='Background variation style')
    parser.add_argument('--item', default="weapon", choices=['potion', 'scroll', 'spell', 'weapon'], help='Item type for the card')
    parser.add_argument('--rarity', default="ultrarare", choices=['common', 'uncommon', 'rare', 'superrare', 'ultrarare', 'condemned'], help='Card rarity level')
    parser.add_argument('--sampler-name', default="euler", choices=['euler', 'euler_ancestral', 'heun', 'dpm_2', 'dpm_2_ancestral', 'lms', 'dpm_fast', 'dpm_adaptive', 'dpmpp_2s_ancestral', 'dpmpp_sde', 'dpmpp_2m', 'ddpm', 'plms'], help='Sampling algorithm')
    parser.add_argument('--scheduler', default="simple", choices=['normal', 'karras', 'simple', 'ddim_uniform'], help='Scheduler type')
    parser.add_argument('--cfg', type=float, default=1.0, help='CFG scale (1.0-20.0)')
    
    args = parser.parse_args()
    client = EdenAIClient(args.api_key)
    
    try:
        task_id = client.create_image(args)
        print("Waiting for image generation to complete...")
        client.wait_for_completion(task_id)
        image_path = client.download_image(task_id)
        print(f"Process completed successfully! Image saved at: {image_path}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 