from flask import render_template, redirect, url_for, session, jsonify, request
from service.graph import generate_temperature_graph


def dashboard(data_base):
    if 'username' not in session:
        return redirect(url_for('login_controller'))

    latest = data_base.get_latest()
    measurements = data_base.get_last_measurements(15)
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

def update_table(data_base):
    count = int(request.args.get('count', 15))
    measurements = data_base.get_last_measurements(limit=count)
    return render_template('partials/table.html', measurements=measurements)

def delete_oldest(data_base):
    try:
        data_base.delete_oldest()
        return jsonify({'success': True, 'message': 'Oldest entry deleted successfully.'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400