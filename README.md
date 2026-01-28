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
- **Deployment**: Docker & Docker Compose with Nginx

## Quick Start

### Option 1: Docker

1. **Copy environment file**:
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` file** with your configuration:
   - Change `SECRET_KEY` to a secure random string
   - Update `POSTGRES_PASSWORD` to a strong password
   - Set `DEBUG=False` for production

3. **Build and start containers**:
   ```bash
   make docker-build
   make docker-up
   ```

4. **View logs**:
   ```bash
   make docker-logs
   ```

5. Visit `http://localhost` to view recipes

**Docker Commands**:
- `make docker-build` - Build Docker images
- `make docker-up` - Start containers
- `make docker-down` - Stop containers
- `make docker-logs` - View logs
- `make docker-restart` - Restart containers
- `make docker-clean` - Remove containers and volumes

### Option 2: Local Development

1. **Set up environment variables**:
   ```bash
   export SECRET_KEY="your-secret-key-here"
   # Or create a .env file and source it:
   # cp .env.example .env
   # Edit .env with your values
   # export $(cat .env | xargs)
   ```

2. **Install dependencies** (using [uv](https://github.com/astral-sh/uv)):
   ```bash
   uv sync
   ```

3. **Run migrations**:
   ```bash
   uv run python manage.py migrate
   ```

4. **Populate sample data** (optional):
   ```bash
   uv run python manage.py populate_recipes
   ```

5. **Create admin user** (optional):
   ```bash
   uv run python manage.py createsuperuser
   ```

6. **Start the development server**:
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
- [x] ~~Add possibility to load initial recipes~~
- [x] ~~Add proper views for adding and editing recipes (just possible in Django admin view)~~
- [ ] Allow users to switch between tiles and table on the landing page
- [ ] Add categories, tags, searching and filtering
- [ ] Use compiled tailwind instead of default cdn
- [ ] AI?
