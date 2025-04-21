from flask import render_template, redirect, url_for, session, jsonify


def dashboard(data_base):
    if 'username' not in session:
        return redirect(url_for('login_controller'))

    latest = data_base.get_latest()
    last_15 = data_base.get_last_15()

    return render_template("dashboard.html", latest=latest, measurements=last_15)

def delete_oldest(data_base):
    try:
        data_base.delete_oldest()
        return jsonify({'success': True, 'message': 'Oldest entry deleted successfully.'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400