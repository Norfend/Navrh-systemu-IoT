import plotly.graph_objs as go
import plotly.io as pio

def generate_temperature_graph(data):
    if not data:
        return None

    timestamps = [entry["timestamp"] for entry in data]
    temperatures = [entry["temperature"] for entry in data]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=timestamps, y=temperatures, mode='lines+markers', name='Temperature'))

    fig.update_layout(
        title='Temperature Over Time',
        xaxis_title='Time',
        yaxis_title='Temperature (°C)',
        margin=dict(l=20, r=20, t=30, b=20)
    )

    return pio.to_html(fig, full_html=False)