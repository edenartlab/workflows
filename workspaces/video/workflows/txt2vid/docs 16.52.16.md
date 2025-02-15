---
aliases: Create a video from text, Text to Video Generation, txt2vid
---

# Create a video from text
![alt text](app/txt2vid_lora_opt.mp4)

Generate creative, abstract text-driven animations. This tool converts text descriptions into fluid video sequences with customizable motion and looping capabilities.

## Overview

- Text-to-video generation
- Adjustable motion strength and frame count
- Seamless loop option
- Custom resolution support

## Quick Start

1. Visit Eden Create: [Create a video from text](https://beta.eden.art/create/txt2vid) tool
2. Enter your descriptive prompt
3. Adjust video settings if needed
4. Click "Create"

See [API Reference](#api-reference) section below for API usage examples.

Ask an Eden agent to "Create a video from text".

## Basic Usage

Required inputs:
- Text prompt describing the desired video

Optional settings:
- Number of frames (24-128)
- Motion strength (0.7-1.3)
- Resolution (512-2048px)
- Closed loop option
- Random seed

## Technical Guidelines

### Resolution Options
- Default: 1024x1024
- Width range: 512-2048px
- Height range: 512-2048px
- Common ratios:
  - 16:9 (2048x1152)
  - 3:2 (1782x1024)
  - 1:1 (1024x1024)
  - 2:3 (1024x1782)
  - 9:16 (1152x2048)

### Video Settings
- Frames: 24-128 (default: 64)
- Video length = frames/12 seconds
- Motion strength: 0.7-1.3 (default: 1.1)

## Best Practices

### Input Optimization
- Use clear, descriptive prompts
- Specify key visual elements
- Indicate desired motion type

### Technical Considerations
- Higher frame counts create longer videos
- Lower motion strength for subtle movements
- Higher motion strength for dynamic scenes

## API Reference

### Endpoint
`POST https://api.eden.art/v2/tasks/create`

### Headers
```
Content-Type: application/json
X-Api-Key: YOUR_API_KEY
```

### Basic Request
```bash
curl -X POST "https://api.eden.art/v2/tasks/create" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: YOUR_API_KEY" \
  -d '{
    "tool": "txt2vid",
    "args": {
      "prompt": "A train passing by a bridge",
      "n_frames": 128,
      "seed": 99
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
    "tool": "txt2vid",
    "parent_tool": null,
    "output_type": "video",
    "args": {
      "prompt": "A train passing by a bridge",
      "n_frames": 128,
      "width": 1024,
      "height": 1024,
      "motion_strength": 1.1,
      "closed_loop": false,
      "seed": 99
    },
    "mock": false,
    "cost": 64,
    "handler_id": "fc-xxxxx",
    "status": "pending",
    "error": null,
    "result": null,
    "performance": null
  }
}
```

## Common Issues and Solutions

### Video Length
**Issue**: Video too short/long  
**Solution**: Adjust n_frames (frames/12 = seconds)

### Motion Issues
**Issue**: Too much/little movement  
**Solution**: Adjust motion_strength (0.7-1.3)

### Loop Problems
**Issue**: Visible seam in loop  
**Solution**: Enable closed_loop parameter