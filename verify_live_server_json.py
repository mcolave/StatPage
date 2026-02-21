import requests
import re
import json

url = "http://127.0.0.1:5000/stats/sea_gdp_cap"
try:
    response = requests.get(url)
    html = response.text
    
    print(f"Status Code: {response.status_code}")
    
    # Check for Plotly Version
    if "plotly-2.27.0.min.js" in html:
        print("PASS: Plotly v2.27.0 found.")
    else:
        print("FAIL: Plotly v2.27.0 NOT found (using old version?).")
        
    # Extract Graph JSON
    # Typically passed as var graphs = {{ graphJSON | safe }};
    # or Plotly.newPlot('chart', {{ graphJSON | safe }}, {});
    # Let's look for the JSON structure
    
    # Search for the JSON object directly if meaningful
    # Or search for "data": and see what follows
    
    match = re.search(r'var graph = ({.*?});', html, re.DOTALL)
    if match:
        json_str = match.group(1)
        try:
            data = json.loads(json_str)
            if 'data' in data and len(data['data']) > 0:
                trace = data['data'][0]
                print(f"X (Values first 3): {trace.get('x')[:3]}")
                print(f"Y (Cntry first 3): {trace.get('y')[:3]}")
                print(f"Orientation: {trace.get('orientation')}")
                
                # Check for numerical correctness
                x_vals = trace.get('x', [])
                if x_vals and isinstance(x_vals[0], (int, float)) and x_vals[0] > 1000:
                    print("PASS: Values look like GDP (large numbers).")
                else:
                    print(f"FAIL: Values look incorrect: {x_vals[:5]}")
            else:
                print("FAIL: JSON found but no data trace.")
        except json.JSONDecodeError as e:
            print(f"FAIL: JSON Decode Error: {e}")
            # Print snippet
            print(f"Snippet: {json_str[:200]}")
    else:
        print("FAIL: Could not find 'var graphs = ...' pattern in HTML.")
        # Fallback search for Plotly.newPlot
        # The template typically does `var graphs = {{ graphJSON | safe }};`
        # Let's check stat_detail.html structure if I can view it?
        # I previously viewed it? Let's check current file.
        pass

except Exception as e:
    print(f"Error fetching: {e}")
