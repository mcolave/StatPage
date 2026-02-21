
# Configuration for Global Statistics
# Add new stats here to automatically generate pages and cards.

STATS = [
    {
        "id": "gdp",
        "title": "GDP Rankings",
        "menu_title": "GDP",
        "desc": "Compare the economic output of top nations.",
        "indicator": "NY.GDP.MKTP.CD",
        "chart_title": "Top Countries by GDP (USD)",
        "color_scale": "Bluyl",
        "value_format": "${:,.2f}", # Python format string
        "type": "bar",
        "category": "Global Economy"
    },
    {
        "id": "population",
        "title": "World Population",
        "menu_title": "Population",
        "desc": "Visualize the distribution of human population.",
        "indicator": "SP.POP.TOTL",  # or custom source, handled via type='pie' specialized logic if needed, but let's try generic
        "chart_title": "Global Population Distribution",
        "color_scale": "Turbo",
        "type": "pie",
        "custom_data_func": "load_population_data", # Special case for RestCountries API
        "category": "Global Society"
    },
    {
        "id": "co2",
        "title": "CO2 Emissions",
        "menu_title": "CO2",
        "desc": "Top countries by CO2 emissions per capita.",
        "indicator": "EN.ATM.CO2E.PC",
        "chart_title": "Top CO2 Emissions (Metric Tons Per Capita)",
        "color_scale": "Redor",
        "type": "bar",
        "category": "Global Environment"
    },
    {
        "id": "life_exp",
        "title": "Life Expectancy",
        "menu_title": "Life Exp.",
        "desc": "Global life expectancy at birth.",
        "indicator": "SP.DYN.LE00.IN",
        "chart_title": "Life Expectancy at Birth (Years)",
        "color_scale": "Tealgrn",
        "type": "bar",
        "category": "Global Society"
    },
    {
        "id": "inflation",
        "title": "Global Inflation",
        "menu_title": "Inflation",
        "desc": "Countries with highest inflation rates.",
        "indicator": "FP.CPI.TOTL.ZG",
        "chart_title": "Inflation Rate (Consumer Prices %)",
        "color_scale": "Magma",
        "type": "bar",
        "category": "Global Economy"
    },
    {
        "id": "gdp_growth",
        "title": "GDP Growth",
        "menu_title": "GDP Growth",
        "desc": "Annual percentage growth rate of GDP.",
        "indicator": "NY.GDP.MKTP.KD.ZG",
        "chart_title": "GDP Growth (Annual %)",
        "color_scale": "Greens",
        "type": "bar",
        "category": "Global Economy"
    },
    {
        "id": "unemployment",
        "title": "Unemployment Rate",
        "menu_title": "Unemployment",
        "desc": "Share of labor force that is without work.",
        "indicator": "SL.UEM.TOTL.ZS",
        "chart_title": "Unemployment Rate (% of Labor Force)",
        "color_scale": "Reds",
        "type": "bar",
        "category": "Global Economy"
    },
    {
        "id": "exports",
        "title": "Exports (% of GDP)",
        "menu_title": "Exports",
        "desc": "Exports of goods and services as % of GDP.",
        "indicator": "NE.EXP.GNFS.ZS",
        "chart_title": "Exports (% of GDP)",
        "color_scale": "Blues",
        "type": "bar",
        "category": "Global Economy"
    },
    {
        "id": "internet",
        "title": "Internet Usage",
        "menu_title": "Internet",
        "desc": "Top connected countries.",
        "indicator": "IT.NET.USER.ZS",
        "chart_title": "Internet Usage (%)",
        "type": "list",
        "category": "Global Society"
    },
    {
        "id": "forest",
        "title": "Forest Cover",
        "menu_title": "Forest",
        "desc": "Greenest countries by forest area.",
        "indicator": "AG.LND.FRST.ZS",
        "chart_title": "Forest Area (%)",
        "type": "list",
        "category": "Global Environment"
    },
    {
        "id": "literacy",
        "title": "Literacy Rates",
        "menu_title": "Literacy",
        "desc": "Countries with highest literacy.",
        "indicator": "SE.ADT.LITR.ZS",
        "chart_title": "Literacy Rate (%)",
        "type": "list",
        "category": "Global Society"
    },

    {
        "id": "urban_pop",
        "title": "Urban Population",
        "menu_title": "Urban Pop",
        "desc": "Percentage of population living in urban areas.",
        "indicator": "SP.URB.TOTL.IN.ZS",
        "chart_title": "Urban Population (% of Total)",
        "color_scale": "Purples",
        "type": "bar",
        "category": "Global Society"
    },
    # SE ASIA STATS
    {
        "id": "sea_gdp_cap",
        "title": "SE Asia GDP Per Capita",
        "menu_title": "SEA GDP/Cap",
        "desc": "GDP Per Capita for Southeast Asian nations.",
        "indicator": "NY.GDP.PCAP.CD",
        "chart_title": "GDP Per Capita (USD) - Southeast Asia",
        "color_scale": "Plasma",
        "type": "bar",
        "orientation": "h", # Use horizontal bars
        "filter_region": "sea", # Custom filter tag
        "category": "Southeast Asia"
    },
    {
        "id": "sea_pop",
        "title": "SE Asia Population",
        "menu_title": "SEA Pop.",
        "desc": "Population of Southeast Asian nations.",
        "indicator": "SP.POP.TOTL",
        "chart_title": "Population - Southeast Asia",
        "color_scale": "Viridis",
        "type": "bar",
        "orientation": "h",
        "filter_region": "sea",
        "category": "Southeast Asia"
    },
    {
        "id": "sea_life_exp",
        "title": "SE Asia Life Expectancy",
        "menu_title": "SEA Life Exp.",
        "desc": "Life Expectancy at Birth in Southeast Asia.",
        "indicator": "SP.DYN.LE00.IN",
        "chart_title": "Life Expectancy (Years) - Southeast Asia",
        "color_scale": "Tealgrn",
        "type": "bar",
        "orientation": "h",
        "filter_region": "sea",
        "category": "Southeast Asia"
    },
    {
        "id": "sea_internet",
        "title": "SE Asia Internet Usage",
        "menu_title": "SEA Internet",
        "desc": "Internet connectivity in Southeast Asia.",
        "indicator": "IT.NET.USER.ZS",
        "chart_title": "Internet Usage (%) - Southeast Asia",
        "color_scale": "Electric",
        "type": "bar",
        "orientation": "h",
        "filter_region": "sea",
        "category": "Southeast Asia"
    },
    {
        "id": "sea_co2",
        "title": "SE Asia CO2 Emissions",
        "menu_title": "SEA CO2",
        "desc": "Carbon Emissions per capita in Southeast Asia.",
        "indicator": "EN.ATM.CO2E.PC",
        "chart_title": "CO2 Emissions (Metric Tons/Capita) - SE Asia",
        "color_scale": "Redor",
        "type": "bar",
        "orientation": "h",
        "filter_region": "sea",
        "category": "Southeast Asia"
    },
    # NEW GLOBAL STATS
    {
        "id": "mobile_subs",
        "title": "Mobile Subscriptions",
        "menu_title": "Mobile Subs",
        "desc": "Mobile cellular subscriptions per 100 people.",
        "indicator": "IT.CEL.SETS.P2",
        "chart_title": "Mobile Subscriptions (per 100 people)",
        "color_scale": "Viridis",
        "type": "bar",
        "category": "Global Society"
    },
    {
        "id": "electricity_access",
        "title": "Electricity Access",
        "menu_title": "Electricity Access",
        "desc": "Access to electricity (% of population).",
        "indicator": "EG.ELC.ACCS.ZS",
        "chart_title": "Access to Electricity (% of Population)",
        "color_scale": "YlOrRd",
        "type": "bar",
        "category": "Global Society"
    },
    {
        "id": "renewable_energy",
        "title": "Renewable Energy",
        "menu_title": "Renewable Energy",
        "desc": "Renewable energy consumption (% of total final energy consumption).",
        "indicator": "EG.FEC.RNEW.ZS",
        "chart_title": "Renewable Energy Consumption (%)",
        "color_scale": "Greens",
        "type": "bar",
        "category": "Global Environment"
    },
    {
        "id": "air_quality",
        "title": "Air Quality (PM2.5)",
        "menu_title": "Air Quality",
        "desc": "PM2.5 air pollution, mean annual exposure.",
        "indicator": "EN.ATM.PM25.MC.M3",
        "chart_title": "PM2.5 Air Pollution (micrograms/m3)",
        "color_scale": "Reds",
        "type": "bar",
        "category": "Global Environment"
    },
    {
        "id": "hospital_beds",
        "title": "Hospital Beds",
        "menu_title": "Hospital Beds",
        "desc": "Hospital beds per 1,000 people.",
        "indicator": "SH.MED.BEDS.ZS",
        "chart_title": "Hospital Beds (per 1,000 people)",
        "color_scale": "Blues",
        "type": "bar",
        "category": "Global Society"
    },
    {
        "id": "health_expenditure",
        "title": "Out-of-Pocket Health Cost",
        "menu_title": "Health Cost",
        "desc": "Out-of-pocket expenditure (% of current health expenditure).",
        "indicator": "SH.XPD.OOPC.CH.ZS",
        "chart_title": "Out-of-Pocket Health Expenditure (%)",
        "color_scale": "Oranges",
        "type": "bar",
        "category": "Global Society"
    },
    # NEW SE ASIA STATS
    {
        "id": "sea_mobile_subs",
        "title": "SE Asia Mobile Subscriptions",
        "menu_title": "SEA Mobile Subs",
        "desc": "Mobile subscriptions per 100 people in SE Asia.",
        "indicator": "IT.CEL.SETS.P2",
        "chart_title": "Mobile Subscriptions (per 100 people) - SE Asia",
        "color_scale": "Viridis",
        "type": "bar",
        "orientation": "h",
        "filter_region": "sea",
        "category": "Southeast Asia"
    },
    {
        "id": "sea_electricity_access",
        "title": "SE Asia Electricity Access",
        "menu_title": "SEA Electricity Access",
        "desc": "Access to electricity (% of population) in SE Asia.",
        "indicator": "EG.ELC.ACCS.ZS",
        "chart_title": "Access to Electricity (%) - SE Asia",
        "color_scale": "YlOrRd",
        "type": "bar",
        "orientation": "h",
        "filter_region": "sea",
        "category": "Southeast Asia"
    },
    {
        "id": "sea_hospital_beds",
        "title": "SE Asia Hospital Beds",
        "menu_title": "SEA Hospital Beds",
        "desc": "Hospital beds per 1,000 people in SE Asia.",
        "indicator": "SH.MED.BEDS.ZS",
        "chart_title": "Hospital Beds (per 1,000 people) - SE Asia",
        "color_scale": "Blues",
        "type": "bar",
        "orientation": "h",
        "filter_region": "sea",
        "category": "Southeast Asia"
    }
]
# Define Regional Groups
SEA_COUNTRIES = [
    "Singapore", "Brunei Darussalam", "Malaysia", "Thailand", "Indonesia", 
    "Vietnam", "Philippines", "Lao PDR", "Cambodia", "Timor-Leste", "Myanmar"
]

# Helper to find stat by ID
def get_stat_config(stat_id):
    for s in STATS:
        if s['id'] == stat_id:
            return s
    return None

def get_region_countries(region_code):
    if region_code == 'sea':
        return SEA_COUNTRIES
    return None
