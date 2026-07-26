# Encryption Flask API

Small Flask backend for a Render Web Service.

## Local Run

```bash
pip install -r requirements.txt
python app.py
```

## Endpoints

- `GET /health`
- `POST /api/periodic-table-encode-simple`
- `POST /api/periodic-table-decode-simple`

Example body:

```json
{
  "text": "Hello, Render!",
  "shift": 3
}
```
