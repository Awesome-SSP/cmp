@echo off
REM Optional: go to the script's directory
cd /d "C:\Users\{username}\Desktop\cmp-main"

REM Run the Python script and log output
"C:\Users\{username}\AppData\Local\Programs\Python\Python312\python.exe" 1.py >> log.txt 2>&1


@echo off
cd /d "C:\Users\{username}\Desktop\cmp-main"
"C:\Users\{username}\AppData\Local\Programs\Python\Python311\python.exe" rpa_email_task.py >> log.txt 2>&1
