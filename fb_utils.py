import requests
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def post_image_to_fb(image_path, caption, page_id, access_token):
    """
    Uploads an image to a Facebook Page via Graph API.
    
    Args:
        image_path (str): Path to the image file.
        caption (str): Text caption for the post.
        page_id (str): The Facebook Page ID.
        access_token (str): The Page Access Token.
        
    Returns:
        dict: The API response (json).
    """
    if not os.path.exists(image_path):
        logger.error(f"Image not found: {image_path}")
        return None

    url = f"https://graph.facebook.com/{page_id}/photos"
    
    payload = {
        'message': caption,
        'access_token': access_token
    }
    
    try:
        with open(image_path, 'rb') as img_file:
            files = {
                'source': img_file
            }
            logger.info(f"Uploading {image_path} to Facebook Page {page_id}...")
            response = requests.post(url, data=payload, files=files, timeout=30)
            
            response.raise_for_status()
            result = response.json()
            logger.info(f"Success! Post ID: {result.get('post_id') or result.get('id')}")
            return result
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Error posting to Facebook: {e}")
        if 'response' in locals():
            try:
                error_data = response.json()
                error_msg = error_data.get('error', {}).get('message', '')
                subcode = error_data.get('error', {}).get('error_subcode')
                
                if subcode == 4854002:
                    print("\n" + "="*50)
                    print("🛑 FACEBOOK SECURITY CHECKPOINT TRIGGERED 🛑")
                    print("Facebook blocked this post because it wants to verify it's really you.")
                    print("ACTION REQUIRED:")
                    print("1. Log in to Facebook.com in your browser.")
                    print("2. Check your notifications or top banner for a 'Suspicious Login' or 'Confirm Identity' alert.")
                    print("3. Approve the activity.")
                    print("4. Wait a few minutes and try again.")
                    print("="*50 + "\n")
                else:
                    logger.error(f"Response: {response.text}")
            except:
                logger.error(f"Response: {response.text}")
        return None
