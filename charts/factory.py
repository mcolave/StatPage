import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import json
import plotly
from data_loader import (load_gdp_data, load_population_data, load_covid_data, 
                           load_co2_data, load_life_expectancy_data, load_inflation_data)

def create_gdp_chart():
    df = load_gdp_data()
    
    if df.empty:
        return json.dumps({}, cls=plotly.utils.PlotlyJSONEncoder)

    fig = px.bar(
        df, 
        x='Country', 
        y='GDP',
        title="Top 10 Countries by GDP (USD)",
        color='GDP',
        color_continuous_scale='Bluyl'
    )
    
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif"),
        margin=dict(t=50, l=25, r=25, b=25)
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_population_chart():
    df = load_population_data()
    
    if df.empty:
        return json.dumps({}, cls=plotly.utils.PlotlyJSONEncoder)

    fig = px.pie(
        df, 
        values='Population', 
        names='Country', 
        title='Global Population Distribution (Top 10)',
        hole=0.4
    )
    
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif")
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_covid_chart():
    df = load_covid_data()
    
    if df.empty:
        return json.dumps({}, cls=plotly.utils.PlotlyJSONEncoder)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Date'], 
        y=df['Cases'], 
        mode='lines',
        name='Cases',
        line=dict(color='#ff5858', width=3),
        fill='tozeroy'
    ))
    
    fig.update_layout(
        title='Global COVID-19 Cases Trend (Cumulative)',
        xaxis_title='Date',
        yaxis_title='Total Cases',
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif")
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_co2_chart():
    df = load_co2_data()
    if df.empty: return json.dumps({}, cls=plotly.utils.PlotlyJSONEncoder)

    fig = px.bar(
        df[:15], 
        x='Country', 
        y='CO2',
        title="Top CO2 Emissions (Metric Tons Per Capita)",
        color='CO2',
        color_continuous_scale='Redor'
    )
    
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif")
    )
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_life_expectancy_chart():
    df = load_life_expectancy_data()
    if df.empty: return json.dumps({}, cls=plotly.utils.PlotlyJSONEncoder)

    fig = px.bar(
        df[:15], 
        x='Country', 
        y='LifeExpectancy',
        title="Life Expectancy at Birth (Years)",
        color='LifeExpectancy',
        color_continuous_scale='Tealgrn'
    )
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif")
    )
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_inflation_chart():
    df = load_inflation_data()
    if df.empty: return json.dumps({}, cls=plotly.utils.PlotlyJSONEncoder)

    fig = px.bar(
        df[:15], 
        x='Country', 
        y='Inflation',
        title="Inflation Rate (Consumer Prices %)",
        color='Inflation',
        color_continuous_scale='Magma'
    )
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif")
    )
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_trends_map():
    from data_loader import load_trends_data
    df = load_trends_data()
    
    if df.empty: 
        return json.dumps({}, cls=plotly.utils.PlotlyJSONEncoder)

    fig = px.choropleth(
        df,
        locations="ISO",
        color="Country",
        hover_name="Country",
        hover_data={"Trends": True, "ISO": False, "Country": False},
        title="<b>Global Trending Searches</b> (Hover to view)",
        projection="natural earth"
    )
    
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        geo=dict(
            bgcolor='rgba(0,0,0,0)',
            showocean=True,
            oceancolor="#0d1117",
            showlakes=True,
            lakecolor="#0d1117",
            showland=True,
            landcolor="#161b22"
        ),
        font=dict(family="Inter, sans-serif"),
        showlegend=False,
        margin=dict(l=0, r=0, t=50, b=0),
        height=500
    )
    
    fig.update_traces(
        hovertemplate="<b>%{hovertext}</b><br><br>%{customdata[0]}<extra></extra>"
    )

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def create_generic_chart(df, chart_type, title, color_column, color_scale='Viridis', orientation='v'):
    """Generates a chart dynamically based on parameters."""
    if df.empty:
        return json.dumps({}, cls=plotly.utils.PlotlyJSONEncoder)

    if chart_type == 'bar':
        df_plot = df[:15].copy() # Work on a copy
        
        # Determine Year for Title
        # Check if 'Year' column exists (it should now)
        year_str = ""
        if 'Year' in df_plot.columns and not df_plot['Year'].isnull().all():
            # Get most common year
            mode_year = df_plot['Year'].mode()
            if not mode_year.empty:
                year_str = f" ({mode_year[0]})"
            else:
                # If mixed, maybe range? or just first
                year_str = f" ({df_plot['Year'].iloc[0]})"
        
        final_title = f"{title}{year_str}"
        
        # Prepare data for go.Bar
        if orientation == 'h':
            x_data = df_plot['Value'].tolist()
            y_data = df_plot['Country'].tolist()
            text_template = '%{x:.2s}'
            
            # DEBUG LOG
            try:
                with open("chart_debug.log", "a") as f:
                    f.write(f"Chart: {title}\n")
                    f.write(f"Orientation: {orientation}\n")
                    f.write(f"X Data (Values): {x_data[:5]}\n")
                    f.write(f"Y Data (Country): {y_data[:5]}\n")
                    f.write("-" * 20 + "\n")
            except: pass
            
        else:
            x_data = df_plot['Country'].tolist()
            y_data = df_plot['Value'].tolist()
            text_template = '%{y:.2s}'

        fig = go.Figure(go.Bar(
            x=x_data,
            y=y_data,
            orientation=orientation,
            texttemplate=text_template,
            textposition='auto',
            marker=dict(
                color=df_plot['Value'],
                colorscale=color_scale,
                showscale=True
            )
        ))
        
        fig.update_layout(
            title=final_title,
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter, sans-serif"),
            margin=dict(t=50, l=25, r=25, b=25)
        )

        if orientation == 'h':
             fig.update_layout(yaxis={'categoryorder':'total ascending'})
            
    elif chart_type == 'pie':
        fig = px.pie(
            df[:10], 
            values='Value', 
            names='Country', 
            title=title,
            hole=0.4
        )
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter, sans-serif")
        )

    else:
        return json.dumps({}, cls=plotly.utils.PlotlyJSONEncoder)
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
