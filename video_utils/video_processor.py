import os
import argparse
import random
from pathlib import Path
from typing import List, Tuple

try:
    from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips, CompositeVideoClip
    import numpy as np
except ImportError:
    print("Required packages not found. Installing...")
    import subprocess
    subprocess.check_call(["pip", "install", "moviepy", "numpy"])
    from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips, CompositeVideoClip
    import numpy as np


def is_video_file(filename: str) -> bool:
    """Check if a file is a video based on its extension."""
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm']
    return os.path.splitext(filename)[1].lower() in video_extensions


def is_image_file(filename: str) -> bool:
    """Check if a file is an image based on its extension."""
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif', '.webp']
    return os.path.splitext(filename)[1].lower() in image_extensions


def get_media_files(folder_path: str) -> List[str]:
    """Get all video and image files from a folder."""
    media_files = []
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if os.path.isfile(filepath) and (is_video_file(filename) or is_image_file(filename)):
            media_files.append(filepath)
    return media_files


def get_target_resolution(first_file: str) -> Tuple[int, int]:
    """Get the resolution from the first media file."""
    if is_video_file(first_file):
        with VideoFileClip(first_file) as clip:
            return clip.size
    elif is_image_file(first_file):
        with ImageClip(first_file) as clip:
            return clip.size
    raise ValueError(f"File {first_file} is neither a video nor an image")


def process_video(filepath: str, target_width: int, target_height: int, pingpong: bool) -> VideoFileClip:
    """Process a video file to match the target resolution and apply pingpong if needed."""
    clip = VideoFileClip(filepath)
    
    # Resize video to match target resolution
    if clip.size != (target_width, target_height):
        clip = clip.resize(width=target_width, height=target_height)
    
    # Apply pingpong effect if requested
    if pingpong:
        reversed_clip = clip.copy().fx(lambda c: c.time_mirror())
        clip = concatenate_videoclips([clip, reversed_clip])
    
    return clip


def process_image(filepath: str, target_width: int, target_height: int, duration: float) -> VideoFileClip:
    """Convert an image to a video clip with the specified duration and resolution."""
    clip = ImageClip(filepath, duration=duration)
    
    # Resize image to match target resolution
    if clip.size != (target_width, target_height):
        clip = clip.resize(width=target_width, height=target_height)
    
    return clip


def apply_crossfade(clips: List[VideoFileClip], crossfade_duration: float) -> VideoFileClip:
    """Apply crossfade transitions between video clips."""
    if not clips:
        raise ValueError("No clips provided")
    
    if len(clips) == 1:
        return clips[0]
    
    # Ensure crossfade duration isn't longer than any clip
    min_duration = min(clip.duration for clip in clips)
    crossfade_duration = min(crossfade_duration, min_duration / 2)
    
    final_clips = []
    for i, clip in enumerate(clips):
        if i == 0:  # First clip
            final_clips.append(clip.crossfadeout(crossfade_duration))
        elif i == len(clips) - 1:  # Last clip
            final_clips.append(clip.crossfadein(crossfade_duration))
        else:  # Middle clips
            final_clips.append(clip.crossfadein(crossfade_duration).crossfadeout(crossfade_duration))
    
    return concatenate_videoclips(final_clips, method="compose")


def apply_ken_burns(video_clip: VideoFileClip) -> VideoFileClip:
    """Apply a subtle Ken Burns effect to the concatenated video."""
    duration = video_clip.duration
    
    # Parameters for the Ken Burns effect
    zoom_range = (1.0, 1.05)  # Subtle zoom
    max_pan = 0.05  # Maximum pan as a fraction of image size
    
    def get_random_movement():
        # Generate random but smooth movement parameters
        zoom_start = random.uniform(*zoom_range)
        zoom_end = random.uniform(*zoom_range)
        
        # Ensure we don't zoom out beyond original size
        if zoom_start > zoom_end:
            zoom_start, zoom_end = zoom_end, zoom_start
        
        # Random pan direction that won't reveal borders
        pan_x = random.uniform(-max_pan, max_pan)
        pan_y = random.uniform(-max_pan, max_pan)
        
        return zoom_start, zoom_end, pan_x, pan_y
    
    zoom_start, zoom_end, pan_x, pan_y = get_random_movement()
    
    def ken_burns_transform(get_frame, t):
        # Apply smooth easing
        progress = 0.5 - 0.5 * np.cos(np.pi * t / duration)
        
        # Calculate current zoom and position
        zoom = zoom_start + progress * (zoom_end - zoom_start)
        x_shift = pan_x * progress * video_clip.w
        y_shift = pan_y * progress * video_clip.h
        
        # Get the frame at the current time
        frame = get_frame(t)
        
        # Create a zoomed frame
        h, w = frame.shape[:2]
        zoomed_h, zoomed_w = int(h * zoom), int(w * zoom)
        
        # Crop the frame to avoid showing borders
        crop_x = int(min(abs(x_shift), (zoomed_w - w) / 2))
        crop_y = int(min(abs(y_shift), (zoomed_h - h) / 2))
        
        # Resize with zoom
        zoomed_frame = video_clip.fx(lambda clip: clip.resize(zoom)).get_frame(t)
        
        # Apply pan by cropping the zoomed frame
        result = zoomed_frame[
            crop_y:crop_y + h,
            crop_x:crop_x + w
        ]
        
        return result
    
    return video_clip.fl(ken_burns_transform)


def process_folder(
    folder_path: str,
    output_path: str,
    image_duration: float = 5.0,
    pingpong: bool = False,
    crossfade_duration: float = 2.0,
    apply_kb_effect: bool = False
):
    """Process all media files in a folder and create a concatenated video."""
    media_files = get_media_files(folder_path)
    
    if not media_files:
        print(f"No media files found in {folder_path}")
        return
    
    print(f"Found {len(media_files)} media files")
    
    # Get target resolution from the first file
    target_width, target_height = get_target_resolution(media_files[0])
    print(f"Target resolution: {target_width}x{target_height}")
    
    # Process each media file
    processed_clips = []
    for filepath in media_files:
        print(f"Processing {os.path.basename(filepath)}")
        
        if is_video_file(filepath):
            clip = process_video(filepath, target_width, target_height, pingpong)
        elif is_image_file(filepath):
            clip = process_image(filepath, target_width, target_height, image_duration)
        else:
            continue
        
        processed_clips.append(clip)
    
    # Concatenate all clips with crossfade transitions
    print("Applying crossfades and concatenating clips...")
    final_video = apply_crossfade(processed_clips, crossfade_duration)
    
    # Save the concatenated video
    output_file = os.path.join(output_path, "concatenated_video.mp4")
    print(f"Saving concatenated video to {output_file}")
    final_video.write_videofile(output_file, codec="libx264", audio_codec="aac")
    
    # Apply Ken Burns effect if requested
    if apply_kb_effect:
        print("Applying Ken Burns effect...")
        kb_output_file = os.path.join(output_path, "kenburns_video.mp4")
        kb_video = apply_ken_burns(final_video)
        print(f"Saving Ken Burns video to {kb_output_file}")
        kb_video.write_videofile(kb_output_file, codec="libx264", audio_codec="aac")
    
    # Close all clips to release resources
    for clip in processed_clips:
        clip.close()
    final_video.close()
    
    print("Processing complete!")


def main():
    parser = argparse.ArgumentParser(description="Process a folder of videos and images.")
    parser.add_argument("folder", help="Path to the folder containing videos and images")
    parser.add_argument("--output", "-o", default=".", help="Path to save the output videos (default: current directory)")
    parser.add_argument("--image-duration", "-d", type=float, default=5.0, help="Duration in seconds for image clips (default: 5.0)")
    parser.add_argument("--pingpong", "-p", action="store_true", help="Apply pingpong effect to videos (default: False)")
    parser.add_argument("--crossfade", "-c", type=float, default=2.0, help="Duration in seconds for crossfade transitions (default: 2.0)")
    parser.add_argument("--kenburns", "-k", action="store_true", help="Apply Ken Burns effect to the final video (default: False)")
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)
    
    process_folder(
        args.folder,
        args.output,
        args.image_duration,
        args.pingpong,
        args.crossfade,
        args.kenburns
    )


if __name__ == "__main__":
    main() 