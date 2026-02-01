import os
import sys
import random
import json
import argparse
from dotenv import load_dotenv
import plotly.io as pio
import plotly.graph_objs as go
from datetime import datetime

# Import chart factories
from charts.factory import (
    create_gdp_chart, 
    create_population_chart, 
    create_covid_chart, 
    create_co2_chart, 
    create_life_expectancy_chart, 
    create_inflation_chart,
    create_trends_map
)
from fb_utils import post_image_to_fb
# Import Trivia Engine
from trivia_engine import generate_trivia_content, generate_trivia_image

# Load environment variables from the script's directory
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)

CHART_OPTIONS = {
    'gdp': {
        'func': create_gdp_chart,
        'caption': "🌍 Top 10 Countries by GDP\n\nCheck out the economic powerhouses of the world! 💰 #GDP #Economics #DataScience #StatPage"
    },
    'population': {
        'func': create_population_chart,
        'caption': "👥 World Population Distribution\n\nThe most populous nations on Earth. 🌏 #Population #Demographics #DataViz #StatPage"
    },
    'covid': {
        'func': create_covid_chart,
        'caption': "🦠 Global COVID-19 Cumulative Cases\n\nA look back at the pandemic case trends. 📉 #HealthData #Covid19 #Statistics #StatPage"
    },
    'co2': {
        'func': create_co2_chart,
        'caption': "🏭 CO2 Emissions per Capita\n\nTop countries by carbon footprint per person. 🌱 #ClimateChange #Environment #CO2 #StatPage"
    },
    'life_expectancy': {
        'func': create_life_expectancy_chart,
        'caption': "❤️ Life Expectancy at Birth\n\nWhich countries have the highest life expectancy? 🏥 #Health #Longevity #Data #StatPage"
    },
    'inflation': {
        'func': create_inflation_chart,
        'caption': "💸 Global Inflation Rates\n\nCurrent consumer price inflation rates by country. 💹 #Economy #Inflation #Finance #StatPage"
    }
}

def generate_chart_image(chart_type, output_file="current_chart.png"):
    if chart_type not in CHART_OPTIONS:
        print(f"Error: Unknown chart type {chart_type}")
        return None, None

    print(f"Generating {chart_type} chart...")
    chart_info = CHART_OPTIONS[chart_type]
    
    # Get JSON string from factory
    json_str = chart_info['func']()
    
    if not json_str or json_str == '{}':
        print("Error: No data returned for chart.")
        return None, None

    # Parse JSON back to dict
    fig_dict = json.loads(json_str)
    
    # Create Figure object
    fig = go.Figure(fig_dict)
    
    # Improve layout for static image
    fig.update_layout(
        paper_bgcolor='#111111', 
        plot_bgcolor='#111111',
        font=dict(color='white')
    )
    
    # Write image
    try:
        fig.write_image(output_file, width=1200, height=630, engine="kaleido")
        print(f"Chart saved to {output_file}")
        return output_file, chart_info['caption']
    except Exception as e:
        print(f"Error generating image: {e}")
        return None, None

def generate_trivia_post():
    print("Generating AI Trivia...")
    
    # 1. Generate text content
    data = generate_trivia_content()
    if not data:
        print("Failed to generate trivia content.")
        return None, None
        
    print(f"Topic: {data.get('topic')}")
    
    # 2. Generate Image
    # Updated to pass full data dict for Pillow text card generation
    image_path = generate_trivia_image(data, output_file="current_trivia.png")
    if not image_path:
        print("Failed to generate trivia image.")
        return None, None
        
    # 3. Create Caption
    stats_text = "\n".join([f"• {stat}" for stat in data.get('stats', [])])
    caption = f"🧠 StatPage Trivia: {data.get('topic')}!\n\n{stats_text}\n\n💡 Fun Fact: {data.get('fun_fact')}\n\n#Trivia #Knowledge #AI #StatPage"
    
    return image_path, caption

def main():
    parser = argparse.ArgumentParser(description="Auto-post charts to StatPage Facebook.")
    parser.add_argument("--type", type=str, help="Specific chart type to post, 'trivia', or 'random_chart'", choices=list(CHART_OPTIONS.keys()) + ['trivia', 'random_chart'])
    parser.add_argument("--dry-run", action="store_true", help="Generate image but do not post")
    args = parser.parse_args()

    # Retry logic
    max_retries = 3
    attempts = 0
    image_path = None
    caption = None
    
    while attempts < max_retries:
        attempts += 1
        
        try:
            if args.type == 'trivia':
                image_path, caption = generate_trivia_post()
            elif args.type == 'random_chart':
                selected_type = random.choice(list(CHART_OPTIONS.keys()))
                image_path, caption = generate_chart_image(selected_type)
            elif args.type:
                 # Specific chart type
                image_path, caption = generate_chart_image(args.type)
            else:
                # Random selection (Chart OR Trivia)
                # Let's give trivia a 30% chance
                if random.random() < 0.3:
                    image_path, caption = generate_trivia_post()
                else:
                    selected_type = random.choice(list(CHART_OPTIONS.keys()))
                    image_path, caption = generate_chart_image(selected_type)
            
            if image_path:
                break
                
            print(f"Generation failed. Retrying... (Attempt {attempts}/{max_retries})")
            
        except Exception as e:
            print(f"Error during attempt {attempts}: {e}")
            
    if not image_path:
        print("Could not generate content after multiple attempts.")
        return

    if args.dry_run:
        print(f"\n[Dry Run] Generated image: {image_path}")
        print(f"[Dry Run] Caption: \n{caption}")
        return

    # Post to Facebook
    page_id = os.getenv("FB_PAGE_ID")
    access_token = os.getenv("FB_PAGE_ACCESS_TOKEN")
    
    if not page_id or not access_token:
        print("Error: FB_PAGE_ID or FB_PAGE_ACCESS_TOKEN not found in .env")
        return

    result = post_image_to_fb(image_path, caption, page_id, access_token)
    
    if result:
        print("Post successful!")
    else:
        print("Post failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
