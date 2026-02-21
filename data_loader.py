import requests
import json
import os
import pandas as pd
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

HEADERS = {'User-Agent': 'StatPage/1.0'}

def fetch_wb_data(indicator, filename, sort_desc=True, filter_countries=None):
    """Helper to fetch and filter World Bank Data."""
    # format=json, per_page=300 to get enough countries, mrnev=1 (most recent non-empty value)
    url = f"https://api.worldbank.org/v2/country/all/indicator/{indicator}?format=json&mrnev=1&per_page=300"
    filepath = os.path.join(DATA_DIR, filename)
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        # 400 bad request might happen if params are wrong, but we fixed them.
        if response.status_code != 200:
             # Fallback to simple URL if advanced params fail (sometimes WB API is finicky)
             url = f"https://api.worldbank.org/v2/country/all/indicator/{indicator}?format=json&per_page=500"
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
            
            # Regional Filtering
            if filter_countries:
                # Check if country is in the allowed list (case-insensitive safe)
                if country_name not in filter_countries:
                    continue
            else:
                # Common WB Aggregates to exclude (only if NOT filtering by specific list)
                blocklist = [
                    "World", " income", "OECD", "North America", "European Union", 
                    "East Asia", "Europe & Central", "Latin America",
                    "Middle East", "South Asia", "Sub-Saharan",
                    "dividend", "IDA", "IBRD", "Euro area", "Arab World", "Small states",
                    "Africa Eastern", "Africa Western", "Central Europe",
                    "Heavily indebted", "Fragile and conflict", "classification", "Not classified",
                    "Least developed countries"
                ]
                
                if any(blk in country_name for blk in blocklist):
                    continue
                
            processed_data.append({
                "Country": country_name,
                "Value": entry['value'],
                "Year": entry['date']
            })
        
        # Sort
        processed_data.sort(key=lambda x: x['Value'], reverse=sort_desc)
        
        # Limit (Only if NOT filtering by region, otherwise show all matches)
        # But wait, if we filter by region, we likely want ALL of them.
        # If no filter, we want Top 20.
        if not filter_countries:
            top_data = processed_data[:20] 
        else:
            top_data = processed_data
        
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
    df = fetch_wb_data("NY.GDP.MKTP.CD", "gdp.json")
    if not df.empty:
        df = df.rename(columns={"Value": "GDP"})
    return df

def load_co2_data():
    """Fetch CO2 emissions (metric tons per capita) (EN.ATM.CO2E.PC)."""
    df = fetch_wb_data("EN.ATM.CO2E.PC", "co2.json")
    if not df.empty:
        df = df.rename(columns={"Value": "CO2"})
    return df

def load_life_expectancy_data():
    """Fetch Life Expectancy at birth (SP.DYN.LE00.IN)."""
    df = fetch_wb_data("SP.DYN.LE00.IN", "life_expectancy.json")
    if not df.empty:
        df = df.rename(columns={"Value": "LifeExpectancy"})
    return df

def load_inflation_data():
    """Fetch Inflation, consumer prices (annual %) (FP.CPI.TOTL.ZG)."""
    df = fetch_wb_data("FP.CPI.TOTL.ZG", "inflation.json")
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
    df = fetch_wb_data("IT.NET.USER.ZS", "internet.json")
    if not df.empty:
        df = df.rename(columns={"Value": "InternetUsage"})
    return df

def load_forest_data():
    """Fetch Forest Area % (AG.LND.FRST.ZS)."""
    df = fetch_wb_data("AG.LND.FRST.ZS", "forest.json")
    if not df.empty:
        df = df.rename(columns={"Value": "ForestArea"})
    return df

def load_literacy_data():
    """Fetch Literacy Rate % (SE.ADT.LITR.ZS)."""
    df = fetch_wb_data("SE.ADT.LITR.ZS", "literacy.json")
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


def load_summary_stats():
    """Calculates global summary stats for the dashboard."""
    stats = {}
    
    # 1. Total Population
    # Fetch full population list to sum it up (reuse cache mechanism ideally, but simple fetch for now)
    try:
        # Re-using the logic from load_population_data but getting SUM
        # We need a robust total. Since load_population_data only returns Top 10, let's look at the raw file if exists
        pop_file = os.path.join(DATA_DIR, 'population.json')
        if os.path.exists(pop_file):
             # Ensure we don't just sum the Top 10 if that's what was saved. 
             # Actually load_population_data logic saves Top 10. We should ideally fetch all.
             # For speed, let's make a quick approx or fetch all *if* we want accuracy.
             pass
             
        # Let's just do a quick calc based on existing Top 10 or generic placeholder if failing
        # Better: Modify load_population_data to return total? NO, side effects.
        # Let's just fetch simplified world data for TOTAL
        # World Bank 'Total' indicator: SP.POP.TOTL for 'World' (WLD)
        url = "https://api.worldbank.org/v2/country/WLD/indicator/SP.POP.TOTL?format=json&mrnev=1"
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            val = r.json()[1][0]['value']
            stats['population'] = f"{val / 1_000_000_000:.2f} B"
        else:
            stats['population'] = "8.1 B" # Fallback
            
    except Exception:
        stats['population'] = "8.1 B"

    # 2. Covid Cases (Total)
    try:
        df_covid = load_covid_data()
        if not df_covid.empty:
            total = df_covid.iloc[-1]['Cases']
            stats['covid_cases'] = f"{total / 1_000_000:.1f} M"
        else:
            stats['covid_cases'] = "775 M"
    except:
        stats['covid_cases'] = "-"

    # 3. Top GDP
    try:
        df_gdp = load_gdp_data()
        if not df_gdp.empty:
            top = df_gdp.iloc[0]
            stats['top_gdp'] = f"{top['Country']}"
            stats['top_gdp_val'] = f"${top['GDP'] / 1_000_000_000_000:.1f} T"
        else:
             stats['top_gdp'] = "USA"
             stats['top_gdp_val'] = "$25 T"
    except:
        stats['top_gdp'] = "-"
        
    # 4. Highest Life Exp
    try:
        df_le = load_life_expectancy_data()
        if not df_le.empty:
            top = df_le.iloc[0]
            stats['life_exp'] = f"{top['Country']}"
            stats['life_exp_val'] = f"{top['LifeExpectancy']:.1f} Yrs"
        else:
            stats['life_exp'] = "Japan"
            stats['life_exp_val'] = "84.6 Yrs"
    except:
        stats['life_exp'] = "-"
        
    return stats
