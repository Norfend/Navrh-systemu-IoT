import logging

from flask import render_template, request, json

from service.graph_service import generate_temperature_graph
from service.temperature_service import get_last_temperature_service, get_last_temperatures_service
from utils.hardware_state import hardware_state as state

module_logger = logging.getLogger(__name__)

def dashboard_service():
    try:
        module_logger.debug("Request received to render dashboard")
        latest = json.loads(get_last_temperature_service()[0].get_data(as_text=True))
        measurements = json.loads(get_last_temperatures_service(15)[0].get_data(as_text=True))
        if measurements:
            graph_html = generate_temperature_graph(measurements)
            module_logger.debug("Dashboard: generated temperature graph")
        else:
            graph_html = None
            module_logger.debug("Dashboard: no measurements, skipping graph generation")

        return render_template(
            "dashboard.html",
            latest=latest,
            measurements=measurements,
            graph_html=graph_html,
            led_status=state["led"],
            measurement_status=state["measurement"],
            measurement_interval=state["interval"]
        )
    except Exception as e:
        module_logger.error(f"Exception in dashboard_service: {e}", exc_info=True)
        return render_template(
            "dashboard.html",
            latest=None,
            measurements=None,
            graph_html=None,
            led_status=False,
            measurement_status=False,
            measurement_interval=0
        )

def update_table():
    count = int(request.args.get('count', 15))
    module_logger.debug(f"Request received to update table with count={count}")
    measurements = json.loads(get_last_temperatures_service(count)[0].get_data(as_text=True))
    module_logger.debug("Rendered table partial successfully")
    return render_template('partials/table.html', measurements=measurements)