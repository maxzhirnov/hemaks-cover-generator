# Flask Image Generator API

This is a simple Flask application that generates images with a given title centered on a PNG template. The application provides an API endpoint to receive a title string, place it on a selected template image, and return the path to the generated image.

## Features

- Accepts a title string and an optional template name via a POST request.
- Places the title text in the center of the selected PNG template.
- Automatically wraps long titles to fit within the image.
- Supports multiple templates with a default fallback.
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
   curl -X POST -H "Content-Type: application/json" -d '{"title": "Your Title Here", "template_name": "teal"}' http://127.0.0.1:5000/create-image
   ```

   - `template_name` can be provided with or without the `.png` extension. If not provided, the default template will be used.

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
- **Font:** Ensure the `FONT_PATH` points to a valid `.ttf` font file.
- **Max Text Width:** Adjust `MAX_TEXT_WIDTH` in `app.py` to fit your needs.