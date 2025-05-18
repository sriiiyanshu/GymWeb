# Fitness Exercise Application

A Django-based web application that provides information about various exercises, including demonstration videos, images, and proper form instructions.

## Project Overview

This application serves as a comprehensive fitness resource, featuring:
- Exercise demonstrations through videos and images
- Proper form instructions for various exercises
- Categories including strength training, bodyweight exercises, and more
- Rich media content for exercises targeting different muscle groups

## Project Structure

```
├── content/               # Exercise media files (videos, images)
├── django-template/      # Main Django project directory
├── extraction/           # Scripts for data processing
├── hevy_images_filtered/ # Processed exercise images
├── hevy_videos/         # Exercise video content
└── static/              # Static files for the web interface
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
```

3. Install required dependencies:
```bash
cd django-template
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python manage.py migrate
```

## Running the Application

1. Make sure you're in the django-template directory and your virtual environment is activated

2. Start the development server:
```bash
python manage.py runserver
```

3. Open your web browser and navigate to `http://localhost:8000`

## Testing

To run the tests:
```bash
python manage.py test
```

## Development

- The main Django application is in the `django-template` directory
- Media content is organized in the `content` directory
- Static files are served from the `static` directory

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details
