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
    
    user_token = input("Enter Short-Lived User Access Token: ").strip()
    # To get a long-lived token, we need App Credentials
    print("\n[Optional] To generate a PERMANENT (Long-Lived) token, we need your App ID & Secret.")
    print("Find them in: https://developers.facebook.com/apps/ -> Settings -> Basic")
    app_id = input("Enter App ID (Press Enter to skip): ").strip()
    app_secret = input("Enter App Secret (Press Enter to skip): ").strip()

    final_user_token = user_token

    if app_id and app_secret:
        print("\nExchanging for Long-Lived Token...")
        try:
            exchange_url = "https://graph.facebook.com/v19.0/oauth/access_token"
            params = {
                "grant_type": "fb_exchange_token",
                "client_id": app_id,
                "client_secret": app_secret,
                "fb_exchange_token": user_token
            }
            resp = requests.get(exchange_url, params=params)
            resp.raise_for_status()
            long_data = resp.json()
            if 'access_token' in long_data:
                final_user_token = long_data['access_token']
                print("✅ Acquired Long-Lived User Token!")
            else:
                print("⚠️ Failed to exchange token, using short-lived one.")
        except Exception as e:
            print(f"⚠️ Exchange failed: {e}")
            print("Proceeding with short-lived token...")

    print("\nFetching Pages...")
    try:
        url = "https://graph.facebook.com/me/accounts"
        params = {
            "access_token": final_user_token,
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
        set_key(env_file, "FB_USER_ACCESS_TOKEN", final_user_token) # Optional backup
        
        print("✅ SUCCESS! Credentials updated.")
        print("IMPORTANT: You must output this new FB_PAGE_ACCESS_TOKEN to GitHub Secrets now.")
        print(f"Your NEW Long-Lived Token (Update GitHub with this!):\n{page_token}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    refresh_tokens()
