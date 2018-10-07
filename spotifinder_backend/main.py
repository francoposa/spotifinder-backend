import os

from aiohttp import web

from spotifinder_backend.infrastructure.server import http

def main():
	app = web.Application()
	http.configure_app(app)
	port = int(os.environ.get('PORT', 8080))
	web.run_app(app, host='127.0.0.1', port=port)
