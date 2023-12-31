from fastapi import FastAPI, HTTPException

from datetime import datetime

from typing import List



app = FastAPI()



# Replace 'your_access_log_path' with the actual path to your access log file

access_log_path = '/path/to/your/access/log/file.log'



def parse_log_line(line):

    # Assuming a common log format with date in square brackets

    parts = line.split('[')

    if len(parts) < 2:

        return None

    timestamp_str = parts[1].split(']')[0]

    try:

        timestamp = datetime.strptime(timestamp_str, '%d/%b/%Y:%H:%M:%S %z')

        return timestamp

    except ValueError:

        return None



@app.get("/access-logs/")

def get_access_logs(start_time: datetime, end_time: datetime) -> List[str]:

    try:

        with open(access_log_path, 'r') as file:

            logs = [line.strip() for line in file if parse_log_line(line) and start_time <= parse_log_line(line) <= end_time]

            return logs

    except FileNotFoundError:

        raise HTTPException(status_code=404, detail="Access log file not found")

    except Exception as e:

        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

