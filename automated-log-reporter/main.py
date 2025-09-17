import pandas as pd
import schedule
import smtplib
import time
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import datetime

# Load config
with open("config.json") as f:
    config = json.load(f)

EMAIL_SENDER = config["email_sender"]
EMAIL_PASSWORD = config["email_password"]
EMAIL_RECEIVER = config["email_receiver"]

def parse_logs():
    # Example: Read logs from file (you can replace with CSV/JSON parsing)
    log_file = "logs/server.log"
    data = []
    with open(log_file, "r") as f:
        for line in f:
            if "ERROR" in line or "WARNING" in line:
                data.append({"timestamp": str(datetime.now()), "log": line.strip()})
    
    df = pd.DataFrame(data)
    filename = f"reports/log_summary_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
    df.to_excel(filename, index=False)
    print(f"[INFO] Report generated: {filename}")
    return filename

def send_email(report_file):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = "Daily Log Summary Report"

    body = MIMEText("Please find attached today's log summary report.", "plain")
    msg.attach(body)

    with open(report_file, "rb") as f:
        attachment = MIMEApplication(f.read(), Name=report_file)
    attachment["Content-Disposition"] = f"attachment; filename={report_file}"
    msg.attach(attachment)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)

    print("[INFO] Email sent successfully.")

def job():
    report = parse_logs()
    send_email(report)

# Run daily at 9 AM
schedule.every().day.at("09:00").do(job)

print("[INFO] Scheduler started...")
while True:
    schedule.run_pending()
    time.sleep(60)
