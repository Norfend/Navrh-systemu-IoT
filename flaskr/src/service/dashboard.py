from flask import render_template, request, json

from repository.temperature_repository import get_last_temperature, get_last_temperatures
from service.graph import generate_temperature_graph


def dashboard():
    latest = json.loads(get_last_temperature()[0].get_data(as_text=True))
    measurements = json.loads(get_last_temperatures(15)[0].get_data(as_text=True))
    if measurements:
        graph_html = generate_temperature_graph(measurements)
    else:
        graph_html = None

    return render_template(
        "dashboard.html",
        latest=latest,
        measurements=measurements,
        graph_html=graph_html
    )

def update_table():
    count = int(request.args.get('count', 15))
    measurements = json.loads(get_last_temperatures(count)[0].get_data(as_text=True))
    return render_template('partials/table.html', measurements=measurements)