# Smart Room Monitor — IoT Prototype

A beginner-friendly, software-only prototype based on an IoT Smart Room Monitoring System internship report.

## Features

- Simulated temperature and humidity readings for living room, bedroom, and kitchen
- Flask REST API with JSON input validation
- SQLite storage for sensor readings
- Dashboard that refreshes every 3 seconds
- Temperature and humidity alerts
- Summary statistics and temperature history chart
- Seven basic API tests

## Technology stack

Python 3, Flask, SQLite, Requests, HTML, CSS, JavaScript, Chart.js.

## Requirements

- Python 3.10 or later
- Internet connection the first time you open the dashboard, because Chart.js is loaded from a CDN

## Run on Windows (VS Code)

1. Extract this project ZIP.
2. Open the extracted `smart-room-monitor-prototype` folder in VS Code.
3. Open Terminal in VS Code and create a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use Command Prompt and run:
   `.\.venv\Scripts\activate.bat`

4. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

5. Start the Flask API and dashboard:

   ```powershell
   python app.py
   ```

6. Open **http://127.0.0.1:5000** in your browser.

7. Open a **second** VS Code terminal in the same folder and run the simulator:

   ```powershell
   python simulator.py 25 1
   ```

   This sends 25 rounds of readings, with a one-second pause between rounds. Keep the API terminal running.

8. To run the tests, keep the API running and use a third terminal:

   ```powershell
   python test_api.py
   ```

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/data` | Receive and save a reading |
| GET | `/api/latest` | Latest reading per room |
| GET | `/api/history?limit=45` | Recent readings |
| GET | `/api/stats` | Total, averages, maximum temperature and alert count |

Example JSON for `POST /api/data`:

```json
{
  "device_id": "kitchen",
  "temperature": 38.2,
  "humidity": 55
}
```

## Alert rules

- `HIGH_TEMP`: temperature is greater than 35°C
- `HIGH_HUMIDITY`: humidity is greater than 80%
- `NORMAL`: neither limit is crossed

## Project structure

```text
smart-room-monitor-prototype/
├── app.py
├── simulator.py
├── test_api.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   └── dashboard.html
└── static/
    ├── dashboard.js
    └── style.css
```

## Upload to GitHub

Create an empty repository on GitHub, for example `smart-room-monitor-prototype`. Then run these commands in the project folder (replace the URL with your own repository URL):

```powershell
git init
git add .
git commit -m "Add Smart Room Monitor prototype"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/smart-room-monitor-prototype.git
git push -u origin main
```

If `git remote add origin` says the remote already exists, run:
`git remote set-url origin https://github.com/YOUR-USERNAME/smart-room-monitor-prototype.git`

## Important limitations

This is a prototype: the sensor data is simulated, not collected from physical sensors. It is intended for local learning and demonstration, not production use. The API has no authentication. The chart library requires an internet connection when loading the page.
