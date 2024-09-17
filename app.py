from flask import Flask, request, jsonify
from PIL import Image, ImageDraw, ImageFont
import os
import random
import math
from math import sin, cos, radians
import io
from transliterate import translit, detect_language
import re
import unicodedata

# Constants
TEMPLATE_DIR = 'templates'  # Directory containing your PNG templates
DEFAULT_TEMPLATE = 'default.png'  # Default template file
FONT_PATH = 'SourceCodePro-Regular.ttf'  # Path to your font file
FONT_SIZE = 50  # Font size
MAX_TEXT_WIDTH = 900  # Maximum width for the text block
STICKERS_DIR = 'stickers'  # Directory containing sticker PNG images
MAX_STICKERS = 10  # Maximum number of stickers to place
STICKER_SIZE_RANGE = (0.1, 0.2)
ROTATION_RANGE = (-30, 30)  # Rotation range in degrees
STICKER_CROP_FACTOR = 0.3

app = Flask(__name__)

# Ensure the public directory exists
os.makedirs('public', exist_ok=True)

def add_stickers(base_image, num_stickers):
    stickers = [f for f in os.listdir(STICKERS_DIR) if f.endswith('.png')]
    if not stickers:
        return base_image

    # Ensure unique stickers
    num_stickers = min(num_stickers, len(stickers), MAX_STICKERS)
    chosen_stickers = random.sample(stickers, num_stickers)

    # Define edge zone (percentage of image dimensions)
    edge_zone = 0.2  # 20% from each edge

    width, height = base_image.size
    edge_width = int(width * edge_zone)
    edge_height = int(height * edge_zone)

    # Define placement areas (edges of the image)
    areas = [
        (0, 0, edge_width, height),  # Left edge
        (width - edge_width, 0, width, height),  # Right edge
        (edge_width, 0, width - edge_width, edge_height),  # Top edge
        (edge_width, height - edge_height, width - edge_width, height)  # Bottom edge
    ]

    # Shuffle areas to randomize initial placements
    random.shuffle(areas)

    for i, sticker_file in enumerate(chosen_stickers):
        sticker_path = os.path.join(STICKERS_DIR, sticker_file)
        sticker = Image.open(sticker_path).convert("RGBA")

        # Random size while maintaining aspect ratio
        size_factor = random.uniform(*STICKER_SIZE_RANGE)
        new_width = int(width * size_factor)
        new_height = int(new_width * sticker.height / sticker.width)
        sticker = sticker.resize((new_width, new_height), Image.LANCZOS)

        # Random rotation
        rotation = random.uniform(*ROTATION_RANGE)
        sticker = sticker.rotate(rotation, expand=True)

        # Choose placement area
        if i < 4:  # For the first 4 stickers, use different areas
            area = areas[i % 4]
        else:  # For subsequent stickers, choose random area
            area = random.choice(areas)

        # Calculate position within the chosen area
        x_min, y_min, x_max, y_max = area
        crop_width = int(sticker.width * STICKER_CROP_FACTOR)
        crop_height = int(sticker.height * STICKER_CROP_FACTOR)
        
        # Ensure valid ranges for x and y
        x_start = max(x_min - crop_width, 0)
        x_end = min(x_max - sticker.width + crop_width, width - 1)
        y_start = max(y_min - crop_height, 0)
        y_end = min(y_max - sticker.height + crop_height, height - 1)

        # If the range is invalid, adjust it
        if x_start > x_end:
            x_start, x_end = x_end, x_start
        if y_start > y_end:
            y_start, y_end = y_end, y_start

        # Generate random position
        x = random.randint(x_start, x_end)
        y = random.randint(y_start, y_end)

        # Create a new transparent image for the rotated sticker
        temp = Image.new('RGBA', base_image.size, (0, 0, 0, 0))
        temp.paste(sticker, (x, y), sticker)

        # Composite the sticker onto the base image
        base_image = Image.alpha_composite(base_image.convert('RGBA'), temp)

    return base_image

def slugify(text):
    """
    Convert spaces or repeated dashes to single dashes. Remove characters that aren't alphanumerics, 
    underscores, or hyphens. Convert to lowercase. Also strip leading and trailing whitespace.
    """
    text = unicodedata.normalize('NFKD', text)
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[-\s]+', '-', text)

def transliterate_filename(title):
    # Detect if the title contains Cyrillic characters
    if re.search('[\u0400-\u04FF]', title):
        # Transliterate Cyrillic characters to Latin
        title = translit(title, 'ru', reversed=True)
    
    # Slugify the title to make it URL-friendly
    return slugify(title)

@app.route('/create-image', methods=['POST'])
def create_image():
    title = request.json.get('title')
    template_name = request.json.get('template_name', DEFAULT_TEMPLATE)
    use_stickers = request.json.get('use_stickers', False)
    num_stickers = request.json.get('num_stickers', 5)

    if not title:
        return jsonify({"error": "Title is required"}), 400

    # Add .png extension if not present
    if not template_name.endswith('.png'):
        template_name += '.png'

    # Construct the template path
    template_path = os.path.join(TEMPLATE_DIR, template_name)

    # Open the specified PNG template
    try:
        img = Image.open(template_path).convert('RGBA')
    except IOError:
        return jsonify({"error": f"Template image '{template_name}' not found"}), 500

    if use_stickers:
        img = add_stickers(img, num_stickers)

    draw = ImageDraw.Draw(img)

    # Load a font
    try:
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    except IOError:
        return jsonify({"error": "Font file not found"}), 500

    # Function to wrap text
    def wrap_text(text, font, max_width):
        lines = []
        words = text.split()
        while words:
            line = ''
            while words and draw.textlength(line + words[0], font=font) <= max_width:
                line += (words.pop(0) + ' ')
            lines.append(line.strip())
        return lines

    # Wrap the text
    lines = wrap_text(title, font, MAX_TEXT_WIDTH)

    # Calculate text height
    total_text_height = sum(draw.textbbox((0, 0), line, font=font)[3] for line in lines)

    # Initial y position
    current_y = (img.height - total_text_height) / 2

    # Function to draw text with highlight box
    def draw_text_with_highlight(draw, text, font, pos, text_color, highlight_color):
        x, y = pos
        # Get text size
        bbox = draw.textbbox((x, y), text, font=font)
        
        # Draw the highlight box
        padding = 10  # Adjust this value to change the size of the highlight box
        highlight_bbox = (bbox[0]-padding, bbox[1]-padding, bbox[2]+padding, bbox[3]+padding)
        draw.rectangle(highlight_bbox, fill=highlight_color)
        
        # Draw the text
        draw.text((x, y), text, font=font, fill=text_color)

    # Add text to the image line by line
    for line in lines:
        text_width = draw.textlength(line, font=font)
        text_x = (img.width - text_width) / 2
        draw_text_with_highlight(draw, line, font, (text_x, current_y), (255, 255, 255), (0, 0, 0))
        current_y += draw.textbbox((0, 0), line, font=font)[3]

    # Transliterate the filename if it's in Cyrillic
    transliterated_title = transliterate_filename(title)
    # Save the image in WebP format
    image_path = f'public/{transliterated_title.replace(" ", "_")}.webp'
    
    # Convert to RGB mode (WebP doesn't support RGBA)
    img = img.convert('RGB')
    
    # Use BytesIO to save in memory first
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='WEBP', quality=30, method=6)
    
    # Write to file
    with open(image_path, 'wb') as f:
        f.write(img_byte_arr.getvalue())

    return jsonify({"image_path": image_path}), 200

@app.route('/list-templates', methods=['GET'])
def list_templates():
    # List all .png files in the TEMPLATE_DIR
    templates = [f[:-4] for f in os.listdir(TEMPLATE_DIR) if f.endswith('.png')]
    return jsonify({"templates": templates})

if __name__ == '__main__':
    app.run(debug=True)



