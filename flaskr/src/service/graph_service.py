import plotly.graph_objs as go
import plotly.io as pio

def generate_temperature_graph(data):
    if not all("receiving_timestamp" in entry for entry in data):
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


    return pio.to_html(fig, full_html=False)