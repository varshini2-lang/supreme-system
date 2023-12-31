from fastapi import FastAPI, HTTPException
from typing import List
import re
from datetime import datetime

app = FastAPI()

log_file_path = "/path/to/your/access.log"

def parse_log_entry(entry: str):
    # Define a regular expression to extract timestamp and other details
    pattern = r'\[(.*?)\].*?"\S+ (.*?) \S+" (\d+) (\d+)'
    match = re.match(pattern, entry)
    
    if match:
        timestamp, url, status_code, size = match.groups()
        return {
            "timestamp": timestamp,
            "url": url,
            "status_code": int(status_code),
            "size": int(size)
        }
    else:
        return None

def read_access_logs(start_time: str, end_time: str) -> List[dict]:
    logs = []
    
    try:
        with open(log_file_path, "r") as file:
            for line in file:
                entry = parse_log_entry(line)
                if entry:
                    log_time = datetime.strptime(entry["timestamp"], "%d/%b/%Y:%H:%M:%S %z")
                    if start_time <= log_time <= end_time:
                        logs.append(entry)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Access log file not found.")
    
    return logs

@app.get("/access-logs/")
def get_access_logs(start_time: str, end_time: str):
    try:
        start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S%z")
        end_time = datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S%z")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid datetime format. Use ISO 8601 format.")

    logs = read_access_logs(start_time, end_time)
    return {"access_logs": logs}
