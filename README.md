# Recipe Viewer (v2)

A clean, modern Django-based recipe viewing application with real-time ingredient calculations.

> **Note:** This is version 2 - a complete rewrite of v1, which was a vibe-coded mess. This version features proper async Django, clean architecture, and full internationalization support.

## Features

- **Recipe Management**: View and manage recipes with ingredients and cooking instructions
- **Dynamic Ingredient Scaling**: Real-time ingredient quantity calculations based on portion size using [Datastar](https://data-star.dev/)
- **Async Django**: Built with Django 5.2+ async views for improved performance
- **Full i18n Support**: Complete internationalization with German and English translations
- **Responsive UI**: Modern, clean interface built with TailwindCSS

## Tech Stack

- **Backend**: Django 5.2+ (async views)
- **Frontend**: Datastar.js for reactive UI updates
- **Styling**: TailwindCSS

## Quick Start

1. **Install dependencies** (using [uv](https://github.com/astral-sh/uv)):
   ```bash
   uv sync
   ```

2. **Run migrations**:
   ```bash
   uv run python manage.py migrate
   ```

3. **Populate sample data** (optional):
   ```bash
   uv run python manage.py populate_recipes
   ```

4. **Create admin user** (optional):
   ```bash
   uv run python manage.py createsuperuser
   ```

5. **Start the development server**:
   ```bash
   uv run python manage.py runserver
   ```

6. Visit `http://localhost:8000` to view recipes

## Development

Format and lint code and check for typing issues:
```bash
make nice
```

## Internationalization

The app supports German (default) and English. To update translations:

```bash
# Extract translatable strings
uv run python manage.py makemessages -l de
uv run python manage.py makemessages -l en

# Edit locale/*/LC_MESSAGES/django.po files

# Compile translations
uv run python manage.py compilemessages
```

## TODOs

- [ ] Add docker compose with postgres for deployment
- [ ] Add possibility to load initial recipes
- [ ] Add proper views for adding and editing recipes (just possible in Django admin view)
- [ ] Add categories, tags, searching and filtering
- [ ] AI?
