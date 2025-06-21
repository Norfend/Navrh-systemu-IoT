import time

from flask import jsonify, make_response
from flask_login import login_required

from service.dashboard_service import dashboard_service, update_table


def all_routes(app, limiter):
    @app.route("/dashboard", methods=["GET"])
    @login_required
    def dashboard_controller():
        return dashboard_service()

    @app.route("/update_table", methods=["GET"])
    @limiter.limit("5 per hour")
    @login_required
    def update_table_controller():
        limits = limiter.current_limit
        remaining = limits.remaining
        reset_time = limits.reset_at

        reset_in = int((reset_time - time.time()))

        response = make_response(update_table())
        response.headers['X-RateLimit-Limit'] = limits.limit
        response.headers['X-RateLimit-Remaining'] = remaining
        response.headers['X-RateLimit-Reset'] = reset_in
        return response

    @app.errorhandler(429)
    def ratelimit_handler(e):
        limits = limiter.current_limit
        reset_time = limits.reset_at
        reset_in = int((reset_time - time.time()))

        response = jsonify({
            "error": "rate limit exceeded",
            "message": str(e.description)
        })

        response.headers['X-RateLimit-Limit'] = limits.limit
        response.headers['X-RateLimit-Remaining'] = 0
        response.headers['X-RateLimit-Reset'] = reset_in

        return response, 429