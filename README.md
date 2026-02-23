# FastAPI Google Sheets Authentication Service

A concise FastAPI authentication demo that uses Google Sheets as a lightweight backend. It provides a minimal, professional UI for registration and login while recording activity to a Google Sheet.

## Table of contents
- Overview
- Screenshots
- Features
- Quick start
- Google Sheets setup
- Configuration
- Running
- Project structure
- Contributing

## Screenshots
Login and registration screenshots are included to show the UI.

![Login Screenshot](assets/Screenshot%202026-02-23%20225027.png)
*Login interface.*

![Registration Screenshot](assets/Screenshot%202026-02-23%20225038.png)
*Registration interface.*

![Google Sheets - Live Update](assets/image.png)
*Google Sheet showing live updates when users register or log in.*

## ✨ Features
- Lightweight authentication demo using FastAPI
- Google Sheets as the persistent store (no DB required)
- Simple, centered UI for login and signup
- Records signup/login timestamps and metadata to the sheet

## Quick start

1. Install Python 3.8+.
2. Create a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows: .venv\Scripts\activate
```

3. Install runtime dependencies:

```bash
pip install fastapi uvicorn gspread oauth2client
```

4. Place your Google service account JSON file into the project root and name it `credentials.json`.

## Google Sheets setup

1. Create a Google Cloud Service Account and download a JSON key (see GCP docs).
2. Share your Google Sheet with the service account `client_email` (Editor access).
3. Copy the spreadsheet ID from the sheet URL and place it in `main.py` as the `SPREADSHEET_ID` value.

## Configuration
- `credentials.json` — Service account key (do not commit)
- `SPREADSHEET_ID` — Spreadsheet ID to write/read data

Example (in `main.py`):

```python
SPREADSHEET_ID = 'your_spreadsheet_id_here'
```

## Run locally

Start the app with uvicorn:

```bash
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000` to view the UI. API docs are available at `http://127.0.0.1:8000/docs`.

## Tests
- `test_connection.py` can be used to validate the Google Sheets connection.

## Project structure

- `main.py` — FastAPI app and routes
- `credentials.json` — Google service account key (local only)
- `assets/` — UI screenshots used in this README
- `test_connection.py` / `test.py` — small test helpers

## Contributing
Contributions and improvements are welcome. Please open issues or PRs.

## License
This repository is provided under an open-source license. Use and modify freely.
