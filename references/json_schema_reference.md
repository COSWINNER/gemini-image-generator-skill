# Nano Banana Structured JSON Prompt Reference

This document provides a comprehensive reference for the structured JSON prompt schema used by Gemini 3 Pro Image generation.

## Schema Overview

The JSON prompt schema contains the following main sections:

| Section | Description | Required |
|---------|-------------|----------|
| `user_intent` | Natural language summary of the goal | No |
| `meta` | Global settings (aspect ratio, quality, etc.) | Recommended |
| `subject` | Array of characters/objects in the image | Recommended |
| `scene` | Environment and atmosphere settings | Recommended |
| `technical` | Virtual photography/camera settings | No |
| `composition` | Framing and angle settings | No |
| `text_rendering` | Settings for text in the image | No |
| `style_modifiers` | Artistic style overrides | No |
| `advanced` | Negative prompts and fine-tuning | No |

## Section Details

### user_intent

A simple string describing the overall goal.

```json
{
  "user_intent": "A cyberpunk warrior standing in a neon-lit alley"
}
```

### meta

Global image generation settings.

| Field | Type | Options | Description |
|-------|------|---------|-------------|
| `aspect_ratio` | string | `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9` | Output dimensions |
| `image_size` | string | `1K`, `2K`, `4K` | Output resolution (default: `1K`) |
| `quality` | string | `ultra_photorealistic`, `standard`, `raw`, `anime_v6`, `3d_render_octane`, `oil_painting`, `sketch`, `pixel_art`, `vector_illustration` | Rendering mode |
| `safety_filter` | string | `block_none`, `block_few`, `block_some`, `block_most` | Content filtering |
| `seed` | integer | any number | For reproducible results |
| `steps` | integer | 10-100 | Denoising steps (higher = more detail) |
| `guidance_scale` | number | 1.0-20.0 | How strictly AI follows prompt |

### subject

Array of characters or objects. Each subject can have:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier (e.g., "hero", "villain") |
| `type` | string | `person`, `animal`, `cyborg`, `monster`, `statue`, `robot`, `vehicle`, `object` |
| `description` | string | Visual traits description |
| `name` | string | Famous character/person name |
| `age` | string | Age description |
| `gender` | string | `male`, `female`, `non-binary`, `androgynous` |
| `hair` | object | Hair style and color |
| `position` | string | `center`, `left`, `right`, `far_left`, `far_right`, `background`, `foreground` |
| `pose` | string | Action/pose description |
| `expression` | string | Facial expression |
| `clothing` | array | Garments worn |
| `accessories` | array | Jewelry, bags, eyewear, etc. |
| `input_image` | object | Reference image for image-to-image |

#### input_image (for image-to-image generation)

```json
{
  "input_image": {
    "path": "./reference.jpg",
    "usage_type": "face_id",
    "strength": 0.85
  }
}
```

Usage types:
- `face_id`: Swap/preserve face identity
- `pose_copy`: Copy skeleton/stance
- `clothing_transfer`: Copy outfit
- `depth_map`: Copy 3D shape
- `full_character_reference`: Full character reference
- `style_transfer`: Transfer artistic style

### scene

Environment settings.

| Field | Type | Description |
|-------|------|-------------|
| `location` | string | Setting description (e.g., "tokyo street", "mars colony") |
| `time` | string | `golden_hour`, `blue_hour`, `high_noon`, `midnight`, `sunrise`, `sunset`, `twilight`, `pitch_black` |
| `weather` | string | `clear_skies`, `overcast`, `rainy`, `stormy`, `snowing`, `foggy`, `hazy`, `sandstorm`, `acid_rain` |
| `lighting` | object | Lighting type and direction |
| `background_elements` | array | Background items (e.g., "flying cars", "cherry blossoms") |

### technical

Camera/photography settings.

| Field | Type | Description |
|-------|------|-------------|
| `camera_model` | string | `iPhone 15 Pro`, `Sony A7R IV`, `Leica M6`, etc. |
| `lens` | string | `16mm` (ultra wide) to `400mm` (telephoto) |
| `aperture` | string | `f/1.2` (bokeh) to `f/16` (sharp) |
| `shutter_speed` | string | `1/8000` (freeze) to `long_exposure_bulb` |
| `iso` | string | `100` (clean) to `12800` (grainy) |
| `film_stock` | string | `Kodak Portra 400`, `CineStill 800T`, etc. |

### composition

Framing settings.

| Field | Type | Options |
|-------|------|---------|
| `framing` | string | `extreme_close_up`, `close_up`, `medium_shot`, `cowboy_shot`, `full_body`, `wide_shot`, `extreme_wide_shot`, `macro_detail` |
| `angle` | string | `eye_level`, `low_angle`, `high_angle`, `dutch_angle`, `bird_eye_view`, `worm_eye_view`, `overhead`, `pov`, `drone_view` |
| `focus_point` | string | `face`, `eyes`, `hands`, `background`, `foreground_object`, `whole_scene` |

### text_rendering

For rendering text in images.

```json
{
  "text_rendering": {
    "enabled": true,
    "text_content": "HELLO",
    "placement": "neon_sign_on_wall",
    "font_style": "cyberpunk_digital",
    "color": "glowing cyan"
  }
}
```

### style_modifiers

Artistic style overrides.

| Field | Type | Description |
|-------|------|-------------|
| `medium` | string | `photography`, `3d_render`, `oil_painting`, `watercolor`, `pencil_sketch`, `ink_drawing`, `anime`, `concept_art`, etc. |
| `aesthetic` | array | `cyberpunk`, `steampunk`, `vaporwave`, `synthwave`, `noir`, `minimalist`, `gothic`, `baroque`, `retro_80s`, etc. |
| `artist_reference` | array | Names of artists to mimic (use with caution) |

### advanced

Fine-tuning options.

| Field | Type | Description |
|-------|------|-------------|
| `negative_prompt` | array | Elements to exclude (e.g., "blur", "low quality", "bad hands") |
| `magic_prompt_enhancer` | boolean | AI expands prompt with adjectives |
| `hdr_mode` | boolean | High Dynamic Range balancing |

## Example Prompts

### Simple Portrait

```json
{
  "user_intent": "Professional headshot of a business executive",
  "meta": {
    "aspect_ratio": "4:5",
    "quality": "ultra_photorealistic"
  },
  "subject": [{
    "type": "person",
    "description": "confident business executive",
    "gender": "female",
    "age": "40s",
    "expression": "smiling",
    "clothing": [{
      "item": "blazer",
      "color": "navy blue",
      "fabric": "wool"
    }]
  }],
  "scene": {
    "location": "modern office",
    "lighting": {
      "type": "studio_softbox",
      "direction": "front_lit"
    }
  },
  "composition": {
    "framing": "close_up",
    "angle": "eye_level",
    "focus_point": "eyes"
  }
}
```

### Cyberpunk Scene

```json
{
  "user_intent": "Cyberpunk hacker in a neon-lit alley",
  "meta": {
    "aspect_ratio": "21:9",
    "quality": "ultra_photorealistic"
  },
  "subject": [{
    "type": "cyborg",
    "description": "young hacker with cybernetic eye implant",
    "hair": {
      "style": "undercut",
      "color": "electric_blue"
    },
    "pose": "crouching while typing on holographic keyboard",
    "clothing": [{
      "item": "hoodie",
      "color": "matte black",
      "fabric": "mesh"
    }],
    "accessories": [{
      "item": "VR goggles",
      "material": "chrome",
      "location": "head"
    }]
  }],
  "scene": {
    "location": "cyberpunk alley",
    "time": "midnight",
    "weather": "rainy",
    "lighting": {
      "type": "neon_lights",
      "direction": "rim_light"
    },
    "background_elements": ["holographic advertisements", "flying drones", "steam vents"]
  },
  "style_modifiers": {
    "aesthetic": ["cyberpunk", "noir"]
  },
  "technical": {
    "film_stock": "CineStill 800T"
  }
}
```

### Image-to-Image Example

```json
{
  "user_intent": "Transform my photo into anime style",
  "meta": {
    "quality": "anime_v6"
  },
  "subject": [{
    "type": "person",
    "input_image": {
      "path": "./my_photo.jpg",
      "usage_type": "full_character_reference",
      "strength": 0.8
    }
  }],
  "style_modifiers": {
    "medium": "anime",
    "aesthetic": ["minimalist"]
  }
}
```
