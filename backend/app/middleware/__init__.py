"""
Application middleware for MediLink backend.
"""

from flask import request
import time


def setup_middleware(app):
    """Register request hooks and performance headers."""
    @app.before_request
    def before_request_hook():
        request.start_time = time.time()

    @app.after_request
    def after_request_hook(response):
        if hasattr(request, "start_time"):
            duration = round((time.time() - request.start_time) * 1000, 2)
            response.headers["X-Response-Time-Ms"] = str(duration)
        response.headers["X-Project"] = "MediLink"
        return response
