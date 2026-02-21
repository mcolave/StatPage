from flask import Flask, render_template, request, jsonify
from charts.factory import create_generic_chart, create_covid_chart
from chatbot.engine import ChatEngine
from stats_config import STATS, get_stat_config
from data_loader import fetch_wb_data, load_population_data, load_forest_data, load_internet_data, load_literacy_data

app = Flask(__name__)
chat_engine = ChatEngine()

@app.context_processor
def inject_global_stats():
    categories = ["Global Economy", "Global Society", "Global Environment", "Southeast Asia"]
    grouped_stats_nav = {}
    for cat in categories:
        grouped_stats_nav[cat] = [s for s in STATS if s.get('category', 'Other') == cat]
    
    return dict(global_stats=STATS, grouped_stats_nav=grouped_stats_nav)

@app.route("/")
def index():
    from charts.factory import create_trends_map
    map_json = create_trends_map()

    # Load Key Metrics
    from data_loader import load_summary_stats
    key_metrics = load_summary_stats()
    
    # Load Highlight Chart (SEA GDP)
    from stats_config import get_stat_config, get_region_countries
    from data_loader import fetch_wb_data
    from charts.factory import create_generic_chart
    
    sea_config = get_stat_config("sea_gdp_cap")
    sea_filter = get_region_countries("sea")
    sea_df = fetch_wb_data(sea_config["indicator"], "sea_gdp.json", filter_countries=sea_filter)
    
    # Use config title or override
    chart_title = f"{sea_config['title']} (Highlight)"
    
    sea_chart_json = create_generic_chart(
        sea_df, 
        sea_config.get("type", "bar"), 
        chart_title,
        "Value",
        sea_config.get("color_scale", "Viridis"),
        orientation="h"
    )

    # Load Daily Trivia
    trivia_data = None
    try:
        import json
        import os
        base_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(base_dir, "current_trivia.json")
        
        if os.path.exists(json_path):
            with open(json_path, "r") as f:
                trivia_data = json.load(f)
    except Exception as e:
        print(f"Error loading trivia: {e}")

    # Group Stats by Category
    grouped_stats = {}
    # Define desired order
    categories = ["Global Economy", "Global Society", "Global Environment", "Southeast Asia", "Other"]
    
    for cat in categories:
        grouped_stats[cat] = [s for s in STATS if s.get('category', 'Other') == cat]
        
    # Add any missing categories dynamically if needed (optional, skipping for now as we control config)

    return render_template("index.html", mapJSON=map_json, seaChartJSON=sea_chart_json, trivia=trivia_data, key_metrics=key_metrics, grouped_stats=grouped_stats)

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message", "")
    response = chat_engine.process_query(user_msg)
    return jsonify({"response": response})

# Dynamic Stat Route
@app.route("/stats/<stat_id>")
def stat_detail(stat_id):
    from stats_config import get_region_countries # Import here or at top
    config = get_stat_config(stat_id)
    if not config:
        return "Stat not found", 404
        
    # Handle Data Loading
    if "custom_data_func" in config:
        # For legacy/custom sources like RestCountries or local lists
        func_name = config["custom_data_func"]
        if func_name == "load_population_data":
            df = load_population_data() # Returns DataFrame with 'Country', 'Population'
            # Rename for generic chart if needed, or handle inside generic chart
            if not df.empty: df = df.rename(columns={"Population": "Value"})
        else:
             df = pd.DataFrame()
    elif config["type"] == "list":
         # Handle List View Data (Manual mapping for now or generic list fetcher?)
         # The config uses indicators for list types too (Internet, Forest, Literacy)
         df = fetch_wb_data(config["indicator"], f"{stat_id}.json")
         if not df.empty:
             data = df.head(20).to_dict(orient='records')
             return render_template("stat_list.html", title=config["title"], data=data, stat_config=config)
         else:
             return render_template("stat_list.html", title=config["title"], data=[], stat_config=config)
         
    else:
        # Generic World Bank Data
        # Check for regional filter
        filter_countries = None
        if "filter_region" in config:
            filter_countries = get_region_countries(config["filter_region"])
            
        df = fetch_wb_data(config["indicator"], f"{stat_id}.json", filter_countries=filter_countries)
        print(f"DEBUG: Loaded df for {stat_id}")
        print(df.head())
        if not df.empty:
            print(f"DEBUG: First row values: {df.iloc[0].to_dict()}")

    # Generate Chart
    chart_json = create_generic_chart(
        df, 
        config.get("type", "bar"), 
        config.get("chart_title", config["title"]),
        "Value",
        config.get("color_scale", "Viridis"),
        orientation=config.get("orientation", "v")
    )
    
    return render_template("stat_detail.html", graphJSON=chart_json, stat_config=config)

# Keep Covid route separate as it's unique (Time Series)
@app.route("/covid")
def covid():
    chart_json = create_covid_chart()
    return render_template("stat_detail.html", graphJSON=chart_json, stat_config={
        "title": "Covid-19 Impact", 
        "desc": "Track the history of pandemic cases globally."
    })

if __name__ == "__main__":
    app.run(debug=True)