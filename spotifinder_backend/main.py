import sys

from aiohttp import web

from spotifinder_backend.infrastructure.server import http

def main():
	app = web.Application()
	web.run_app(app, host='127.0.0.1', port=8080)


if __name__ == "__main__":

    sys.exit(main())
