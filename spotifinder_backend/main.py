import os

from aiohttp import web
from aiohttp.web_middlewares import normalize_path_middleware

from spotifinder_backend.infrastructure.server import http
from spotifinder_backend.usecases.constants import *


def on_startup():
    """Return a startup handler that will bootstrap and then begin background tasks."""

    async def startup_handler(app):
        """Run all initialization tasks.
        These are tasks that should be run after the event loop has been started but before the HTTP
        server has been started.
        """

        spotify_client_id = os.environ.get(SPOTIFY_CLIENT_ID)
        spotify_client_secret = os.environ.get(SPOTIFY_CLIENT_SECRET)

        # Save dependencies in the HTTP app.
        http.register_dependency(app, SPOTIFY_CLIENT_ID, spotify_client_id)
        http.register_dependency(app, SPOTIFY_CLIENT_SECRET, spotify_client_secret)

        async def cleanup(app):
            """Perform required cleanup on shutdown"""
            # await client_session.close()

        app.on_shutdown.append(cleanup)

    return startup_handler


def main():
    app = web.Application(
        middlewares=[normalize_path_middleware(append_slash=False, remove_slash=True)]
    )
    http.configure_app(app, on_startup())
    port = int(os.environ.get("PORT", 8080))
    web.run_app(app, host="0.0.0.0", port=port)
