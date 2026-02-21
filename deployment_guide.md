# Deployment Guide: PythonAnywhere (Update Existing App)

Since you already have the app set up at `/home/mcolave/stathub` and a virtual environment at `/home/mcolave/.virtualenvs/stathub-venv`, follow these simpler steps to update.

## 1. Upload the ZIP File
1.  Log in to your PythonAnywhere dashboard.
2.  Go to the **Files** tab.
3.  Navigate into your project folder: `stathub`.
4.  Click the **Upload a file** button and select `StatPage_Deploy.zip` from your computer.

## 2. Unzip and Update
1.  Open a **Bash** console from the dashboard.
2.  Run the following commands to update your code:

```bash
# Go to your project directory
cd stathub

# Unzip and overwrite existing files
unzip -o StatPage_Deploy.zip

# Activate your EXISTING virtual environment
workon stathub-venv

# Install any new dependencies
pip install -r requirements.txt
```

## 3. Web App Reload
1.  Go to the **Web** tab.
2.  Click the green **Reload** button at the top.
3.  Your site should be updated!

## troubleshooting
If you see errors, check the **Error Log** link in the Web tab. It's usually a missing package or a syntax error.
