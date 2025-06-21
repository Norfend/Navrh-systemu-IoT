import logging

import plotly.graph_objs as go
import plotly.io as pio

module_logger = logging.getLogger(__name__)

def generate_temperature_graph(data):
    module_logger.debug("Generating temperature graph from data")
    if not all("receiving_timestamp" in entry for entry in data):
        module_logger.warning("Missing 'receiving_timestamp' in one or more data entries")
        return None

    receiving_timestamp = [entry["receiving_timestamp"] for entry in data]
    temperatures = [entry["temperature"] for entry in data]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=receiving_timestamp, y=temperatures, mode='lines+markers', name='Temperature'))

    fig.update_layout(
        title='Temperature Over Time',
        xaxis_title='Time',
        yaxis_title='Temperature (°C)',
        margin=dict(l=20, r=20, t=30, b=20)
    )

    module_logger.info("Temperature graph generated successfully")
    return pio.to_html(fig, full_html=False)