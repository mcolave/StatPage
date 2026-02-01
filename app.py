from flask import Flask, render_template, request, jsonify
from charts.factory import (create_gdp_chart, create_population_chart, create_covid_chart, 
                            create_co2_chart, create_life_expectancy_chart, create_inflation_chart)
from chatbot.engine import ChatEngine

app = Flask(__name__)
chat_engine = ChatEngine()

@app.route("/")
def index():
    from charts.factory import create_trends_map
    map_json = create_trends_map()
    return render_template("index.html", mapJSON=map_json)

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message", "")
    response = chat_engine.process_query(user_msg)
    return jsonify({"response": response})

@app.route("/gdp")
def gdp():
    chart_json = create_gdp_chart()
    return render_template("gdp.html", graphJSON=chart_json)

@app.route("/population")
def population():
    chart_json = create_population_chart()
    return render_template("population.html", graphJSON=chart_json)

@app.route("/covid")
def covid():
    chart_json = create_covid_chart()
    return render_template("covid.html", graphJSON=chart_json)

@app.route("/co2")
def co2():
    chart_json = create_co2_chart()
    return render_template("co2.html", graphJSON=chart_json)

@app.route("/life-expectancy")
def life_expectancy():
    chart_json = create_life_expectancy_chart()
    return render_template("life_expectancy.html", graphJSON=chart_json)

@app.route("/inflation")
def inflation():
    chart_json = create_inflation_chart()
    return render_template("inflation.html", graphJSON=chart_json)

@app.route("/internet")
def internet():
    # Pass data directly for list view
    from data_loader import load_internet_data
    df = load_internet_data()
    data = df.head(20).to_dict(orient='records')
    return render_template("internet.html", data=data)

@app.route("/forest")
def forest():
    from data_loader import load_forest_data
    df = load_forest_data()
    data = df.head(20).to_dict(orient='records')
    return render_template("forest.html", data=data)

@app.route("/literacy")
def literacy():
    from data_loader import load_literacy_data
    df = load_literacy_data()
    data = df.head(20).to_dict(orient='records')
    return render_template("literacy.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)