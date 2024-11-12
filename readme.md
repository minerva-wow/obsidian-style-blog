# Graph Blog

A Django blog system with an Obsidian-style graph visualization of posts. Write in Markdown, visualize with an interactive network graph.

## Key Features

- Interactive post visualization using D3.js
- Markdown content with frontmatter support 
- Tag-based organization with custom colors
- Redis caching for performance
- Basic comment system with rate limiting
- Mobile-responsive design using Tailwind CSS

## Tech Stack

- Python 3.8+
- Django 4.2
- PostgreSQL
- Redis
- Tailwind CSS
- D3.js

## Local Development

1. Clone and setup environment:
```bash
git clone https://github.com/minerva-wow/obsidian-style-blog.git
cd obsidian-style-blog
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Configure environment variables in `.env`:
```
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=blog_db
DB_USER=your-db-user
DB_PASSWORD=your-db-password
REDIS_URL=redis://localhost:6379/1
```

3. Initialize database:
```bash
python manage.py migrate
```

4. Start development server:
```bash
python manage.py runserver
```

## Content Management

### Blog Posts
Create markdown files in `content/` directory with frontmatter:
```markdown
---
title: Python for Data Science
slug: python-data-science
tags: ['Python', 'Data Science', 'Machine Learning']
---

your content here...
```
### About Page
Create `about.md` in the `content/` directory. Check `content/about.md` in the repository for the complete format and structure.
After adding or modifying content, run:
```bash
python manage.py sync_content
```

## Development Notes

```bash
# Watch Tailwind CSS changes
npm install
npm run watch

# Build for production
npm run build
# Collect static files
python manage.py collectstatic --no-input
```

## Deployment

> Note: A verified Railway deployment guide will be added soon. The project is currently in testing phase.

For other deployment options, you'll need to:

- Set up PostgreSQL and Redis
- Configure proper security settings
- Set up static file serving
- Use a production WSGI server (e.g., Gunicorn)
- Configure proper user authentication

## Known Issues

- Redis connection might need additional configuration in production
- Static file handling needs optimization for production
- Rate limiting needs more testing under load

## License

MIT

## Contributing

Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## Questions?

Open an issue or submit a PR.