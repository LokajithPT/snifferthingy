# DNS Watchtower

A DNS sniffer and logger for Windows. Logs domain queries, highlights suspicious domains, and displays them on a live-updating dashboard.

## Features

- Logs timestamp, IP address, and domain name
- Highlights known suspicious domains
- Live auto-refreshing web dashboard
- Option to clear all logs
- Client/server architecture

## Requirements

- Windows OS
- Python 3.8+ (must be in PATH)
- Internet access (for package installation)

## Project Structure

```
dns-watchtower/
├── main.py            # Flask server - dashboard + log receiver
├── client.py          # DNS sniffer - sends logs to server
├── requirements.txt   # Python dependencies
├── run_setup.bat      # One-click setup script for Windows
└── templates/
    └── index.html     # Web dashboard template
```

## Setup Instructions

### 1. Install Python

Download and install Python 3.x from:

https://www.python.org/downloads/

During installation, check the box that says:

```
[✔] Add Python to PATH
```

### 2. Run the Setup Script

After Python is installed, double-click `run_setup.bat` or right-click and choose:

```
Run as administrator
```

This will:

- Install required packages from `requirements.txt`
- Launch `main.py` in one terminal
- Launch `client.py` in another terminal
- Open the dashboard at http://localhost:5000 in your browser

## Usage

- The dashboard shows the 100 most recent DNS requests
- Suspicious domains are highlighted in red
- The "Clear All Logs" button deletes everything in the database

## Adding Suspicious Domains

Inside `main.py`, you'll find the following block:

```python
SUS_DOMAINS = {
    "www.youtube.com",
    "www.tiktok.com",
    "www.pornhub.com",
    "www.facebook.com"
    # Add more domains as needed
}
```

Add or remove domains as necessary.

## Known Limitations

- Only logs DNS traffic from the local machine
- Requires administrative privileges for sniffing
- Does not block domains — only logs and highlights them
- Intended for educational and monitoring use

## License

No license. Use however you want. Break it, fork it, mod it.

## Author

Created by Loki.

