# Facebook Automation for StatPage

This setup allows you to automatically generate statistical charts and post them to your Facebook Page.

## Prerequisites

1.  **Install Dependencies**:
    You need to install the project dependencies, specifically `kaleido` which is used for generating static images.
    ```bash
    pip install -r requirements.txt
    ```

2.  **Facebook Credentials**:
    You need a **Page Access Token** and your **Page ID**.
    - Go to [Meta for Developers](https://developers.facebook.com/).
    - Create an App (Business type).
    - Add the "Graph API Explorer" product or go to the Explorer tool.
    - Generate a User Token with `pages_manage_posts`, `pages_read_engagement` permissions.
    - Extend it to a Long-Lived Token if you want it to last.
    - Exchange it for a **Page Access Token** (via the Explorer or API).
    
    Add these to your `.env` file:
    ```
    FB_PAGE_ID=your_page_id_here
    FB_PAGE_ACCESS_TOKEN=your_long_token_here
    ```

## Usage

### 1. Test Creation (Dry Run)
Check if chart generation works without posting to Facebook.
```bash
python auto_poster.py --dry-run
```
This will save a `current_chart.png` in the folder. Check it to see if it looks good.

### 2. Post a Random Chart
To post a random chart from the available options:
```bash
python auto_poster.py
```

### 3. Post a Specific Chart
To post a specific type (e.g., GDP, CO2):
```bash
python auto_poster.py --type gdp
python auto_poster.py --type covid
```

## Scheduling (Optional)
To run this automatically every day:
- **Windows**: Use "Task Scheduler" to run `python auto_poster.py` daily.
- **PythonAnywhere**: If you deploy this, use the "Tasks" tab to run the script.
