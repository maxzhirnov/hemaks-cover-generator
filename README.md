# Flask Image Generator API

This is a Flask application that generates images with a given title centered on a PNG template, with optional stickers. The application provides API endpoints to create images and list available templates.

## Features

- Accepts a title string and optional parameters via a POST request.
- Places the title text in the center of the selected PNG template.
- Automatically wraps long titles to fit within the image.
- Supports multiple templates with a default fallback.
- Optional feature to add stickers to the image.
- Stickers are placed around the edges of the image for a decorative effect.
- Lists available templates via a dedicated endpoint.
- Saves the generated image in the `public` directory.
- Returns the path to the generated image.

## Prerequisites

- Python 3.9+
- Flask
- Pillow
- Docker (for deployment)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/maxzhirnov/hemaks-cover-generator.git
   cd hemaks-cover-generator
   ```

2. **Set up a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Flask application:**

   ```bash
   python app.py
   ```

2. **Send a POST request to the `/create-image` API:**

   You can use `curl`, Postman, or any HTTP client to send a request:

   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{"title": "Your Title Here", "template_name": "teal", "use_stickers": true, "num_stickers": 5}' http://127.0.0.1:5000/create-image
   ```

   - `template_name` can be provided with or without the `.png` extension. If not provided, the default template will be used.
   - `use_stickers` is a boolean flag to enable or disable sticker placement.
   - `num_stickers` is an optional integer to specify the number of stickers to place (default is 5).

3. **List available templates via the `/list-templates` endpoint:**

   ```bash
   curl http://127.0.0.1:5000/list-templates
   ```

   This will return a JSON response with the list of available template names.

4. **Access the generated image:**

   The response will contain the path to the generated image, which is stored in the `public` directory.

## Deployment

To deploy the application using Docker and GitHub Actions:

1. **Build the Docker image:**

   ```bash
   docker build -t maxzhirnov/hemaks-cover-generator .
   ```

2. **Run the Docker container:**

   ```bash
   docker run -d -p 8992:5000 -v /path/on/host/public:/app/public maxzhirnov/hemaks-cover-generator
   ```

3. **Set up GitHub Actions:**

   Use the provided `.github/workflows/deploy.yml` to automate deployment to your Ubuntu server.

## Configuration

- **Template Images:** Store your PNG templates in the `templates` directory. The application will use `default.png` if no template name is provided.
- **Sticker Images:** Store your PNG stickers in the `stickers` directory.
- **Font:** Ensure the `FONT_PATH` points to a valid `.ttf` font file.
- **Max Text Width:** Adjust `MAX_TEXT_WIDTH` in `app.py` to fit your needs.
- **Sticker Settings:** Modify the following constants in `app.py` to adjust sticker behavior:
  - `MAX_STICKERS`: Maximum number of stickers to place.
  - `STICKER_SIZE_RANGE`: Size range of stickers relative to image width.
  - `ROTATION_RANGE`: Rotation range for stickers in degrees.
  - `STICKER_CROP_FACTOR`: How much of the sticker can be cropped off the edges.

## Customization

You can further customize the image generation by modifying the `create_image` and `add_stickers` functions in `app.py`. This allows you to adjust text placement, sticker distribution, and other visual elements.
