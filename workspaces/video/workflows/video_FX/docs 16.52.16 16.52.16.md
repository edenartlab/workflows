---
aliases: 
- AI Video Effects
- Video AI Effects
- AI Video Stylization
- Video Style Transfer
---

# AI Video Effects
![alt text](https://edenartlab-prod-data.s3.us-east-1.amazonaws.com/app/video_FX_thumbnail.mp4)

Apply sophisticated AI-powered visual effects to specific regions of a video using advanced depth, edge, and luminance-based masking techniques. This tool allows creative stylization of video content with granular control over effect application.

## Overview

- Region-based video stylization
- Depth-aware AI effect targeting
- Custom style image application
- Fine-grained effect strength control
- Preserves original video structure

## Quick Start

1. Visit Eden Create: [AI video effects](https://beta.eden.art/create/video_FX) tool
2. Upload an input video
3. Select a style image
4. Configure masking parameters
5. Click "Create"

See [API Reference](#api-reference) for programmatic usage.

Ask an Eden agent to "AI video effects".

## Basic Usage

Required Inputs:
- Input video
- Style image
- Number of frames
- Processing resolution

## Technical Guidelines

### Processing Parameters
- Resolution Range: 768-1280px
- Recommended: 1024px
- Frame Count: 16-512 frames
- Typical Output: 3-6 seconds

## Advanced Features

### Depth-Based Masking
Control AI effect strength based on object distance from camera
- `close_strength`: Target objects near camera
- Range: -1.0 to 1.0
- Negative values stylize distant objects

### Edge and Texture Targeting
Modify effect application on textured regions
- `edge_strength`: Control stylization on edges
- Recommended: Negative values for flat regions

### Luminance Masking
Apply effects based on image brightness
- `luminance_strength`: Target bright/dark regions
- Range: -1.0 to 1.0

## Tips for Best Results

### Technical Considerations
- Use consistent style images
- Experiment with masking parameters
- Start with low effect strengths
- Preview and iterate

### Input Optimization
- Choose high-contrast style images
- Use videos with clear depth variations
- Avoid extremely complex source videos

## Technical Details

### Base Technology
- ComfyUI-based video processing
- Multi-stage masked stylization
- Depth-aware region detection

### Default Parameters
- Minimum Denoise: 0.0
- Maximum Denoise: 0.55
- Default Resolution: 1024px
- Default Frames: 24

### Limitations
- Max Resolution: 1280px
- Video Length: ~3-6 seconds
- Cannot replace objects completely

## Common Issues and Solutions

1. Artifact-heavy outputs
   - Reduce `max_denoise`
   - Choose simpler style images

2. Unexpected stylization
   - Fine-tune masking parameters
   - Adjust `close_strength`, `edge_strength`

## API Reference

### Endpoint
`https://api.eden.art/v2/tasks/create`

### Request Headers
- `Content-Type: application/json`
- `X-Api-Key: YOUR_API_KEY`

### Example Request
```bash
curl -X POST "https://api.eden.art/v2/tasks/create" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: YOUR_API_KEY" \
  -d '{
    "tool": "video_FX",
    "args": {
      "video": "https://edenartlab-stage-data.s3.amazonaws.com/b09ed23211a88017430bd687b1989dcd41f18222343fcd8f133f7cda489100b0.mp4",
      "style_image": "https://edenartlab-prod-data.s3.us-east-1.amazonaws.com/bb88e857586a358ce3f02f92911588207fbddeabff62a3d6a479517a646f053c.jpg",
      "resolution": 1024,
      "n_frames": 24,
      "close_strength": -0.1,
      "edge_strength": -0.2,
      "luminance_strength": 0.0,
      "max_denoise": 0.55,
      "min_denoise": 0.0
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
    "tool": "video_FX",
    "parent_tool": null,
    "output_type": "video",
    "args": {
      "video": "https://edenartlab-stage-data.s3.amazonaws.com/b09ed23211a88017430bd687b1989dcd41f18222343fcd8f133f7cda489100b0.mp4",
      "style_image": "https://edenartlab-prod-data.s3.us-east-1.amazonaws.com/bb88e857586a358ce3f02f92911588207fbddeabff62a3d6a479517a646f053c.jpg",
      "resolution": 1024,
      "n_frames": 24,
      "close_strength": -0.1,
      "edge_strength": -0.2,
      "luminance_strength": 0.0,
      "max_denoise": 0.55,
      "min_denoise": 0.0
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