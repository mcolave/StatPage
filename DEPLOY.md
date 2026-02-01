# Replacing Your Existing PythonAnywhere Site

Since you already have a web app running at `mcolave.pythonanywhere.com`, follow these steps to **overwrite** it with the new StatHub site.

## 1. Clean Up Old Files
1.  Log in to your [PythonAnywhere Dashboard](https://www.pythonanywhere.com/).
2.  Go to the **Files** tab.
3.  Look for your existing project folder (e.g., `mysite` or whatever you used before).
    - *Optional: Rename it to `mysite_backup` if you want to save it.*
    - **Or just delete the old files** inside it to avoid confusion.

## 2. Upload the New Code
1.  In the **Files** tab (home directory `/home/mcolave/`), click **Upload a file**.
2.  Select **`stathub_deploy.zip`** from your computer.
3.  Once uploaded, click **Open Bash Console here** (top right).
4.  Run these commands to unzip the new site into a folder named `stathub`:
    ```bash
    unzip stathub_deploy.zip -d stathub
## 3. Create a Fresh Virtual Environment
In the Bash Console, let's create a cleaner, separate environment for this new app:

```bash
mkvirtualenv stathub-venv
pip install -r stathub/requirements.txt
```
*(This installs your libraries into a new, isolated folder called `stathub-venv`. It won't touch your old projects.)*

## 4. Point Your Web App to the New Code
1.  Go to the **Web** tab.
2.  Scroll down to the **Code** section.
3.  **Source code**: Change this to:
    `/home/mcolave/stathub`
4.  **Working directory**: Change this to:
    `/home/mcolave/stathub`
5.  **IMPORTANT: Virtualenv**: Change this path to your new one:
    `/home/mcolave/.virtualenvs/stathub-venv`

6.  **WSGI configuration file**: Click the file path to edit it.
    - **Delete everything** in the file.
    - **Paste this new configuration**:
      ```python
      import sys
      import os
      
      # Add your project directory to the sys.path
      path = '/home/mcolave/stathub'
      if path not in sys.path:
          sys.path.append(path)
      
      # Load environment variables
      from dotenv import load_dotenv
      project_folder = os.path.expanduser('~/stathub')
      load_dotenv(os.path.join(project_folder, '.env'))
      
      # Import the Flask app
      from app import app as application
      ```
    - Click **Save**.

## 5. Reload
1.  Go back to the **Web** tab.
2.  Click the big green **Reload mcolave.pythonanywhere.com** button.

**That's it!** Your site is now updated with the new Dashboard, Maps, and AI Chatbot. 🚀
