---
aliases: Stylize a video, Video Style Transfer, vid2vid_sdxl
---

# Stylize a video
![alt text](app/vid2vid_sdxl_opt.mp4)

Transform existing videos by applying artistic styles while preserving motion and shape. This tool uses advanced AI to reinterpret video content through the aesthetic lens of a reference style image.

## Overview

- Video style transfer based on reference images
- Motion and shape preservation from source video
- Adjustable style strength and motion control
- Support for looping animations

## Quick Start

1. Visit Eden Create: [Stylize a video](https://beta.eden.art/create/vid2vid_sdxl) tool
2. Upload your source video
3. Upload a style reference image
4. Click "Create"

See [API Reference](#api-reference) section below for API usage examples.

Ask an Eden agent to "Stylize a video".

## Basic Usage

Required inputs:
- Source video
- Style reference image

Optional settings:
- Processing resolution (640-1280px)
- Number of frames (16-264)
- Control strength (0-1.2)
- Diffusion framerate (8-12 fps)

## Technical Guidelines

### Resolution Settings
- Default: 896px
- Minimum: 640px
- Maximum: 1280px
- Higher resolutions produce better quality but increase processing time significantly

### Frame Processing
- Frame cap: 16-264 frames
- Output duration = frames ÷ 8 seconds (e.g., 24 frames = 3 seconds)
- Diffusion framerate: 8-12 fps
- Default framerate: 8 fps

## Best Practices for Inputs

### Video Input
- Keep source videos short (recommended 2-4 seconds)
- Ensure clear motion and good lighting
- Avoid rapid camera movements
- Use stable footage for best results

### Style Image
- Choose high-quality reference images
- Select images with clear artistic style
- Avoid cluttered or busy compositions

## Advanced Features

### Control Strength
- Range: 0.0-1.2
- Default: 0.5
- Low values (0.3-0.45): More creative freedom, better style adherence
- High values (0.55-0.65): Better source video preservation

### Looping Animation
- Enable closed loop for seamless animation
- Recommended for GIF-like content
- Ensures first and last frames match

### Diffusion Framerate Control
- 8 fps: Standard processing, longer output
- 12 fps: Better for fast motion preservation
- Affects RIFE interpolation quality

## Technical Details

### Processing Specifications
- Base model: SDXL
- Output type: Video
- Default resolution: 896px
- Frame interpolation: RIFE

### Limitations
- Maximum frame cap: 264 frames
- Maximum resolution: 1280px
- Processing time increases with resolution and frame count

## API Reference

### Endpoint
```bash
curl -X POST "https://api.eden.art/v2/tasks/create" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: YOUR_API_KEY" \
  -d '{
    "tool": "vid2vid_sdxl",
    "args": {
      "video": "https://edenartlab-stage-data.s3.amazonaws.com/b09ed23211a88017430bd687b1989dcd41f18222343fcd8f133f7cda489100b0.mp4",
      "image": "https://edenartlab-prod-data.s3.us-east-1.amazonaws.com/bb88e857586a358ce3f02f92911588207fbddeabff62a3d6a479517a646f053c.jpg",
      "resolution": 896,
      "frame_cap": 24,
      "control_strength": 0.5,
      "diffusion_framerate": 8,
      "closed_loop": false,
      "seed": 1234567890
    }
  }'
```

### Response Format
```json
{
  "task": {
    "_id": "task_12345",
    "createdAt": "2024-01-29T21:52:07.171578+00:00",
    "updatedAt": "2024-01-29T21:52:07.171608+00:00",
    "user": "user_id",
    "requester": "requester_id",
    "tool": "vid2vid_sdxl",
    "parent_tool": null,
    "output_type": "video",
    "args": {
      "video": "https://edenartlab-stage-data.s3.amazonaws.com/b09ed23211a88017430bd687b1989dcd41f18222343fcd8f133f7cda489100b0.mp4",
      "image": "https://edenartlab-prod-data.s3.us-east-1.amazonaws.com/bb88e857586a358ce3f02f92911588207fbddeabff62a3d6a479517a646f053c.jpg",
      "resolution": 896,
      "frame_cap": 24,
      "control_strength": 0.5,
      "diffusion_framerate": 8,
      "closed_loop": false,
      "seed": 1234567890
    },
    "mock": false,
    "cost": 48,
    "handler_id": "fc-xxxxx",
    "status": "pending",
    "error": null,
    "result": null,
    "performance": null
  }
}
```