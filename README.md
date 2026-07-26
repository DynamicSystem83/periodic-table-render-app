# Periodic Table Encoding/Decoding Render App

This project deploys as two Render services:

- `backend`: Flask API deployed as a Render Web Service.
- `frontend`: React app deployed as a Render Static Site.

The app accepts text, sends it to the Flask backend, applies a Caesar shift, and displays the shifted output.

## Local Development

Backend:

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

The frontend reads the backend URL from `VITE_API_BASE_URL`. Without that variable it uses `http://localhost:5000`.

## Render Deployment

Create the services from `render.yaml`, or create them manually:

1. Create a Render Web Service from `backend`.
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
2. Create a Render Static Site from `frontend`.
   - Build command: `npm install && npm run build`
   - Publish directory: `dist`
3. Set `VITE_API_BASE_URL` on the Static Site to the deployed backend URL.
4. Set `CORS_ORIGINS` on the Web Service to the deployed frontend URL.
