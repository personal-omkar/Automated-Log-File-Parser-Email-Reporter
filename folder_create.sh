#!/bin/bash

# Project root folder
PROJECT="automated-log-reporter"

# Create directories
mkdir -p $PROJECT/logs
mkdir -p $PROJECT/reports

# Create files with initial content
cat <<EOL > $PROJECT/requirements.txt
pandas
schedule
openpyxl
EOL

cat <<EOL > $PROJECT/config.json
{
  "email_sender": "your_email@gmail.com",
  "email_password": "your_password",
  "email_receiver": "receiver_email@gmail.com"
}
EOL

cat <<EOL > $PROJECT/README.md
# Automated Log File Parser & Email Reporter

## Features
- Reads server log files (or CSV/JSON).
- Extracts useful data (errors, warnings, daily activity).
- Generates a summary report in Excel.
- Automatically emails the report daily at a scheduled time.

## Tech
Python, Pandas, smtplib, schedule
EOL

cat <<EOL > $PROJECT/logs/server.log
2025-09-17 10:00:00 INFO Service started
2025-09-17 10:01:00 WARNING Disk usage high
2025-09-17 10:02:00 ERROR Connection failed
EOL

# Empty main.py file
touch $PROJECT/main.py

echo "✅ Project structure for '$PROJECT' created successfully!"
