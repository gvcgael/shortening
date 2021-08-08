
from aiohttp import web
from .application import ShortenerApp

if __name__ == '__main__':
    web.run_app(ShortenerApp.instanciate().app, port=30000)
