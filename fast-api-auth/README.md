# FastAPI Google Sheets Authentication Service

A formal, high-performance authentication service built with FastAPI that uses Google Sheets as a lightweight backend database. Features a minimalist black and white aesthetic with a tabbed interface.

## ✨ Features
- **Formal Aesthetic**: Professional black and white design using the Inter typeface.
- **Tabbed Layout**: Single centered card for both Login and Registration.
- **Google Sheets Backend**: Real-time logging of user activity including signup dates, login times, and IP addresses.
- **Toast Notifications**: Interactive feedback for user actions.

## 📸 Demonstration
![Login View](assets/login_view.png)
*Figure 1: System Login Interface*

![Registration View](assets/registration_view.png)
*Figure 2: Account Registration Interface*

---

## 🚀 Setup Instructions

### 1. Prerequisite Environments
Ensure you have Python 3.8+ installed on your system.

### 2. Install Dependencies
Navigate to the project directory and run:
```bash
pip install fastapi uvicorn gspread
```

### 3. Google Cloud Platform (GCP) Setup
To connect to Google Sheets, you need a Service Account:
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (e.g., `FastApi-Auth`).
3. Enable the **Google Sheets API** and **Google Drive API** in the API Library.
4. Go to **IAM & Admin > Service Accounts**.
5. Click **Create Service Account**, give it a name, and click **Create and Continue**.
6. Select the **Editor** role and click **Done**.
7. Click on the newly created service account, go to the **Keys** tab, and click **Add Key > Create New Key**.
8. Select **JSON** and download the file. Rename it to `credentials.json` and place it in the `fast-api-auth` folder.

### 4. Google Sheets Configuration
1. Create a new Google Sheet.
2. **Important**: Share the Google Sheet with the `client_email` found in your `credentials.json` (give it **Editor** access).
3. Copy the **Spreadsheet ID** from the URL:
   `https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit`
4. Open `main.py` and update the `SPREADSHEET_ID` variable:
   ```python
   SPREADSHEET_ID = 'your_spreadsheet_id_here'
   ```

### 5. Running the Application
Start the server using `uvicorn`:
```bash
uvicorn main:app --reload
```
The application will be available at `http://127.0.0.1:8000`.

---

## 🛠 Project Structure
- `main.py`: Core FastAPI application with embedded HTML/CSS/JS.
- `credentials.json`: Google Service Account keys (do not commit this to version control).
- `assets/`: Directory for project screenshots and media.
- `test.py`: Simple Python script for automated testing.

## 📝 License
This project is open-source. Feel free to use and modify.
