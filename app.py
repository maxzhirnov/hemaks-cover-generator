from flask import Flask, request, jsonify
from PIL import Image, ImageDraw, ImageFont
import os

# Constants
TEMPLATE_DIR = 'templates'  # Directory containing your PNG templates
DEFAULT_TEMPLATE = 'default.png'  # Default template file
FONT_PATH = 'AzeretMono-Regular.ttf'  # Path to your font file
FONT_SIZE = 50  # Font size
MAX_TEXT_WIDTH = 900  # Maximum width for the text block

app = Flask(__name__)

# Ensure the public directory exists
os.makedirs('public', exist_ok=True)

@app.route('/create-image', methods=['POST'])
def create_image():
    title = request.json.get('title')
    template_name = request.json.get('template_name', DEFAULT_TEMPLATE)

    if not title:
        return jsonify({"error": "Title is required"}), 400

    # Construct the template path
    template_path = os.path.join(TEMPLATE_DIR, template_name)

    # Open the specified PNG template
    try:
        img = Image.open(template_path)
    except IOError:
        return jsonify({"error": f"Template image '{template_name}' not found"}), 500

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

    # Add text to the image line by line
    for line in lines:
        text_width = draw.textlength(line, font=font)
        text_x = (img.width - text_width) / 2
        draw.text((text_x, current_y), line, font=font, fill=(0, 0, 0))
        current_y += draw.textbbox((0, 0), line, font=font)[3]

    # Save the image
    image_path = f'public/{title.replace(" ", "_")}.png'
    img.save(image_path)

    return jsonify({"image_path": image_path}), 200

if __name__ == '__main__':
    app.run(debug=True)