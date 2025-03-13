"""
Temple Abyss Card Generator Script

This script generates custom Temple Abyss trading cards with AI-generated artwork.

Basic Usage:
    python api_call.py --api-key YOUR_API_KEY

Optional Parameters:
    --prompt "Your custom art description"    : Describe the artwork you want generated
    --negative-prompt "What to avoid"         : Describe what you don't want in the art
    --seed 123456789                         : Set random seed for reproducible results
    --n-samples 1                            : Number of images to generate (1-4)
    --use-rendered-art-image                 : Use pre-rendered art instead of generating new
    --rendered-art-image "url/to/image.png"  : URL of pre-rendered art to use
    --background-image "url/to/bg.png"       : Card background template URL
    --clan-icon "url/to/icon.png"            : Clan affiliation icon URL
    --rarity-icon "url/to/icon.png"          : Card rarity icon URL
    --aura-icon "url/to/icon.png"            : Aura type icon URL
    --init-image "url/to/image.png"          : Reference image for ControlNet guidance
    --card-name "Card Name"                  : Name of the card (default: "CARD_NAME")
    --trait "Card Trait"                     : Trait text (default: "TRAIT")
    --card-text "Card Description"           : Card effect description
    --rng-points "123"                       : Point value (default: "420")
    --controlnet-strength 0.8                : Strength of image guidance (0.0-1.0)
    --controlnet depth                       : Type of image guidance (depth/canny/etc)
    --lora "67a222bae707584b6d669623"      : Custom LoRA model ID to use
    --lora-strength 0.68                     : Strength of style effect (0.0-1.0)

Example:
    python api_call.py --api-key abc123 --card-name "Dragon" --trait "Ancient Beast" --card-text "Breathes fire on all enemies"

The script will generate the card artwork and compose it with the card template, saving the result to ./generated_images/
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

    def create_image(self, prompt):
        payload = {
            "tool": "temple_abyss",
            "args": {
                "n_samples": 1,
                "prompt": "Steve is the curmudgeonly manager of the Garden of Eden, japanese anime style, comic book dark fantasy style, thick thick thick bold linework, illustration, Steve, the dissapointed Manager of the garden of eden stares disapprovingly, obscure symbols glowing on the stone floor, shadows flickering around, candles illuminating the scene with warm light., the overall style of the artwork is moody, with a focus on texture and light, creating a sense of depth and mystery, serene mood, tritone tritone tritone, eerie, dark shadows",
                "negative_prompt": "wobly lines, arms, screen, feminine, girly, skulls, faces, demons, creatures, bodies, people, hands, watermark, text, nude, naked, nsfw, poorly drawn face, ugly, tiling, out of frame, blurry, blurred, grainy, signature, cut off, draft",
                "seed": 214748364,
                "use_rendered_art_image": False,
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
                "lora": "67a222bae707584b6d669623",
                "lora_strength": 0.68
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
    parser = argparse.ArgumentParser(description='Generate images using Eden AI API')
    parser.add_argument('--api-key', required=True, help='Your Eden AI API key')
    parser.add_argument('--prompt', default=None, help='Optional custom prompt for image generation')
    parser.add_argument('--negative-prompt', default=None, help='Optional custom negative prompt for image generation')
    parser.add_argument('--seed', type=int, default=123456789, help='Set random seed for reproducible results')
    parser.add_argument('--n-samples', type=int, default=1, choices=[1, 2, 3, 4], help='Number of images to generate')
    parser.add_argument('--use-rendered-art-image', action='store_true', help='Use pre-rendered art instead of generating new')
    parser.add_argument('--rendered-art-image', default=None, help='URL of pre-rendered art to use')
    parser.add_argument('--background-image', default=None, help='Card background template URL')
    parser.add_argument('--clan-icon', default=None, help='Clan affiliation icon URL')
    parser.add_argument('--rarity-icon', default=None, help='Card rarity icon URL')
    parser.add_argument('--aura-icon', default=None, help='Aura type icon URL')
    parser.add_argument('--init-image', default=None, help='Reference image for ControlNet guidance')
    parser.add_argument('--card-name', default="CARD_NAME", help='Name of the card')
    parser.add_argument('--trait', default="TRAIT", help='Trait of the card')
    parser.add_argument('--card-text', default="Card effect description goes here", help='Description text for the card')
    parser.add_argument('--rng-points', default="420", help='Point value for the card')
    parser.add_argument('--controlnet-strength', type=float, default=0.80, help='Strength of ControlNet guidance')
    parser.add_argument('--controlnet', default="depth", choices=['none', 'canny', 'depth', 'scribble', 'pose', 'threshold', 'lineart'], help='Type of ControlNet preprocessor')
    parser.add_argument('--lora', default="67a222bae707584b6d669623", help='Custom LoRA model ID to use')
    parser.add_argument('--lora-strength', type=float, default=0.68, help='Strength of the LoRA effect')
    args = parser.parse_args()
    
    client = EdenAIClient(args.api_key)
    
    # Use provided prompt or fall back to default
    prompt = args.prompt or """A captivating and vibrant illustration of a massive ancient temple of eyes, swirling dark clouds, purple sunset in the sky,
    pools of water reflecting rays of godly sunlight, stunning artwork"""
    
    try:
        task_id = client.create_image(prompt)
        print("Waiting for image generation to complete...")
        client.wait_for_completion(task_id)
        image_path = client.download_image(task_id)
        print(f"Process completed successfully! Image saved at: {image_path}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()