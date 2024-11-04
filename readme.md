# Obsidian-Style Blog

A Django-based blog system featuring an Obsidian-like graph view of posts and their relationships. This blog system allows you to write posts in Markdown format and visualizes the connections between posts through their tags.

## Features

- 📊 Interactive Graph View Homepage
  - Visual representation of posts and their relationships
  - Force-directed graph layout using D3.js
  - Color-coded tags for better visualization
  
- 📝 Markdown Support
  - Write posts in Markdown format
  - Automatic rendering to HTML
  - Support for basic Markdown syntax
  
- 🏷️ Tag System
  - Customizable tag colors
  - Tag-based post organization
  - Visual representation in graph view
  
- 💬 Comments
  - Comment system for each post
  - User authentication for commenting
  
- 🔄 GitHub Integration
  - Synchronization with GitHub repository
  - Version control for your content
  - Automated content deployment

## Tech Stack

- Backend: Django + PostgreSQL
- Frontend: D3.js for graph visualization
- Content: Markdown
- Version Control: Git

## Project Structure

```
obsidian-style-blog/
├── config/                 # Django project settings
├── blog/                   # Main blog application
├── content/               # Markdown files for posts
├── templates/             # HTML templates
│   └── blog/
│       ├── base.html
│       ├── home.html
│       └── post_detail.html
├── static/                # Static files (CSS, JS)
├── manage.py
├── requirements.txt
└── README.md
```

## Setup

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/obsidian-style-blog.git
cd obsidian-style-blog
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the database:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Usage

### Adding Content

1. Create Markdown files in the `content/` directory
2. Add front matter for tags and metadata
3. Run the sync script to update the database:
```bash
python manage.py sync_content
```

### Customizing Tags

1. Log in to the admin interface
2. Navigate to Tags section
3. Create or edit tags and set their colors

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by Obsidian's Graph View
- Built with Django Framework
- Visualizations powered by D3.js