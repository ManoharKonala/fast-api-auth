"""
FastAPI Google Sheets Authentication
------------------------------------

Pip Install Commands:
pip install fastapi uvicorn gspread

Usage:
1. Ensure 'credentials.json' is in the same directory.
2. Run: uvicorn main:app --reload
"""

import gspread
from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from datetime import datetime

app = FastAPI()

# --- Configuration ---
CREDENTIALS_FILE = 'credentials.json'
SPREADSHEET_ID = '1UE5uEV6o_VWKNNs56LzJkdc2OJxOpO6djxR5hMHaDWc'

# --- Google Sheets Setup ---
try:
    gc = gspread.service_account(filename=CREDENTIALS_FILE)
    # Open by Key is more robust than name
    sh = gc.open_by_key(SPREADSHEET_ID)
    worksheet = sh.sheet1  # Access the first sheet
    
    # Ensure headers exist
    if not worksheet.row_values(1):
        worksheet.append_row(["Username", "Password", "Action", "Timestamp", "IP"])
        print("Headers added to Google Sheet.")
        
except Exception as e:
    print(f"Error connecting to Google Sheets: {e}")
    # We don't raise immediately to allow app to start, but endpoints will fail if not connected
    worksheet = None

# --- HTML Content ---
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <title>FastAPI Auth | Formal</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #000000;
            --primary-hover: #333333;
            --bg-body: #f9fafb;
            --card-bg: #ffffff;
            --border-color: #e5e7eb;
            --text-main: #111827;
            --text-muted: #6b7280;
        }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-body);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            color: var(--text-main);
        }

        .card {
            background: var(--card-bg);
            padding: 40px;
            border-radius: 4px;
            border: 1px solid var(--border-color);
            width: 360px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
            position: relative;
        }

        .tabs {
            display: flex;
            border-bottom: 2px solid var(--border-color);
            margin-bottom: 32px;
        }

        .tab {
            padding: 12px 0;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            flex: 1;
            text-align: center;
            transition: all 0.2s ease;
            position: relative;
        }

        .tab.active {
            color: var(--primary);
            font-weight: 600;
        }

        .tab.active::after {
            content: '';
            position: absolute;
            bottom: -2px;
            left: 0;
            width: 100%;
            height: 2px;
            background-color: var(--primary);
        }

        .form-container {
            display: none;
        }

        .form-container.active {
            display: block;
        }

        h2 {
            text-align: left;
            color: var(--text-main);
            margin-top: 0;
            margin-bottom: 8px;
            font-weight: 600;
            font-size: 20px;
            letter-spacing: -0.025em;
        }

        p.subtitle {
            color: var(--text-muted);
            font-size: 14px;
            margin-bottom: 32px;
        }

        form {
            display: flex;
            flex-direction: column;
            gap: 16px;
        }

        .input-group {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        label {
            font-size: 12px;
            font-weight: 500;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        input {
            width: 100%;
            padding: 12px;
            border: 1px solid var(--border-color);
            border-radius: 4px;
            font-size: 14px;
            transition: all 0.2s ease;
            box-sizing: border-box;
            outline: none;
            background: #fff;
        }

        input:focus {
            border-color: var(--primary);
        }

        button {
            margin-top: 8px;
            padding: 14px;
            background: var(--primary);
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: all 0.2s ease;
            text-transform: uppercase;
            letter-spacing: 0.025em;
        }

        button:hover {
            background: var(--primary-hover);
        }

        button:disabled {
            background: #d1d5db;
            cursor: not-allowed;
        }

        /* Toast Notification */
        #toast {
            visibility: hidden;
            min-width: 200px;
            background-color: #000;
            color: #fff;
            text-align: center;
            border-radius: 4px;
            padding: 12px 24px;
            position: fixed;
            z-index: 100;
            bottom: 32px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 14px;
            font-weight: 500;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            opacity: 0;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        #toast.show {
            visibility: visible;
            opacity: 1;
            bottom: 48px;
        }

        #toast.success { border-bottom: 3px solid #10B981; }
        #toast.error { border-bottom: 3px solid #EF4444; }

    </style>
</head>
<body>
    <div class="card">
        <div class="tabs">
            <div class="tab active" onclick="switchTab('login')">Login</div>
            <div class="tab" onclick="switchTab('signup')">Registration</div>
        </div>

        <!-- Login Form -->
        <div id="loginSection" class="form-container active">
            <h2>System Login</h2>
            <p class="subtitle">Access your account dashboard.</p>
            <form id="loginForm">
                <div class="input-group">
                    <label>Username</label>
                    <input type="text" name="username" placeholder="johndoe" required>
                </div>
                <div class="input-group">
                    <label>Password</label>
                    <input type="password" name="password" placeholder="••••••••" required>
                </div>
                <button type="submit">Authentication</button>
            </form>
        </div>

        <!-- Registration Form -->
        <div id="signupSection" class="form-container">
            <h2>Account Registration</h2>
            <p class="subtitle">Enter your details to create an account.</p>
            <form id="signupForm">
                <div class="input-group">
                    <label>Username</label>
                    <input type="text" name="username" placeholder="johndoe" required>
                </div>
                <div class="input-group">
                    <label>Password</label>
                    <input type="password" name="password" placeholder="••••••••" required>
                </div>
                <button type="submit">Create Account</button>
            </form>
        </div>
    </div>

    <div id="toast"></div>

    <script>
        function switchTab(tab) {
            // Update tabs
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            event.target.classList.add('active');

            // Update forms
            document.querySelectorAll('.form-container').forEach(f => f.classList.remove('active'));
            if (tab === 'login') {
                document.getElementById('loginSection').classList.add('active');
            } else {
                document.getElementById('signupSection').classList.add('active');
            }
        }

        function showToast(message, type) {
            const toast = document.getElementById("toast");
            toast.className = "show " + type;
            toast.innerText = message;
            setTimeout(function(){ 
                toast.className = toast.className.replace("show", ""); 
            }, 3000);
        }

        async function handleFormSubmit(event, url) {
            event.preventDefault();
            const formData = new FormData(event.target);
            const button = event.target.querySelector('button');
            const originalText = button.innerText;
            
            button.disabled = true;
            button.innerText = 'PROCESSING...';

            try {
                const response = await fetch(url, {
                    method: 'POST',
                    body: formData
                });
                const result = await response.json();
                
                if (response.ok && (result.message.includes("Successful"))) {
                    showToast(result.message, "success");
                    event.target.reset();
                } else {
                    showToast(result.message || "An error occurred", "error");
                }
            } catch (error) {
                showToast("Network error", "error");
            } finally {
                button.disabled = false;
                button.innerText = originalText;
            }
        }

        // Attach listeners
        document.getElementById('signupForm').addEventListener('submit', (e) => handleFormSubmit(e, '/signup'));
        document.getElementById('loginForm').addEventListener('submit', (e) => handleFormSubmit(e, '/login'));
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return html_content

@app.post("/signup")
async def signup(request: Request, username: str = Form(...), password: str = Form(...)):
    if not worksheet:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        # Check if username exists (Column A is index 1)
        usernames = worksheet.col_values(1)
        
        if username in usernames:
            return {"message": "Username already exists"}
        
        # Get Timestamp and IP
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        client_ip = request.client.host
        
        # Append new user with Action "Signup"
        # Schema: [Username, Password, Action, Timestamp, IP]
        worksheet.append_row([username, password, "Signup", timestamp, client_ip])
        return {"message": "Signup Successful"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing signup: {str(e)}")

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if not worksheet:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        # Find the cell with the username
        cell = worksheet.find(username, in_column=1)
        
        if not cell:
            return {"message": "Invalid Credentials"}
        
        # Ignore header row
        if cell.row == 1:
             return {"message": "Invalid Credentials"}

        # Get the Password from the same row, column 2 (B)
        stored_password = worksheet.cell(cell.row, 2).value
        
        if stored_password == password:
            # Update Action (Col 3), Timestamp (Col 4), IP (Col 5)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            client_ip = request.client.host
            
            # Update cells
            worksheet.update_cell(cell.row, 3, "Login")
            worksheet.update_cell(cell.row, 4, timestamp)
            worksheet.update_cell(cell.row, 5, client_ip)
            
            return {"message": "Login Successful"}
        else:
            return {"message": "Invalid Credentials"}
            
    except gspread.exceptions.CellNotFound:
        return {"message": "Invalid Credentials"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing login: {str(e)}")