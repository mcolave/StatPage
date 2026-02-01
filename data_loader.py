import requests
import json
import os
import pandas as pd
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

HEADERS = {'User-Agent': 'StatPage/1.0'}

def _fetch_world_bank_data(indicator, filename, sort_desc=True):
    """Helper to fetch and filter World Bank Data."""
    # format=json, per_page=300 to get enough countries, mrnev=1 (most recent non-empty value)
    url = f"http://api.worldbank.org/v2/country/all/indicator/{indicator}?format=json&mrnev=1&per_page=300"
    filepath = os.path.join(DATA_DIR, filename)
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        # 400 bad request might happen if params are wrong, but we fixed them.
        if response.status_code != 200:
             # Fallback to simple URL if advanced params fail (sometimes WB API is finicky)
             url = f"http://api.worldbank.org/v2/country/all/indicator/{indicator}?format=json&per_page=100"
             response = requests.get(url, headers=HEADERS, timeout=10)
             
        response.raise_for_status()
        raw_data = response.json()
        
        if len(raw_data) < 2:
            raise ValueError("Invalid API response format")
            
        data = raw_data[1]
        
        # Process and Filter
        processed_data = []
        for entry in data:
            if entry['value'] is None:
                continue
                
            country_name = entry['country']['value']
            
            # Common WB Aggregates to exclude
            blocklist = [
                "World", "High income", "OECD members", "North America", "European Union", 
                "East Asia & Pacific", "Europe & Central Asia", "Latin America & Caribbean",
                "Middle East & North Africa", "South Asia", "Sub-Saharan Africa",
                "Low & middle income", "Upper middle income", "Lower middle income", 
                "Late-demographic dividend", "Post-demographic dividend", "Early-demographic dividend",
                "IDA & IBRD total", "IBRD only", "IDA total", "Euro area", "Arab World", "Small states",
                "Africa Eastern and Southern", "Africa Western and Central"
            ]
            
            if any(blk in country_name for blk in blocklist):
                continue
                
            processed_data.append({
                "Country": country_name,
                "Value": entry['value']
            })
        
        # Sort
        processed_data.sort(key=lambda x: x['Value'], reverse=sort_desc)
        top_data = processed_data[:20] # Keep top 20
        
        # Save cache
        with open(filepath, 'w') as f:
            json.dump(top_data, f)
            
        return pd.DataFrame(top_data)

    except Exception as e:
        print(f"Error fetching {indicator}: {e}. Loading from cache.")
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return pd.DataFrame(json.load(f))
        return pd.DataFrame()

def load_gdp_data():
    """Fetch GDP (NY.GDP.MKTP.CD)."""
    df = _fetch_world_bank_data("NY.GDP.MKTP.CD", "gdp.json")
    if not df.empty:
        df = df.rename(columns={"Value": "GDP"})
    return df

def load_co2_data():
    """Fetch CO2 emissions (metric tons per capita) (EN.ATM.CO2E.PC)."""
    df = _fetch_world_bank_data("EN.ATM.CO2E.PC", "co2.json")
    if not df.empty:
        df = df.rename(columns={"Value": "CO2"})
    return df

def load_life_expectancy_data():
    """Fetch Life Expectancy at birth (SP.DYN.LE00.IN)."""
    df = _fetch_world_bank_data("SP.DYN.LE00.IN", "life_expectancy.json")
    if not df.empty:
        df = df.rename(columns={"Value": "LifeExpectancy"})
    return df

def load_inflation_data():
    """Fetch Inflation, consumer prices (annual %) (FP.CPI.TOTL.ZG)."""
    df = _fetch_world_bank_data("FP.CPI.TOTL.ZG", "inflation.json")
    if not df.empty:
        df = df.rename(columns={"Value": "Inflation"})
    return df

def load_population_data():
    """Fetch Population data from RestCountries API or fallback."""
    url = "https://restcountries.com/v3.1/all?fields=name,population,flags"
    filepath = os.path.join(DATA_DIR, 'population.json')
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        processed_data = []
        for entry in data:
            if 'name' not in entry or 'common' not in entry['name']: continue
            processed_data.append({
                "Country": entry['name']['common'],
                "Population": entry['population']
            })
            
        processed_data.sort(key=lambda x: x['Population'], reverse=True)
        top_10 = processed_data[:10]
        
        with open(filepath, 'w') as f:
            json.dump(top_10, f)
            
        return pd.DataFrame(top_10)

    except Exception as e:
        print(f"Error fetching Population data: {e}. Loading from cache.")
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return pd.DataFrame(json.load(f))
        return pd.DataFrame()

def load_covid_data():
    """Fetch Global Covid History from disease.sh or fallback."""
    url = "https://disease.sh/v3/covid-19/historical/all?lastdays=all"
    filepath = os.path.join(DATA_DIR, 'covid.json')
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        with open(filepath, 'w') as f:
            json.dump(data, f)
            
        cases_dict = data['cases']
        dates = list(cases_dict.keys())
        counts = list(cases_dict.values())
        
        df = pd.DataFrame({'Date': dates, 'Cases': counts})
        df['Date'] = pd.to_datetime(df['Date'])
        return df

    except Exception as e:
        print(f"Error fetching Covid data: {e}. Loading from cache.")
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                data = json.load(f)
                cases_dict = data['cases']
                return pd.DataFrame({'Date': pd.to_datetime(list(cases_dict.keys())), 'Cases': list(cases_dict.values())})
        return pd.DataFrame()

def load_internet_data():
    """Fetch Internet Usage % (IT.NET.USER.ZS)."""
    df = _fetch_world_bank_data("IT.NET.USER.ZS", "internet.json")
    if not df.empty:
        df = df.rename(columns={"Value": "InternetUsage"})
    return df

def load_forest_data():
    """Fetch Forest Area % (AG.LND.FRST.ZS)."""
    df = _fetch_world_bank_data("AG.LND.FRST.ZS", "forest.json")
    if not df.empty:
        df = df.rename(columns={"Value": "ForestArea"})
    return df

def load_literacy_data():
    """Fetch Literacy Rate % (SE.ADT.LITR.ZS)."""
    df = _fetch_world_bank_data("SE.ADT.LITR.ZS", "literacy.json")
    if not df.empty:
        df = df.rename(columns={"Value": "LiteracyRate"})
    return df

def load_trends_data():
    """Load simulated Google Trends data."""
    filepath = os.path.join(DATA_DIR, 'trends.json')
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            data = json.load(f)
        return pd.DataFrame(data)
    return pd.DataFrame()
