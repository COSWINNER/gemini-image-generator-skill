# Gemini Image Generator Skill

English | [简体中文](./README_CN.md)

A Claude Code Skill based on Gemini 3 Pro Image API, supporting text-to-image and image-to-image generation.

## Features

### Core Capabilities

- **Text-to-Image**: Generate high-quality images from natural language descriptions
- **Image-to-Image**: Modify, transform, or combine existing images
  - Face identity preservation
  - Pose transfer
  - Style transfer
  - Clothing transfer
  - Image editing and enhancement

### Unique Advantages

- **Ultra-High Resolution**: Supports 1K/2K/4K resolution tiers, up to 6336×2688 pixels
- **Multiple Aspect Ratios**: 10 aspect ratio options covering various use cases
- **Smart Interaction**: Claude automatically analyzes requirements and guides users through details
- **Structured Prompts**: Precise control over generation through JSON format
- **Flexible Deployment**: Supports custom API endpoints for proxy usage

### Use Cases

**Design Work**
- Website logo design
- Banner images
- Posters and promotional materials
- Social media graphics
- Product showcase images

**Content Creation**
- Article illustrations
- Cover images
- Avatars and personal branding
- Concept art

**Business Applications**
- Advertising materials
- E-commerce product images
- Brand visual design
- Presentation graphics

**Personal Entertainment**
- Desktop wallpapers
- Mobile wallpapers
- AI art creation
- Photo style conversion

## Supported Aspect Ratios and Resolutions

| Aspect Ratio | 1K Resolution | 2K Resolution | 4K Resolution |
|--------------|---------------|---------------|---------------|
| 1:1          | 1024×1024     | 2048×2048     | 4096×4096     |
| 2:3          | 848×1264      | 1696×2528     | 3392×5056     |
| 3:2          | 1264×848      | 2528×1696     | 5056×3392     |
| 3:4          | 896×1200      | 1792×2400     | 3584×4800     |
| 4:3          | 1200×896      | 2400×1792     | 4800×3584     |
| 4:5          | 928×1152      | 1856×2304     | 3712×4608     |
| 5:4          | 1152×928      | 2304×1856     | 4608×3712     |
| 9:16         | 768×1376      | 1536×2752     | 3072×5504     |
| 16:9         | 1376×768      | 2752×1536     | 5504×3072     |
| 21:9         | 1584×672      | 3168×1344     | 6336×2688     |

## Installation

### 1. Install Dependencies

```bash
pip install -q -U google-genai Pillow
```

### 2. Configure Environment Variables

```bash
export GEMINI_API_KEY="your-api-key-here"

# Optional: Custom API endpoint
export GEMINI_BASE_URL="https://your-proxy-url.com"
```

### 3. Install the Skill

Clone the repository, then copy the `gemini-image-generator` directory to your project's `.claude/skills/` directory:

```
your-project/
├── .claude/
│   └── skills/
│       └── gemini-image-generator/
│           ├── SKILL.md
│           ├── README.md
│           ├── scripts/
│           │   └── generate_image.py
│           └── references/
│               └── json_schema_reference.md
```

## Usage

### Using in Claude Code

After installation, there are two ways to invoke this Skill:

**Method 1: Explicit Invocation (Recommended)**

Use the `/gemini-image-generator` command to explicitly invoke the Skill:

```
/gemini-image-generator Generate an image of a sleeping cat
```

```
/gemini-image-generator Convert this photo ./photo.jpg to anime style
```

**Method 2: Natural Language Description**

Simply describe your image generation needs, and Claude will automatically recognize and invoke this Skill:

```
Generate a cyberpunk style city night scene
```

```
Convert this photo ./photo.jpg to anime style
```

Claude will automatically:
1. Analyze your requirements and ask for necessary details (aspect ratio, resolution, etc.)
2. Convert requirements into structured JSON format
3. Call the generation script to create the image

### Output Location

Generated images are saved by default in the `./generation-image/` directory with filename format `generated_YYYYMMDD_HHMMSS.png`.

## JSON Prompt Structure

For the complete JSON prompt structure, refer to `references/json_schema_reference.md`. Main fields include:

```json
{
  "user_intent": "Natural language description of the goal",
  "meta": {
    "aspect_ratio": "16:9",
    "image_size": "1K",
    "quality": "ultra_photorealistic"
  },
  "subject": [{
    "type": "person",
    "description": "Visual feature description",
    "pose": "Action description",
    "expression": "Expression"
  }],
  "scene": {
    "location": "Scene description",
    "time": "golden_hour",
    "lighting": {"type": "cinematic"}
  },
  "style_modifiers": {
    "medium": "photography",
    "aesthetic": ["cyberpunk"]
  }
}
```

## FAQ

| Issue | Solution |
|-------|----------|
| API Key not found | Ensure `GEMINI_API_KEY` environment variable is set |
| Image generation failed | Check if prompt violates content policy |
| Poor image quality | Adjust `meta.quality` and `meta.image_size` parameters |
| Wrong aspect ratio | Check if `meta.aspect_ratio` is a supported value |

## Directory Structure

```
gemini-image-generator/
├── SKILL.md                    # Skill definition file (read by Claude)
├── README.md                   # English documentation (this file)
├── README_CN.md                # Chinese documentation
├── scripts/
│   └── generate_image.py       # Image generation script
└── references/
    └── json_schema_reference.md # Complete JSON prompt reference
```

## License

MIT
