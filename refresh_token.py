import os
import requests
from dotenv import load_dotenv, set_key

def refresh_tokens():
    print("--- Facebook Token Refresher ---")
    print("1. Go to Graph API Explorer: https://developers.facebook.com/tools/explorer/")
    print("2. Select your App 'StatPage' (if applicable) or default.")
    print("3. In 'User or Page', select 'User Token'.")
    print("4. Add Permissions: 'pages_show_list', 'pages_read_engagement', 'pages_manage_posts'.")
    print("5. Click 'Generate Access Token'.")
    print("6. Copy the token and paste it here.")
    print("-" * 30)
    
    user_token = input("Enter User Access Token: ").strip()
    
    if not user_token:
        print("Empty token provided. Exiting.")
        return

    print("\nFetching Pages...")
    try:
        url = "https://graph.facebook.com/me/accounts"
        params = {
            "access_token": user_token,
            "fields": "name,access_token,id"
        }
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        
        data = resp.json().get('data', [])
        
        target_page = None
        for page in data:
            if page.get('name') == "StatPage":
                target_page = page
                break
        
        if not target_page:
            print("Error: Could not find page named 'StatPage' in your account.")
            print("Available pages: " + ", ".join([p.get('name') for p in data]))
            return

        page_token = target_page.get('access_token')
        page_id = target_page.get('id')
        
        print(f"\nFound Page: {target_page.get('name')} (ID: {page_id})")
        
        # Update .env in the same directory as this script
        env_file = os.path.join(os.path.dirname(__file__), ".env")
        # Create env if not exists
        if not os.path.exists(env_file):
            with open(env_file, 'w') as f: pass
            
        print(f"Updating {env_file}...")
        set_key(env_file, "FB_PAGE_ID", page_id)
        set_key(env_file, "FB_PAGE_ACCESS_TOKEN", page_token)
        # Verify
        set_key(env_file, "FB_USER_ACCESS_TOKEN", user_token) # Optional backup
        
        print("✅ SUCCESS! Credentials updated.")
        print("You can now run 'python auto_poster.py'")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    refresh_tokens()
