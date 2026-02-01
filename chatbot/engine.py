import re
import os
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
from data_loader import (load_gdp_data, load_population_data, load_covid_data, 
                           load_co2_data, load_life_expectancy_data, load_inflation_data,
                           load_internet_data, load_forest_data, load_literacy_data)

# Load environment variables
load_dotenv()

class ChatEngine:
    def __init__(self):
        self.data_sources = {
            'gdp': load_gdp_data,
            'population': load_population_data,
            'co2': load_co2_data,
            'life expectancy': load_life_expectancy_data,
            'inflation': load_inflation_data,
            'covid': load_covid_data,
            'internet usage': load_internet_data,
            'forest area': load_forest_data,
            'literacy rate': load_literacy_data
        }
        # Pre-load data
        self.cache = {}
        for key, func in self.data_sources.items():
            self.cache[key] = func()
            
        # Configure AI
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            
            # Dynamic Model Selection
            # Find the first available model that supports generation
            valid_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            gemini_models = [m for m in valid_models if 'gemini' in m.lower()]
            
            if gemini_models:
                # Prefer 1.5-flash if available, otherwise take the first one
                preferred = next((m for m in gemini_models if '1.5-flash' in m), gemini_models[0])
                print(f"Using AI Model: {preferred}")
                self.model = genai.GenerativeModel(preferred)
            else:
                print("No valid Gemini models found. Using regex fallback.")
                self.model = None
                self.api_key = None # Disable AI
        else:
            print("WARNING: GEMINI_API_KEY not found. Chatbot will use regex fallback.")

    def _build_context(self):
        """Creates a text summary of the current data for the AI."""
        context = "Here is the available statistical data:\n\n"
        
        for metric, df in self.cache.items():
            if df.empty: continue
            
            context += f"--- {metric.upper()} (Top 10) ---\n"
            # Convert top 10 rows to string
            context += df.head(10).to_string(index=False)
            context += "\n\n"
            
        return context

    def process_query(self, message):
        # 1. Try AI if available
        if self.api_key:
            try:
                return self.process_query_with_llm(message)
            except Exception as e:
                return f"AI Error: {e}. Falling back to basic search."
        
        # 2. Fallback to Regex (Basic)
        return self.process_query_regex(message)

    def process_query_with_llm(self, message):
        context = self._build_context()
        prompt = f"""
        You are a helpful data assistant for a statistics website.
        Use the provided data to answer the user's question accurately.
        If the answer is not in the data, verify if you can infer it or politely say you don't have that specific info.
        Keep answers concise and friendly.
        
        DATA CONTEXT:
        {context}
        
        USER QUESTION: "{message}"
        
        ANSWER:
        """
        
        response = self.model.generate_content(prompt)
        return response.text

    def process_query_regex(self, message):
        message = message.lower()
        
        # Intent: Top X [Metric]
        match_top = re.search(r'top (\d+)\s*(biggest|highest)?\s*(gdp|population|co2|inflation|life expectancy)', message)
        if match_top:
            limit = int(match_top.group(1))
            metric = match_top.group(3)
            return self.get_top_rankings_regex(metric, limit)

        # Intent: [Metric] of [Country]
        match_specific = re.search(r'(gdp|population|co2|inflation|life expectancy)\s*(of|in)\s*([a-z\s]+)', message)
        if match_specific:
            metric = match_specific.group(1)
            country = match_specific.group(3).strip()
            return self.get_country_stat_regex(metric, country)

        if 'hello' in message or 'hi' in message:
            return "Hello! I can help you with global statistics. Try asking 'Top 5 GDP' or 'Population of China'."
        
        return "I'm not sure I understand. Try asking for 'Top 3 GDP' or 'Inflation in USA' (or add a GEMINI_API_KEY for smarter answers)."

    def get_top_rankings_regex(self, metric, limit):
        df = self.cache.get(metric)
        if df is None or df.empty: return f"data not found for {metric}"
        
        limit = min(limit, 10)
        col_map = {'gdp': 'GDP', 'population': 'Population', 'co2': 'CO2', 'life expectancy': 'LifeExpectancy', 'inflation': 'Inflation'}
        val_col = col_map.get(metric)
        
        response = f"Top {limit} {metric.upper()}:\n"
        for i, row in df.head(limit).iterrows():
            response += f"{i+1}. {row['Country']}: {row[val_col]}\n"
        return response

    def get_country_stat_regex(self, metric, country_query):
        df = self.cache.get(metric)
        if df is None or df.empty: return f"data not found for {metric}"
        
        found = df[df['Country'].str.lower().str.contains(country_query, regex=False)]
        if found.empty: return f"Data not found for '{country_query}' in {metric}."
        
        col_map = {'gdp': 'GDP', 'population': 'Population', 'co2': 'CO2', 'life expectancy': 'LifeExpectancy', 'inflation': 'Inflation'}
        row = found.iloc[0]
        return f"{metric} of {row['Country']}: {row[col_map.get(metric)]}"
