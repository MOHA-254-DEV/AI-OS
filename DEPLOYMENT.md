# Deployment & GitHub Secrets Guide

## 1. Required Environment Variables

Set these as secrets on Render, Railway, or in your GitHub Actions:

- `OPENAI_API_KEY`
- `API_TOKEN`
- `SECRET_KEY`
- `VOICE_ENABLED`
- `DEBUG_MODE`
- `ENV`
- `PORT`

## 2. Render

- Add the above as Environment Variables in the Render dashboard.
- Use `render.yaml` for one-click deploy.

## 3. Railway

- Add the above as Environment Variables in the Railway dashboard.
- Use `railway.json` and set start command as in example.

## 4. GitHub Actions

- Go to your repository Settings > Secrets and variables > Actions.
- Add secrets with the same names: `OPENAI_API_KEY`, etc.

## 5. Local Development

- Copy `.env.example` to `.env` and fill in values.

## 6. Security

- Never commit your actual secrets or .env file to the repo.
- Use `security/secret_loader.py` for encrypted secrets if needed.
