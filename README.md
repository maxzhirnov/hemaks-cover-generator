```markdown
# Flask Image Generator API

This is a simple Flask application that generates images with a given title centered on a PNG template. The application provides an API endpoint to receive a title string, place it on a selected template image, and return the path to the generated image.

## Features

- Accepts a title string and optional template name via a POST request.
- Places the title text in the center of the selected PNG template.
- Automatically wraps long titles to fit within the image.
- Supports multiple templates with a default fallback.
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
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
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

2. **Send a POST request to the API:**

   You can use `curl`, Postman, or any HTTP client to send a request:

   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{"title": "Your Title Here", "template_name": "your_template.png"}' http://127.0.0.1:5000/create-image
   ```

   If `template_name` is not provided, the default template will be used.

3. **Access the generated image:**

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

- **Template Images:** Store your PNG templates in the `templates` directory. The application will use `default_template.png` if no template name is provided.
- **Font:** Ensure the `FONT_PATH` points to a valid `.ttf` font file.
- **Max Text Width:** Adjust `MAX_TEXT_WIDTH` in `app.py` to fit your needs.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```

### Key Updates

- **Template Support**: Added information about supporting multiple templates and using a default template.
- **Usage Instructions**: Updated usage instructions to include the optional `template_name` parameter.
- **Deployment**: Updated Docker instructions to reflect the use of volumes for persistent storage.
- **Configuration**: Clarified where to store template images and how to configure the application.

Feel free to customize the `README.md` further to match your repository details and specific setup.

Citations:
[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/17767938/e1405793-9ca1-408c-a99e-ad367946640b/paste.txt