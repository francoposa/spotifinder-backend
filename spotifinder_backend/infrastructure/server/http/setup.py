"""
Setup functions for HTTP server.
"""

import aiohttp_cors

from spotifinder_backend.infrastructure.server.http.handlers import health, spotify
from spotifinder_backend.infrastructure.server.http.errors import ERROR_HANDLERS


HEALTH = "/health"
INFO = "/info"
ANALYZE = "/analyze"


def _setup_routes(app):
    """Add routes to the given aiohttp app."""

    # Default cors settings.
    cors = aiohttp_cors.setup(
        app,
        defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True, expose_headers="*", allow_headers="*"
            )
        },
    )

    # Health check.
    app.router.add_get(HEALTH, health.health_check)

    # Metadata.
    app.router.add_get(INFO, health.info)

    # Spotify resource analysis
    app.router.add_get(ANALYZE, spotify.get_resource_analysis)


def configure_app(app, startup_handler):
    """Configure the web.Application."""

    _setup_routes(app)

    # Schedule custom startup routine.
    app.on_startup.append(startup_handler)


def register_dependency(app, constant_key, dependency, usecase=None):
    """Add dependencies used by the HTTP handlers."""

    if usecase is None:
        app[constant_key] = dependency
    else:
        if constant_key not in app:
            app[constant_key] = {}
        app[constant_key][usecase] = dependency