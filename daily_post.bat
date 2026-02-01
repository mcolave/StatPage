@echo off
cd /d "c:\Users\mcolave_msi\OneDrive\Documents\PyScripts2026\StatPage"

echo -------------------------------------------------- >> daily_log.txt
echo Starting Daily Post Routine: %date% %time% >> daily_log.txt

echo Posting Trivia... >> daily_log.txt
"c:\Users\mcolave_msi\OneDrive\Documents\PyScripts2026\.venv\Scripts\python.exe" auto_poster.py --type trivia >> daily_log.txt 2>&1

echo Waiting 60 seconds... >> daily_log.txt
timeout /t 60 /nobreak >nul

echo Posting Random Chart... >> daily_log.txt
"c:\Users\mcolave_msi\OneDrive\Documents\PyScripts2026\.venv\Scripts\python.exe" auto_poster.py --type random_chart >> daily_log.txt 2>&1

echo Routine Complete. >> daily_log.txt
