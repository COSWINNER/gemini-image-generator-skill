#!/usr/bin/env python3
"""
Gemini 3 Pro Image Generation Script

This script generates images using Gemini 3 Pro Image API.
Supports both text-to-image and image-to-image generation.

Environment Variables:
    GEMINI_API_KEY: Your Gemini API key (required)
    GEMINI_BASE_URL: Custom base URL for API endpoint (optional)

Usage:
    python generate_image.py --prompt-json '<json_string>' [--input-images <path1> <path2> ...]
    python generate_image.py --prompt-file prompt.json [--input-images <path1> <path2> ...]
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Error: google-genai package not installed.")
    print("Please install with: pip install -q -U google-genai")
    sys.exit(1)

try:
    from PIL import Image
except ImportError:
    print("Error: Pillow package not installed.")
    print("Please install with: pip install Pillow")
    sys.exit(1)


def get_client() -> genai.Client:
    """Initialize Gemini client with environment configuration."""
    api_key = os.environ.get("GEMINI_API_KEY")
    base_url = os.environ.get("GEMINI_BASE_URL")

    if not api_key:
        print("Error: GEMINI_API_KEY environment variable is not set.")
        sys.exit(1)

    client_kwargs = {"api_key": api_key}

    if base_url:
        # Configure custom base URL if provided
        client_kwargs["http_options"] = types.HttpOptions(base_url=base_url)

    return genai.Client(**client_kwargs)


def load_input_images(image_paths: list[str]) -> list:
    """Load input images for image-to-image generation."""
    images = []
    for path in image_paths:
        try:
            img = Image.open(path)
            images.append(img)
            print(f"Loaded input image: {path}")
        except Exception as e:
            print(f"Warning: Failed to load image {path}: {e}")
    return images


def build_prompt_text(prompt_json: dict) -> str:
    """
    Convert structured JSON prompt to natural language prompt.
    This function interprets the JSON schema and creates a descriptive prompt.
    """
    parts = []

    # User intent (if provided)
    if "user_intent" in prompt_json:
        parts.append(prompt_json["user_intent"])

    # Meta settings description
    if "meta" in prompt_json:
        meta = prompt_json["meta"]
        if "quality" in meta:
            parts.append(f"Style: {meta['quality'].replace('_', ' ')}")

    # Subject descriptions
    if "subject" in prompt_json:
        for idx, subj in enumerate(prompt_json["subject"]):
            subj_desc = []

            if "name" in subj:
                subj_desc.append(subj["name"])

            if "type" in subj:
                subj_desc.append(f"({subj['type']})")

            if "description" in subj:
                subj_desc.append(subj["description"])

            if "age" in subj:
                subj_desc.append(f", {subj['age']}")

            if "gender" in subj:
                subj_desc.append(f", {subj['gender']}")

            if "hair" in subj:
                hair = subj["hair"]
                hair_desc = []
                if "color" in hair:
                    hair_desc.append(hair["color"].replace("_", " "))
                if "style" in hair:
                    hair_desc.append(hair["style"].replace("_", " "))
                if hair_desc:
                    subj_desc.append(f", {' '.join(hair_desc)} hair")

            if "pose" in subj:
                subj_desc.append(f", {subj['pose']}")

            if "expression" in subj:
                subj_desc.append(f", {subj['expression']} expression")

            if "position" in subj:
                subj_desc.append(f", positioned {subj['position'].replace('_', ' ')}")

            # Clothing
            if "clothing" in subj:
                clothes = []
                for item in subj["clothing"]:
                    cloth_desc = []
                    if "color" in item:
                        cloth_desc.append(item["color"])
                    if "fabric" in item:
                        cloth_desc.append(item["fabric"])
                    if "item" in item:
                        cloth_desc.append(item["item"])
                    if cloth_desc:
                        clothes.append(" ".join(cloth_desc))
                if clothes:
                    subj_desc.append(f", wearing {', '.join(clothes)}")

            # Accessories
            if "accessories" in subj:
                accs = []
                for acc in subj["accessories"]:
                    acc_desc = []
                    if "material" in acc:
                        acc_desc.append(acc["material"])
                    if "color" in acc:
                        acc_desc.append(acc["color"])
                    if "item" in acc:
                        acc_desc.append(acc["item"])
                    if acc_desc:
                        accs.append(" ".join(acc_desc))
                if accs:
                    subj_desc.append(f", with {', '.join(accs)}")

            if subj_desc:
                parts.append(f"Subject {idx + 1}: " + "".join(subj_desc))

    # Scene description
    if "scene" in prompt_json:
        scene = prompt_json["scene"]
        scene_desc = []

        if "location" in scene:
            scene_desc.append(f"Location: {scene['location']}")

        if "time" in scene:
            scene_desc.append(f"Time: {scene['time'].replace('_', ' ')}")

        if "weather" in scene:
            scene_desc.append(f"Weather: {scene['weather'].replace('_', ' ')}")

        if "lighting" in scene:
            lighting = scene["lighting"]
            light_parts = []
            if "type" in lighting:
                light_parts.append(lighting["type"].replace("_", " "))
            if "direction" in lighting:
                light_parts.append(lighting["direction"].replace("_", " "))
            if light_parts:
                scene_desc.append(f"Lighting: {', '.join(light_parts)}")

        if "background_elements" in scene:
            scene_desc.append(f"Background: {', '.join(scene['background_elements'])}")

        if scene_desc:
            parts.append("Scene: " + "; ".join(scene_desc))

    # Technical/Camera settings
    if "technical" in prompt_json:
        tech = prompt_json["technical"]
        tech_desc = []

        if "camera_model" in tech:
            tech_desc.append(f"Shot on {tech['camera_model']}")

        if "lens" in tech:
            tech_desc.append(f"{tech['lens']} lens")

        if "aperture" in tech:
            tech_desc.append(tech["aperture"])

        if "film_stock" in tech:
            tech_desc.append(f"{tech['film_stock']} film look")

        if tech_desc:
            parts.append("Technical: " + ", ".join(tech_desc))

    # Composition
    if "composition" in prompt_json:
        comp = prompt_json["composition"]
        comp_desc = []

        if "framing" in comp:
            comp_desc.append(comp["framing"].replace("_", " "))

        if "angle" in comp:
            comp_desc.append(f"{comp['angle'].replace('_', ' ')} angle")

        if "focus_point" in comp:
            comp_desc.append(f"focus on {comp['focus_point'].replace('_', ' ')}")

        if comp_desc:
            parts.append("Composition: " + ", ".join(comp_desc))

    # Text rendering
    if "text_rendering" in prompt_json and prompt_json["text_rendering"].get("enabled"):
        text = prompt_json["text_rendering"]
        text_desc = []

        if "text_content" in text:
            text_desc.append(f'text "{text["text_content"]}"')

        if "placement" in text:
            text_desc.append(f"as {text['placement'].replace('_', ' ')}")

        if "font_style" in text:
            text_desc.append(f"in {text['font_style'].replace('_', ' ')} style")

        if "color" in text:
            text_desc.append(f"colored {text['color']}")

        if text_desc:
            parts.append("Text: " + " ".join(text_desc))

    # Style modifiers
    if "style_modifiers" in prompt_json:
        style = prompt_json["style_modifiers"]
        style_desc = []

        if "medium" in style:
            style_desc.append(style["medium"].replace("_", " "))

        if "aesthetic" in style:
            aesthetics = [a.replace("_", " ") for a in style["aesthetic"]]
            style_desc.append(", ".join(aesthetics))

        if "artist_reference" in style:
            style_desc.append(f"in the style of {', '.join(style['artist_reference'])}")

        if style_desc:
            parts.append("Style: " + ", ".join(style_desc))

    # Negative prompt (for context, though Gemini handles this differently)
    if "advanced" in prompt_json and "negative_prompt" in prompt_json["advanced"]:
        neg = prompt_json["advanced"]["negative_prompt"]
        if neg:
            parts.append(f"Avoid: {', '.join(neg)}")

    return "\n".join(parts)


def generate_image(
    client: genai.Client,
    prompt_json: dict,
    input_images: Optional[list] = None,
    output_dir: str = "./generation-image"
) -> str:
    """
    Generate image using Gemini 3 Pro Image.

    Args:
        client: Gemini client instance
        prompt_json: Structured JSON prompt
        input_images: Optional list of PIL Image objects for image-to-image
        output_dir: Directory to save generated images

    Returns:
        Path to the generated image file
    """
    # Ensure output directory exists
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Build text prompt from JSON
    prompt_text = build_prompt_text(prompt_json)
    print(f"\n--- Generated Prompt ---\n{prompt_text}\n------------------------\n")

    # Build content list
    contents = []

    # Add input images for image-to-image generation
    if input_images:
        for img in input_images:
            contents.append(img)
        contents.append(prompt_text)
    else:
        contents.append(prompt_text)

    # Extract configuration from JSON
    meta = prompt_json.get("meta", {})

    # Build image configuration
    image_config_kwargs = {}

    # Aspect ratio
    if "aspect_ratio" in meta:
        image_config_kwargs["aspect_ratio"] = meta["aspect_ratio"]

    # Image size (resolution): 1K, 2K, or 4K
    if "image_size" in meta:
        image_config_kwargs["image_size"] = meta["image_size"]

    # Build generation config
    config = types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"],
        image_config=types.ImageConfig(**image_config_kwargs) if image_config_kwargs else None
    )

    # Generate image
    print("Generating image with Gemini 3 Pro Image...")
    try:
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",  # Using available image generation model
            contents=contents,
            config=config
        )
    except Exception as e:
        print(f"Error generating image: {e}")
        sys.exit(1)

    # Process response and save image
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_saved = False
    response_text = ""

    for part in response.candidates[0].content.parts:
        if part.text is not None:
            response_text = part.text
            print(f"Model response: {part.text}")
        elif part.inline_data is not None:
            # Use the official as_image() method to get PIL Image
            try:
                image = part.as_image()

                # Generate filename
                filename = f"generated_{timestamp}.png"
                filepath = output_path / filename

                # Save using PIL
                image.save(str(filepath))

                print(f"Image saved to: {filepath}")
                image_saved = True
                return str(filepath)
            except AttributeError:
                # Fallback: if as_image() not available, try direct data access
                # inline_data.data is already bytes, no need to base64 decode
                image_data = part.inline_data.data

                # Determine file extension based on mime type
                mime_type = part.inline_data.mime_type
                ext = "png"
                if "jpeg" in mime_type or "jpg" in mime_type:
                    ext = "jpg"
                elif "webp" in mime_type:
                    ext = "webp"

                # Generate filename
                filename = f"generated_{timestamp}.{ext}"
                filepath = output_path / filename

                with open(filepath, "wb") as f:
                    f.write(image_data)

                print(f"Image saved to: {filepath}")
                image_saved = True
                return str(filepath)

    if not image_saved:
        print("Warning: No image was generated in the response.")
        if response_text:
            print(f"Model only returned text: {response_text}")
        return ""

    return ""


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using Gemini 3 Pro Image API"
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--prompt-json",
        type=str,
        help="JSON string containing the structured prompt"
    )
    group.add_argument(
        "--prompt-file",
        type=str,
        help="Path to JSON file containing the structured prompt"
    )

    parser.add_argument(
        "--input-images",
        nargs="+",
        type=str,
        help="Paths to input images for image-to-image generation"
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default="./generation-image",
        help="Directory to save generated images (default: ./generation-image)"
    )

    args = parser.parse_args()

    # Load prompt JSON
    if args.prompt_json:
        try:
            prompt_json = json.loads(args.prompt_json)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON prompt: {e}")
            sys.exit(1)
    else:
        try:
            with open(args.prompt_file, "r", encoding="utf-8") as f:
                prompt_json = json.load(f)
        except Exception as e:
            print(f"Error reading prompt file: {e}")
            sys.exit(1)

    # Initialize client
    client = get_client()

    # Load input images if provided
    input_images = None
    if args.input_images:
        input_images = load_input_images(args.input_images)

    # Generate image
    result = generate_image(
        client=client,
        prompt_json=prompt_json,
        input_images=input_images,
        output_dir=args.output_dir
    )

    if result:
        print(f"\nGeneration complete! Image saved to: {result}")
    else:
        print("\nGeneration completed but no image was saved.")


if __name__ == "__main__":
    main()
