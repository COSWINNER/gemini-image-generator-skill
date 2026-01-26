# Gemini Image Generator Skill

English | [简体中文](./README_CN.md)

A Claude Code Skill based on Gemini 3 Pro Image API, supporting text-to-image and image-to-image generation across multiple creative domains.

## Features

### Core Capabilities

**Multi-Domain Support**
- **Photography**: Portraits, landscapes, scenes with virtual camera settings and lighting control
- **Graphic Design**: Posters, logos, business cards, social media graphics, banners
- **UI Design**: Mobile app screens, dashboards, landing pages, settings panels

**Generation Modes**
- **Text-to-Image**: Generate high-quality images from natural language descriptions
- **Image-to-Image**: Modify, transform, or combine existing images
  - Full image transform: Face identity, pose transfer, style transfer, clothing transfer
  - **Precision Edit Mode (partial_edit)**: Local precise modifications with multiple edit commands
  - **Hybrid Mode**: Reference images + local edits combined

### Unique Advantages

- **Multi-Domain Schema**: Structured JSON prompts tailored for photography, graphic design, and UI design
- **Ultra-High Resolution**: Supports 1K/2K/4K resolution tiers, up to 6336×2688 pixels
- **Multiple Aspect Ratios**: 10 aspect ratio options covering various use cases
- **Smart Interaction**: Claude automatically analyzes requirements and guides users through details
- **Flexible Deployment**: Supports custom API endpoints for proxy usage

### Use Cases

**Photography**
- Professional portraits and headshots
- Landscape and scenery photography
- Product photography with studio lighting
- Artistic scenes with specific camera settings

**Graphic Design**
- Website logo design
- Event posters and flyers
- Business cards and branding materials
- Social media graphics and banners
- Infographic design

**UI/UX Design**
- Mobile app screen mockups
- Dashboard and data visualization interfaces
- Landing page designs
- Settings and configuration panels
- Component library design

**Content Creation**
- Article illustrations
- Cover images
- Avatars and personal branding
- Concept art

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
pip install -q -U google-genai Pillow python-dotenv
```

### 2. Configure Environment Variables

**Method 1: Using .env file (Recommended)**

Copy the example file and configure:

```bash
cp .env.example .env
```

Edit `.env` with your values:

```bash
GEMINI_API_KEY=your-api-key-here
# GEMINI_BASE_URL=https://your-proxy-url.com
# GEMINI_MODEL=gemini-3-pro-image-preview
```

**Method 2: Using system environment variables**

```bash
export GEMINI_API_KEY="your-api-key-here"

# Optional: Custom API endpoint
export GEMINI_BASE_URL="https://your-proxy-url.com"

# Optional: Custom model
export GEMINI_MODEL="gemini-3-pro-image-preview"
```

> **Note**: Configuration priority is `.env > system environment variables > default values`

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

For the complete JSON prompt structure, refer to the documents in `references/`:
- `json_schema_t2i_reference.md` - Complete Text-to-Image reference
- `json_schema_i2i_reference.md` - Complete Image-to-Image reference (includes Precision Edit Mode)

The schema supports three creative domains:

### Photography (Default)

```json
{
  "user_intent": "A cyberpunk warrior standing in a neon-lit alley",
  "meta": {
    "domain": "photography",
    "aspect_ratio": "16:9",
    "quality": "ultra_photorealistic"
  },
  "subject": [{
    "type": "cyborg",
    "description": "young hacker with cybernetic eye implant"
  }],
  "scene": {
    "location": "cyberpunk alley",
    "lighting": {"type": "neon_lights", "direction": "rim_light"}
  },
  "style_modifiers": {
    "aesthetic": ["cyberpunk", "noir"]
  }
}
```

### Graphic Design

```json
{
  "user_intent": "Summer sale poster with 50% off promotion",
  "meta": {
    "domain": "graphic_design",
    "aspect_ratio": "3:4",
    "quality": "ultra_photorealistic"
  },
  "graphic_design": {
    "design_type": "poster",
    "layout": {
      "grid_system": "hierarchical",
      "alignment": "center_aligned",
      "spacing": "generous_whitespace"
    },
    "color_scheme": {
      "palette_type": "vibrant",
      "primary_color": "tropical orange",
      "secondary_color": "sky blue"
    },
    "elements": [
      {"type": "headline", "content": "SUMMER SALE", "placement": "top_center"},
      {"type": "headline", "content": "50% OFF", "placement": "center"},
      {"type": "cta_button", "content": "SHOP NOW", "placement": "bottom_center"}
    ],
    "visual_style": {
      "mood": "energetic",
      "texture": "smooth"
    }
  }
}
```

### UI Design

```json
{
  "user_intent": "Modern dark mode analytics dashboard",
  "meta": {
    "domain": "ui_design",
    "aspect_ratio": "16:9"
  },
  "ui_design": {
    "component_type": "dashboard",
    "layout": {"structure": "grid", "columns": 3, "spacing": "comfortable"},
    "components": [
      {"type": "card", "variant": "primary"},
      {"type": "chart", "variant": "primary"},
      {"type": "sidebar", "variant": "secondary"}
    ],
    "color_system": {
      "mode": "dark_mode",
      "primary": "#6366f1",
      "background": "#0f172a"
    },
    "styling": {
      "border_radius": "medium_rounded",
      "shadow": "subtle_elevation"
    }
  }
}
```

### Precision Edit Mode

Local precise modifications with multiple edit commands:

```json
{
  "user_intent": "Change model's dress to red, make expression smiling",
  "meta": {"aspect_ratio": "3:4"},
  "input_image": {
    "path": "./portrait.jpg",
    "usage_type": "partial_edit",
    "strength": 0.92
  },
  "edits": {
    "clothing": {
      "edits": [{"target": "color", "action": "change_to", "value": "red"}]
    },
    "face": {
      "edits": [{"target": "expression", "action": "change_to", "value": "smiling"}]
    }
  }
}
```

### Hybrid Mode

Reference images + local edits combined:

```json
{
  "user_intent": "Change pose to reference image, make bag leather material",
  "meta": {"aspect_ratio": "3:4"},
  "base_image": {"path": "./main.jpg", "strength": 0.92},
  "reference_images": [
    {"path": "./pose.jpg", "usage_type": "pose_copy", "strength": 0.80}
  ],
  "lock": ["face"],
  "edits": {
    "accessories": {
      "edits": [{"target": "material", "action": "change_to", "value": "leather"}]
    }
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
├── SKILL.md                         # Skill definition file (read by Claude)
├── README.md                        # English documentation (this file)
├── README_CN.md                     # Chinese documentation
├── .env.example                     # Environment variables template
├── scripts/
│   └── generate_image.py            # Image generation script
└── references/
    ├── json_schema_t2i_reference.md # Complete Text-to-Image JSON reference
    └── json_schema_i2i_reference.md # Complete Image-to-Image JSON reference (includes Precision Edit Mode)
```

## License

MIT
