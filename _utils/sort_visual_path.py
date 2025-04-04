import os, shutil
import itertools
import time
import argparse
from PIL import Image

import torch
import numpy as np
from torchvision.transforms import ToTensor, ToPILImage
import torch.nn.functional as F
from tqdm import tqdm

global device
device = "cuda" if torch.cuda.is_available() else "cpu"

## pip install einops
from einops import rearrange

## python -m pip install tsp_solver2
from tsp_solver.greedy import solve_tsp

## pip install lpips
import lpips
lpips_perceptor = lpips.LPIPS(net='alex').eval().to(device)    # lpips model options: 'squeeze', 'vgg', 'alex'

################# helper functions #####################

def load_img(img_path, mode='RGB'):
    try:
        img = Image.open(img_path).convert(mode)
        return img
    except:
        print(f"Error loading image: {img_path}")
        return None

def get_centre_crop(img, aspect_ratio):
    h, w = np.array(img).shape[:2]
    if w/h > aspect_ratio:
        # crop width:
        new_w = int(h * aspect_ratio)
        left = (w - new_w) // 2
        right = (w + new_w) // 2
        crop = img[:, left:right]
    else:
        # crop height:
        new_h = int(w / aspect_ratio)
        top = (h - new_h) // 2
        bottom = (h + new_h) // 2
        crop = img[top:bottom, :]
    return crop

@torch.no_grad()
def resize_batch(images, target_w):
    try:
        if len(images.shape) == 5:
            images = images.squeeze()

        if len(images.shape) == 3:
            images = images.unsqueeze(0)

        b,c,h,w = images.shape
        target_h = int(target_w * h / w)
        return F.interpolate(images, size=(target_h, target_w), mode='bilinear', align_corners=False)
    except:
        raise(f"Error resizing batch of images: {images.shape}")


def prep_pt_img_for_clip(pt_img, clip_preprocessor):
    # This is a bit hacky and can be optimized, but turn the PyTorch img back into a PIL image, since that's what the preprocessor expects:
    pt_img = 255. * rearrange(pt_img, 'b c h w -> b h w c')
    pil_img = Image.fromarray(pt_img.squeeze().cpu().numpy().astype(np.uint8))

    # now, preprocess the image with the CLIP preprocessor:
    clip_img = clip_preprocessor(images=pil_img, return_tensors="pt")["pixel_values"].float().to(device)
    return clip_img

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
            imgs.append(np.array(load_img(path, 'RGB')))
        except:
            print(f"Error loading image: {path}")
    
    # Get center crops at same aspect ratio
    print("Creating center crops at same aspect ratio...")
    aspect_ratios = [img.shape[1] / img.shape[0] for img in imgs]
    final_aspect_ratio = np.mean(aspect_ratios)
    crops = [get_centre_crop(img, final_aspect_ratio) for img in imgs]

    # Compute final w,h using final_aspect_ratio and target_n_pixels:
    final_h = np.sqrt(target_n_pixels / final_aspect_ratio)
    final_w = final_h * final_aspect_ratio
    final_h, final_w = int(final_h), int(final_w)

    # Resize images
    print("Resizing images...")
    resized_imgs = []
    for img in tqdm(crops):
        resized_imgs.append(Image.fromarray(img).resize((final_w, final_h), Image.LANCZOS))   
    
    return resized_imgs

################################################################################


def load_images(directory, target_size):
    images, image_paths = [], []
    valid_extensions = ('.png', '.jpg', '.jpeg')  # Define valid image extensions
    for filename in os.listdir(directory):
        if filename.lower().endswith(valid_extensions):
            image_paths.append(os.path.join(directory, filename))
        else:
            print(f"Ignoring non-image file: {filename}")
    
    print("Loading and cropping all images to a uniform size...")
    images = get_uniformly_sized_crops(image_paths, target_size)

    # convert the images to tensors
    image_tensors = [ToTensor()(img).unsqueeze(0) for img in images]

    print(f"Loaded {len(images)} images from {directory}")
    return list(zip(image_paths, image_tensors))


def compute_pairwise_lpips(image_tensors, batch_size=4):
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
    num_images = len(filenames)
    distance_matrix = [[0 for _ in range(num_images)] for _ in range(num_images)]
    for i, img1 in enumerate(filenames):
        for j, img2 in enumerate(filenames):
            if i != j:
                distance_matrix[i][j] = pairwise_distances[(img1, img2)]
    return distance_matrix


@torch.no_grad()
def main(directory, target_n_pixels, optim_steps=1000, list_only=True, copy_metadata_files=False, image_extensions=".jpg,.png,.jpeg"):
    outdir = os.path.join(directory, "reordered")
    
    # Check if 'reordered' directory already exists
    if os.path.exists(outdir):
        print(f"Reordered directory already exists at {outdir}. Skipping computation.")
        reordered_files = sorted(os.listdir(outdir))
        return [os.path.join(outdir, f) for f in reordered_files]

    paths_and_tensors = load_images(directory, target_n_pixels)
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
    print(f"!!! path: {path}")

    if list_only:
        print(f"List only mode: returning ordered list of file paths. {path}")
        return path

    os.makedirs(outdir, exist_ok=True)

    print(f"Saving optimal visual walkthrough to {outdir}")
    for i, index in enumerate(path_indices):
        original_img_path = paths_and_tensors[index][0]
        image_pt_tensor = paths_and_tensors[index][1]
        new_name = f"{i:05d}_{os.path.basename(original_img_path)}.jpg"

        pil_image = ToPILImage()(image_pt_tensor.squeeze(0))
        pil_image.save(os.path.join(outdir, new_name))

        if copy_metadata_files:
            # replace extension with .json
            json_filepath = original_img_path
            for ext in image_extensions.split(','):
                json_filepath = json_filepath.replace(ext, ".json")

            if os.path.exists(json_filepath):
                print(f"Copying {json_filepath} to {outdir}")
                shutil.copy(json_filepath, os.path.join(outdir, new_name.replace(".jpg", ".json")))

    print(f"\nAll done! ---> {len(path_indices)} reordered images saved to {outdir}")
    return [os.path.join(outdir, f) for f in sorted(os.listdir(outdir))]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute shortest visual path through images in a directory")
    parser.add_argument("directory", type=str, help="Directory containing images")
    parser.add_argument("--optim_steps", type=int, default=1000, help="Number of tsp optimisation steps to run (will try to optimize the greedy tsp solution)")
    parser.add_argument("--image_extensions", type=str, default=".jpg,.png,.jpeg", help="Comma separated list of image extensions to consider")
    parser.add_argument("--copy_metadata_files", action="store_true", help="If set, will copy any metadata files (e.g. .json) to the output directory")
    parser.add_argument("--target_n_pixels", type=int, default=1200*1920, help="Target number of pixels for output images (script will resize and crop images)")
    parser.add_argument("--list_only", action="store_true", default=True, help="If set, only returns an ordered list of file paths without saving files")
    args = parser.parse_args()
    main(args.directory, args.target_n_pixels, args.optim_steps, args.list_only, args.copy_metadata_files, args.image_extensions)