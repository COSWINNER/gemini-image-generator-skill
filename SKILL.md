---
name: gemini-image-generator
description: "This skill generates images using Gemini 3 Pro Image API with real-time web search capabilities via Google Search integration. It supports both text-to-image and image-to-image generation including image editing, style transfer, and image merging. The search functionality ensures generated content can incorporate current information and accurate references. This skill should be used when users want to create, modify, or transform images using AI. The workflow involves three steps: first, Claude analyzes user intent and clarifies unclear requirements through conversation; second, Claude converts intent to structured JSON prompt format; third, Claude calls the generate_image.py script to generate images and save results to the generation-image directory."
---

# Gemini Image Generator Skill

Generate high-quality images using Gemini 3 Pro Image API with structured JSON prompts.

## Capabilities

- **Text-to-Image**: Generate images from natural language descriptions
- **Image-to-Image**: Modify, transform, or combine existing images
  - Face identity preservation
  - Pose transfer
  - Style transfer
  - Clothing transfer
  - Image editing and enhancement
- **Real-time Search**: Integrated Google Search for real-time web queries, ensuring generated content is based on up-to-date information and accurate references

## Prerequisites

Ensure the following dependencies are installed:

```bash
pip install -q -U google-genai Pillow python-dotenv
```

Environment variables must be set:
- `GEMINI_API_KEY`: Your Gemini API key (required)
- `GEMINI_BASE_URL`: Custom API endpoint URL (optional, for proxy or alternative endpoints)

## Supported Aspect Ratios and Resolutions

Gemini 3 Pro Image supports the following aspect ratios and resolutions:

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

**Common Use Cases**:
- `1:1` - Social media posts, profile pictures
- `4:3` / `3:4` - Standard photos
- `16:9` / `9:16` - Desktop wallpapers / Mobile wallpapers
- `4:5` - Instagram portrait
- `21:9` - Ultra-wide cinematic

## Workflow

### Step 1: Analyze User Intent (Claude's Responsibility)

When a user requests image generation, Claude should analyze and clarify their intent:

1. **Identify the generation type**:
   - **Text-to-image (Pure Creation)**: User describes a new image without any reference images
   - **Image-to-image (Reference-based)**: User provides reference image(s) for ANY of these scenarios:
     * Style transfer (e.g., "make it look like this style")
     * Structure/composition reference (e.g., "similar layout/arrangement")
     * Content reference (e.g., "based on this example")
     * Face/identity preservation
     * Pose copying
     * Object/scene transformation

2. **🚨 CRITICAL: Reference Image Detection**:
   - **IF user mentions ANY existing image** (e.g., "像这张图", "参考这个", "based on this", "similar to this image", "用这张图的风格"):
     * ✅ This is Image-to-image generation
     * ✅ You MUST include the reference image in `input_image` field
     * ✅ You MUST pass the image path via `--input-images` parameter
     * ❌ DO NOT just read the image and describe it in text
     * ❌ DO NOT convert visual elements into text prompts
   - **Only if user describes a brand new image from imagination**: Use text-to-image

3. **Determine aspect ratio and resolution**:
   - **For text-to-image**: If user does NOT explicitly specify aspect ratio or resolution, Claude MUST ask the user which aspect ratio and resolution they prefer (refer to the supported options table above)
   - **For image-to-image**: Automatically select the closest matching aspect ratio based on the source image dimensions. For multiple input images, use the primary/main image as reference. If user explicitly specifies a different aspect ratio, use the user's preference instead.

4. **Clarify unclear aspects** by asking the user about:
   - **Subject details**: Who or what is the main subject?
   - **Scene/setting**: Where does this take place?
   - **Style/aesthetic**: Realistic? Artistic? Specific style (cyberpunk, anime, etc.)?
   - **Composition**: Close-up? Full body? Wide shot?
   - **Technical aspects**: Any specific camera look or film style?
   - **Special requirements**: Text in image? Specific poses? Multiple subjects?

5. **For image-to-image**, additionally clarify:
   - Which input images to use?
   - What kind of transformation? (face swap, style transfer, pose copy, etc.)
   - How much to preserve from the original? (strength parameter: 0.5-0.95, higher = more similar)

### Step 2: Convert Intent to JSON Format (Claude's Responsibility)

Claude converts the clarified user intent to a structured JSON prompt. Reference `references/json_schema_reference.md` for the complete schema.

**Key sections to include** (only include relevant fields):

```json
{
  "user_intent": "Natural language summary of the goal",
  "meta": {
    "aspect_ratio": "16:9",
    "image_size": "1K",
    "quality": "ultra_photorealistic"
  },
  "subject": [{
    "type": "person",
    "description": "Visual traits",
    "pose": "Action description",
    "expression": "neutral",
    "clothing": [{"item": "...", "color": "..."}],
    "input_image": {
      "path": "./input.jpg",
      "usage_type": "face_id",
      "strength": 0.85
    }
  }],
  "scene": {
    "location": "Setting description",
    "time": "golden_hour",
    "lighting": {"type": "cinematic", "direction": "rim_light"}
  },
  "composition": {
    "framing": "medium_shot",
    "angle": "eye_level"
  },
  "style_modifiers": {
    "medium": "photography",
    "aesthetic": ["cyberpunk"]
  }
}
```

**Important guidelines**:
- Only include fields relevant to the user's request
- Do not add unnecessary optional fields
- For image-to-image, include `input_image` in the subject
- `aspect_ratio`: One of `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`
- `image_size`: One of `1K`, `2K`, `4K` (default: `1K`)

### Step 3: Generate Image

Execute the image generation script with the JSON prompt.

**IMPORTANT**: Use the skill's path relative to project root: `.claude/skills/gemini-image-generator/scripts/generate_image.py`

#### For Text-to-Image

```bash
python .claude/skills/gemini-image-generator/scripts/generate_image.py --prompt-json '{"user_intent":"..."}'
```

#### For Image-to-Image

```bash
python .claude/skills/gemini-image-generator/scripts/generate_image.py --prompt-json '{"user_intent":"..."}' --input-images ./input1.jpg ./input2.jpg
```

#### Custom Output Directory

```bash
python .claude/skills/gemini-image-generator/scripts/generate_image.py --prompt-json '{"user_intent":"..."}' --output-dir ./my-images
```

#### Output Location

Generated images are saved to `./generation-image/` directory (or custom directory) with timestamp-based filenames:
- Format: `generated_YYYYMMDD_HHMMSS.png`

## Usage Examples

### Example 1: Simple Portrait

**User**: "Generate a professional headshot of a business woman"

**Claude's Analysis**:
1. Ask: "What style do you prefer - formal corporate or more casual professional? Any specific background preference? And what expression - friendly smile or serious/confident?"

**After Clarification**, Claude generates JSON:

```json
{
  "user_intent": "Professional headshot of a business woman",
  "meta": {"aspect_ratio": "4:5", "quality": "ultra_photorealistic"},
  "subject": [{
    "type": "person",
    "gender": "female",
    "description": "confident business executive",
    "expression": "smiling",
    "clothing": [{"item": "blazer", "color": "navy blue"}]
  }],
  "scene": {
    "location": "modern office",
    "lighting": {"type": "studio_softbox"}
  },
  "composition": {"framing": "close_up", "focus_point": "eyes"}
}
```

**Execute**:
```bash
python .claude/skills/gemini-image-generator/scripts/generate_image.py --prompt-json '{"user_intent":"Professional headshot..."}'
```

### Example 2: Image Style Transfer

**User**: "Transform this photo into anime style" (provides input image path)

**Claude's Analysis**:
1. Confirm the input image path
2. Ask: "Which anime style do you prefer? Studio Ghibli soft style, or modern sharp anime? How much stylization - keep recognizable or fully transform?"

**After Clarification**, Claude generates JSON:

```json
{
  "user_intent": "Transform photo into anime style",
  "meta": {"quality": "anime_v6"},
  "subject": [{
    "type": "person",
    "input_image": {
      "path": "./user_photo.jpg",
      "usage_type": "full_character_reference",
      "strength": 0.8
    }
  }],
  "style_modifiers": {"medium": "anime"}
}
```

**Execute**:
```bash
python .claude/skills/gemini-image-generator/scripts/generate_image.py --prompt-json '...' --input-images ./user_photo.jpg
```

### Example 3: Complex Scene with Multiple Elements

**User**: "Create a cyberpunk street scene with a hacker character"

**Claude's Analysis**:
1. Ask about character: "What does the hacker look like? Male/female? Cybernetic enhancements? Clothing style?"
2. Ask about scene: "Time of day? Rainy? What elements in the background - neon signs, flying cars, crowds?"
3. Ask about style: "Ultra-realistic or more stylized/artistic?"

**After Clarification**, Claude generates comprehensive JSON with all scene details.

### Example 4: Image Editing

**User**: "Add a wizard hat to my cat in this photo"

**Claude's Analysis**:
1. Confirm the input image path
2. Ask: "What style of wizard hat - classic pointy purple, colorful magical, or something else?"

**JSON**:
```json
{
  "user_intent": "Add wizard hat to cat photo",
  "subject": [{
    "type": "animal",
    "description": "cat with wizard hat",
    "input_image": {
      "path": "./cat.jpg",
      "usage_type": "full_character_reference",
      "strength": 0.9
    },
    "accessories": [{"item": "wizard hat", "color": "purple", "material": "fabric"}]
  }]
}
```

## Resources

### scripts/

- `generate_image.py`: Main image generation script using Gemini API
  - Accepts JSON prompt via `--prompt-json`
  - Supports input images via `--input-images`
  - Saves output to `--output-dir` (default: `./generation-image/`)

### references/

- `json_schema_reference.md`: Complete documentation of the structured JSON prompt schema with all available fields

## Troubleshooting

### Common Issues

1. **API Key not found**: Ensure `GEMINI_API_KEY` environment variable is set
2. **Image not generated**: Check if the prompt violates content policies
3. **Low quality output**: Adjust quality settings in meta section
4. **Wrong aspect ratio**: Verify `aspect_ratio` in meta section matches your needs

### Tips for Better Results

- Be specific about subject details (age, clothing, pose)
- Include lighting and atmosphere descriptions
- Use technical photography terms for realistic images
- Reference specific art styles for artistic images
- Use negative prompts in advanced section to avoid common issues (blur, bad hands, etc.)
