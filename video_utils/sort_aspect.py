import os
import shutil
import argparse
import itertools
import time
from PIL import Image
from pathlib import Path
from tqdm import tqdm

import torch
import numpy as np
from torchvision.transforms import ToTensor, ToPILImage
import torch.nn.functional as F

# Check for CUDA availability
device = "cuda" if torch.cuda.is_available() else "cpu"

try:
    from einops import rearrange
except ImportError:
    print("Installing einops...")
    import subprocess
    subprocess.check_call(["pip", "install", "einops"])
    from einops import rearrange

try:
    from tsp_solver.greedy import solve_tsp
except ImportError:
    print("Installing tsp_solver2...")
    import subprocess
    subprocess.check_call(["pip", "install", "tsp_solver2"])
    from tsp_solver.greedy import solve_tsp

try:
    import lpips
    lpips_perceptor = lpips.LPIPS(net='alex').eval().to(device)
except ImportError:
    print("Installing lpips...")
    import subprocess
    subprocess.check_call(["pip", "install", "lpips"])
    import lpips
    lpips_perceptor = lpips.LPIPS(net='alex').eval().to(device)

# Constants for aspect ratio categorization
SQUARE_THRESHOLD = 0.1  # If width/height ratio is within this threshold of 1.0, consider it square

# Helper functions for image processing
def load_img(img_path, mode='RGB'):
    """Load an image from path and convert to specified mode."""
    try:
        img = Image.open(img_path).convert(mode)
        return img
    except Exception as e:
        print(f"Error loading image {img_path}: {e}")
        return None

def get_aspect_category(width, height):
    """Determine if an image is square, landscape, or portrait based on dimensions."""
    ratio = width / height
    if 1.0 - SQUARE_THRESHOLD <= ratio <= 1.0 + SQUARE_THRESHOLD:
        return "square"
    elif ratio > 1.0:
        return "landscape"
    else:
        return "portrait"

def get_centre_crop(img, aspect_ratio):
    """Create a center crop of the image with the specified aspect ratio."""
    h, w = np.array(img).shape[:2]
    if w/h > aspect_ratio:
        # crop width
        new_w = int(h * aspect_ratio)
        left = (w - new_w) // 2
        right = (w + new_w) // 2
        crop = img[:, left:right]
    else:
        # crop height
        new_h = int(w / aspect_ratio)
        top = (h - new_h) // 2
        bottom = (h + new_h) // 2
        crop = img[top:bottom, :]
    return crop

@torch.no_grad()
def resize_batch(images, target_w):
    """Resize a batch of images to a target width while preserving aspect ratio."""
    try:
        if len(images.shape) == 5:
            images = images.squeeze()

        if len(images.shape) == 3:
            images = images.unsqueeze(0)

        b, c, h, w = images.shape
        target_h = int(target_w * h / w)
        return F.interpolate(images, size=(target_h, target_w), mode='bilinear', align_corners=False)
    except Exception as e:
        raise RuntimeError(f"Error resizing batch of images: {images.shape}, {e}")

def get_uniformly_sized_crops(img_paths, target_n_pixels):
    """
    Given a list of images:
        - extract the best possible centre crop of same aspect ratio for all images
        - rescale these crops to have ~target_n_pixels
        - return resized images
    """
    # Load images
    print("Loading images...")
    imgs = []
    for path in tqdm(img_paths):
        try:
            img = load_img(path, 'RGB')
            if img is not None:
                imgs.append(np.array(img))
        except Exception as e:
            print(f"Error processing image {path}: {e}")
    
    if not imgs:
        print("No valid images found")
        return []
    
    # Get center crops at same aspect ratio
    print("Creating center crops at same aspect ratio...")
    aspect_ratios = [img.shape[1] / img.shape[0] for img in imgs]
    final_aspect_ratio = np.mean(aspect_ratios)
    crops = [get_centre_crop(img, final_aspect_ratio) for img in imgs]

    # Compute final w,h using final_aspect_ratio and target_n_pixels
    final_h = np.sqrt(target_n_pixels / final_aspect_ratio)
    final_w = final_h * final_aspect_ratio
    final_h, final_w = int(final_h), int(final_w)

    # Resize images
    print("Resizing images...")
    resized_imgs = []
    for img in tqdm(crops):
        resized_imgs.append(Image.fromarray(img).resize((final_w, final_h), Image.LANCZOS))   
    
    return resized_imgs

@torch.no_grad()
def perceptual_distance(batch_img1, batch_img2, resize_target_pixels_before_computing_lpips=768):
    """
    Returns perceptual distance between batch_img1 and batch_img2.
    This function assumes batch_img1 and batch_img2 are in the range [0, 1].
    By default, images are resized to a fixed resolution before computing the LPIPS score.
    """
    minv1, minv2 = batch_img1.min().item(), batch_img2.min().item()
    minv = min(minv1, minv2)
    if minv < 0:
        print("WARNING: perceptual_distance() assumes images are in [0,1] range.  minv1: %.3f | minv2: %.3f" % (minv1, minv2))

    if resize_target_pixels_before_computing_lpips > 0:
        batch_img1, batch_img2 = resize_batch(batch_img1, resize_target_pixels_before_computing_lpips), resize_batch(batch_img2, resize_target_pixels_before_computing_lpips)

    # LPIPS model requires images to be in range [-1, 1]:
    perceptual_distances = lpips_perceptor((2 * batch_img1) - 1, (2 * batch_img2) - 1).mean(dim=(1, 2, 3))

    return perceptual_distances

def load_images(directory, target_size):
    """Load images from a directory, crop and resize them to a uniform size."""
    images, image_paths = [], []
    valid_extensions = ('.png', '.jpg', '.jpeg', '.webp', '.bmp')
    
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath) and filename.lower().endswith(valid_extensions):
            image_paths.append(filepath)
    
    if not image_paths:
        print(f"No valid images found in {directory}")
        return []
    
    print("Loading and cropping all images to a uniform size...")
    images = get_uniformly_sized_crops(image_paths, target_size)

    # convert the images to tensors
    image_tensors = [ToTensor()(img).unsqueeze(0) for img in images]

    print(f"Loaded {len(images)} images from {directory}")
    return list(zip(image_paths, image_tensors))

def compute_pairwise_lpips(image_tensors, batch_size=4):
    """Compute pairwise LPIPS distances between all images."""
    pairwise_distances = {}
    num_combinations = len(image_tensors) * (len(image_tensors) - 1) // 2
    progress_bar = tqdm(total=num_combinations, desc="Computing pairwise LPIPS")
    
    # Create a list of image pairs
    image_pairs = list(itertools.combinations(image_tensors, 2))
    
    # Calculate the number of batches
    num_batches = len(image_pairs) // batch_size + (1 if len(image_pairs) % batch_size != 0 else 0)
    
    for batch_idx in range(num_batches):
        # Create batches of image pairs
        start_idx = batch_idx * batch_size
        end_idx = min((batch_idx + 1) * batch_size, len(image_pairs))
        batch_image_pairs = image_pairs[start_idx:end_idx]
        
        # Create tensor batches
        img1_batch = torch.stack([img1[1] for img1, img2 in batch_image_pairs], dim=0).to(device)
        img2_batch = torch.stack([img2[1] for img1, img2 in batch_image_pairs], dim=0).to(device)

        if len(batch_image_pairs) > 1:
            img1_batch = img1_batch.squeeze()
            img2_batch = img2_batch.squeeze()
        
        # Compute perceptual distances for the batch
        dists_batch = perceptual_distance(img1_batch, img2_batch)
        
        # Update the pairwise_distances dictionary
        for (img1, img2), dist in zip(batch_image_pairs, dists_batch):
            pairwise_distances[(img1[0], img2[0])] = dist.item()
            pairwise_distances[(img2[0], img1[0])] = dist.item()
            progress_bar.update(1)

    progress_bar.close()
    return pairwise_distances

def create_distance_matrix(pairwise_distances, filenames):
    """Create a distance matrix from pairwise distances."""
    num_images = len(filenames)
    distance_matrix = [[0 for _ in range(num_images)] for _ in range(num_images)]
    for i, img1 in enumerate(filenames):
        for j, img2 in enumerate(filenames):
            if i != j:
                distance_matrix[i][j] = pairwise_distances[(img1, img2)]
    return distance_matrix

def sort_images_visually(directory, target_n_pixels, optim_steps=1000, list_only=False, copy_metadata_files=False):
    """Sort images in a directory based on perceptual similarity."""
    outdir = os.path.join(directory, "reordered")
    
    # Check if 'reordered' directory already exists
    if os.path.exists(outdir):
        print(f"Reordered directory already exists at {outdir}. Skipping computation.")
        reordered_files = sorted(os.listdir(outdir))
        return [os.path.join(outdir, f) for f in reordered_files]

    paths_and_tensors = load_images(directory, target_n_pixels)
    
    if not paths_and_tensors:
        print(f"No valid images to sort in {directory}")
        return []
        
    filenames = [t[0] for t in paths_and_tensors]

    print(f"Computing pairwise perceptual distances for {len(filenames)} images. This may take a while..")
    start_time = time.time()
    pairwise_distances = compute_pairwise_lpips(paths_and_tensors)
    distance_matrix = create_distance_matrix(pairwise_distances, filenames)
    print(f"Finished computing pairwise distances in {time.time() - start_time:.2f} seconds")

    print("Solving traveling salesman problem...")
    start_time = time.time()
    path_indices = solve_tsp(distance_matrix, optim_steps=optim_steps)
    path = [filenames[idx] for idx in path_indices]
    print(f"Finished solving TSP in {time.time() - start_time:.2f} seconds")

    if list_only:
        print(f"List only mode: returning ordered list of file paths.")
        return path

    os.makedirs(outdir, exist_ok=True)

    print(f"Saving optimal visual walkthrough to {outdir}")
    for i, index in enumerate(path_indices):
        original_img_path = paths_and_tensors[index][0]
        image_pt_tensor = paths_and_tensors[index][1]
        new_name = f"{i:05d}_{os.path.basename(original_img_path)}"

        pil_image = ToPILImage()(image_pt_tensor.squeeze(0))
        pil_image.save(os.path.join(outdir, new_name))

        if copy_metadata_files:
            # Check for associated metadata files
            base, _ = os.path.splitext(original_img_path)
            json_filepath = base + ".json"
            if os.path.exists(json_filepath):
                new_json_name = os.path.splitext(new_name)[0] + ".json"
                shutil.copy(json_filepath, os.path.join(outdir, new_json_name))

    print(f"\nAll done! ---> {len(path_indices)} reordered images saved to {outdir}")
    return [os.path.join(outdir, f) for f in sorted(os.listdir(outdir))]

def categorize_images(input_dir, output_base_dir, valid_extensions=('.png', '.jpg', '.jpeg', '.webp', '.bmp')):
    """
    Categorize images from input_dir into square, landscape, and portrait categories
    and save them to respective subdirectories in output_base_dir.
    """
    # Create category directories
    categories = ["square", "landscape", "portrait"]
    category_dirs = {}
    
    for category in categories:
        category_dir = os.path.join(output_base_dir, category)
        os.makedirs(category_dir, exist_ok=True)
        category_dirs[category] = category_dir
    
    # Process all images in the input directory
    processed_count = 0
    categorized = {"square": 0, "landscape": 0, "portrait": 0}
    
    for filename in os.listdir(input_dir):
        filepath = os.path.join(input_dir, filename)
        
        # Skip if not a file or not an image with valid extension
        if not os.path.isfile(filepath) or not filename.lower().endswith(valid_extensions):
            continue
        
        try:
            # Open image and get dimensions
            img = Image.open(filepath)
            width, height = img.size
            
            # Determine category
            category = get_aspect_category(width, height)
            
            # Copy to appropriate category directory
            dest_path = os.path.join(category_dirs[category], filename)
            shutil.copy2(filepath, dest_path)
            
            processed_count += 1
            categorized[category] += 1
            
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
    
    print(f"Processed {processed_count} images:")
    print(f"  - Square: {categorized['square']}")
    print(f"  - Landscape: {categorized['landscape']}")
    print(f"  - Portrait: {categorized['portrait']}")
    
    return category_dirs

def main():
    parser = argparse.ArgumentParser(description="Categorize images by aspect ratio and sort them visually")
    parser.add_argument("input_dir", type=str, help="Directory containing images to process")
    parser.add_argument("--output_dir", type=str, help="Base output directory for categorized images (default: input_dir/categorized)", default=None)
    parser.add_argument("--target_pixels", type=int, default=1200*1200, help="Target number of pixels for LPIPS comparison")
    parser.add_argument("--optim_steps", type=int, default=1000, help="Number of TSP optimization steps")
    parser.add_argument("--copy_metadata", action="store_true", help="Copy associated JSON metadata files if they exist")
    parser.add_argument("--skip_sort", action="store_true", help="Skip visual sorting step after categorization")
    
    args = parser.parse_args()
    
    input_dir = args.input_dir
    if not os.path.isdir(input_dir):
        print(f"Error: Input directory '{input_dir}' does not exist")
        return
    
    # Set default output dir if not specified
    output_dir = args.output_dir or os.path.join(input_dir, "categorized")
    
    print(f"Categorizing images from {input_dir} by aspect ratio...")
    category_dirs = categorize_images(input_dir, output_dir)
    
    if args.skip_sort:
        print("Skipping visual sorting step as requested")
        return
    
    # Sort each category directory
    for category, directory in category_dirs.items():
        # Check if directory has any images
        image_count = sum(1 for f in os.listdir(directory) 
                         if os.path.isfile(os.path.join(directory, f)) 
                         and f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.bmp')))
        
        if image_count > 1:
            print(f"\nVisually sorting {image_count} {category} images...")
            sort_images_visually(
                directory, 
                args.target_pixels, 
                args.optim_steps, 
                list_only=False, 
                copy_metadata_files=args.copy_metadata
            )
        else:
            print(f"\nSkipping visual sorting for {category} category (insufficient images: {image_count})")
    
    print("\nAll processing complete!")

if __name__ == "__main__":
    main() 