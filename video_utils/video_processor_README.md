# Video Processor

This script processes a folder of videos and images, creating a concatenated video with various effects.

## Features

- Automatically resizes all videos and images to match the resolution of the first media file
- Converts images to videos with a configurable duration
- Optional pingpong effect for videos (play forward then backward)
- Concatenates all media with configurable crossfade transitions
- Optional Ken Burns effect (subtle pan and zoom) as a post-processing step

## Requirements

- Python 3.6+
- Required packages (automatically installed by the script if missing):
  - moviepy
  - numpy

## Installation

No installation is required. Just make sure you have Python installed on your system.

## Usage

```bash
python video_processor.py [folder] [options]
```

### Arguments

- `folder`: Path to the folder containing videos and images (required)

### Options

- `--output`, `-o`: Path to save the output videos (default: current directory)
- `--image-duration`, `-d`: Duration in seconds for image clips (default: 5.0)
- `--pingpong`, `-p`: Apply pingpong effect to videos (default: False)
- `--crossfade`, `-c`: Duration in seconds for crossfade transitions (default: 2.0)
- `--kenburns`, `-k`: Apply Ken Burns effect to the final video (default: False)

## Examples

Process all media in a folder with default settings:
```bash
python video_processor.py C:/path/to/media
```

Process with custom settings:
```bash
python video_processor.py C:/path/to/media --output C:/path/to/output --image-duration 3 --pingpong --crossfade 1.5 --kenburns
```

## Output

The script generates:
1. `concatenated_video.mp4`: The main output with all media concatenated with crossfades
2. `kenburns_video.mp4`: (Optional) The same video with Ken Burns effect applied

## Notes

- The script determines the target resolution from the first media file found in the folder
- All videos and images are resized to match this resolution
- The Ken Burns effect is a subtle pan and zoom that avoids showing black borders
- For best results, ensure your media files have similar aspect ratios 