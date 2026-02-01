import os
import random
import json
import textwrap
from PIL import Image, ImageDraw, ImageFont
import google.generativeai as genai
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# Configure API
def configure_genai():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env")
    genai.configure(api_key=api_key)

TRIVIA_PROMPTS = [
    "Generate a trivia card about a record-breaking natural wonder (e.g., highest mountain, deepest ocean).",
    "Generate a trivia card about a record-breaking man-made structure (e.g., tallest building, longest bridge).",
    "Generate a trivia card about an extreme weather record.",
    "Generate a trivia card about a biological record (e.g., fast animal, oldest tree)."
]

def generate_trivia_content():
    """
    Generates trivia text using Gemini.
    Returns: dict with topic, stats, fun_fact
    """
    try:
        configure_genai()
        
        # Dynamic text model selection
        text_model_name = 'gemini-1.5-flash' # Default
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if 'flash' in m.name:
                    text_model_name = m.name
                    break
        
        print(f"Using Text Model: {text_model_name}")
        model = genai.GenerativeModel(text_model_name)
        
        prompt = random.choice(TRIVIA_PROMPTS) + """
        Return ONLY a JSON object with this structure:
        {
            "topic": "Title of the subject (e.g. Mount Everest)",
            "stats": ["Stat 1", "Stat 2", "Stat 3"],
            "fun_fact": "A short, interesting fun fact."
        }
        """
        response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
        data = json.loads(response.text)
        return data
    except Exception as e:
        print(f"Error generating text: {e}")
        return None

def create_gradient_image(width, height, start_color, end_color):
    base = Image.new('RGB', (width, height), start_color)
    top = Image.new('RGB', (width, height), end_color)
    mask = Image.new('L', (width, height))
    mask_data = []
    for y in range(height):
        mask_data.extend([int(255 * (y / height))] * width)
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base

def generate_trivia_image(data, output_file="current_trivia.png"):
    """
    Generates a text card image using Pillow.
    Args:
        data (dict): Contains 'topic', 'stats', 'fun_fact'
    """
    try:
        # Dimensions for FB (1200x630 or 1080x1080). Let's do square.
        W, H = 1080, 1080
        
        # Random simple gradient colors (Dark themes)
        colors = [
            ((15, 32, 39), (32, 58, 67)), # Dark Blue
            ((20, 30, 48), (36, 59, 85)), # Royal Blue
            ((19, 78, 94), (113, 178, 128)), # Greenish
            ((35, 7, 77), (204, 83, 51)), # Purple to Orange
            ((0, 0, 0), (67, 67, 67)) # Gray
        ]
        start_c, end_c = random.choice(colors)
        
        print("Generating background...")
        img = create_gradient_image(W, H, start_c, end_c)
        draw = ImageDraw.Draw(img)
        
        # Fonts - Try to load a nice system font, fallback to default
        # Font Handling - Robust Cross-Platform Fix
        def get_font(name, size):
            try:
                return ImageFont.truetype(name, size)
            except IOError:
                return None
                
        # 1. Try Roboto (Downloaded if missing) - Best for consistency
        font_path = "Roboto-Bold.ttf"
        import requests
        if not os.path.exists(font_path):
            print("Downloading Roboto font for consistent rendering...")
            try:
                url = "https://github.com/google/fonts/raw/main/apache/roboto/Roboto-Bold.ttf"
                r = requests.get(url)
                with open(font_path, 'wb') as f:
                    f.write(r.content)
            except Exception as e:
                 print(f"Failed to download font: {e}")
                 
        title_font = get_font(font_path, 80)
        text_font = get_font(font_path, 50)
        small_font = get_font(font_path, 35)
        
        # 2. Fallback to Arial (Windows)
        if not title_font:
             title_font = get_font("arial.ttf", 80)
             text_font = get_font("arial.ttf", 50)
             small_font = get_font("arial.ttf", 35)
             
        # 3. Fallback to DejaVu (Linux/GitHub Actions)
        if not title_font:
             # Common locations on Ubuntu
             linux_fonts = [
                 "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                 "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
             ]
             for f in linux_fonts:
                 title_font = get_font(f, 80)
                 if title_font:
                     text_font = get_font(f, 50)
                     small_font = get_font(f, 35)
                     print(f"Using Linux Font: {f}")
                     break

        # 4. Final Fallback (Bitmap - Tiny but prevents crash)
        if not title_font:
            print("⚠️ Warning: No TrueType font found. Text will be tiny.")
            title_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
            
        # Draw Content
        margin = 100
        current_y = 100
        
        # 1. TOPIC
        title = data.get('topic', 'Trivia Time!')
        # Check text wrapping for Title
        lines = textwrap.wrap(title, width=20)
        for line in lines:
            # Center text
            bbox = draw.textbbox((0, 0), line, font=title_font)
            text_w = bbox[2] - bbox[0]
            draw.text(((W - text_w) / 2, current_y), line, font=title_font, fill="white")
            current_y += 100
            
        current_y += 50
        
        # Separator line
        draw.line((margin, current_y, W - margin, current_y), fill="white", width=3)
        current_y += 80
        
        # 2. STATS
        stats = data.get('stats', [])
        for stat in stats:
            lines = textwrap.wrap(f"• {stat}", width=40)
            for line in lines:
                draw.text((margin, current_y), line, font=text_font, fill="#EEEEEE")
                current_y += 60
            current_y += 20
            
        current_y += 50
        
        # 3. FUN FACT Box
        fact = data.get('fun_fact', '')
        fact_lines = textwrap.wrap(f"💡 {fact}", width=35)
        
        # Draw a semi-transparent box for fun fact
        # Calculate box height
        box_h = (len(fact_lines) * 60) + 40
        overlay = Image.new('RGBA', (W, H), (0,0,0,0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.rectangle(
            [(margin - 20, current_y - 20), (W - margin + 20, current_y + box_h)],
            fill=(255, 255, 255, 30),
            outline="white",
            width=2
        )
        img = Image.alpha_composite(img.convert('RGBA'), overlay)
        draw = ImageDraw.Draw(img) # Re-get draw for merged image
        
        for line in fact_lines:
            # Center/Left align fact? Left looks better in box
            draw.text((margin, current_y), line, font=text_font, fill="#FFD700") # Gold for fun fact
            current_y += 60
            
        # Footer
        draw.text((W - 300, H - 100), "Created by StatPage AI", font=small_font, fill=(200, 200, 200))
        
        img.save(output_file)
        print(f"Trivia card text image saved to {output_file}")
        return output_file
        
    except Exception as e:
        print(f"Error generating text card: {e}")
        return None

if __name__ == "__main__":
    print("--- STARTING TRIVIA ENGINE (TEXT MODE) ---")
    content = generate_trivia_content()
    if content:
        print(f"Content Type: {type(content)}")
        print(f"Content: {content}")
        try:
            print(f"Topic: {content.get('topic')}")
            generate_trivia_image(content)
            print("Done.")
        except Exception as e:
            print(f"Error in main: {e}")
    else:
        print("Failed to get content.")
