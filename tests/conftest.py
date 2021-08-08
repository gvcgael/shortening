import pytest
from aiohttp import web
from shortener import ShortenerApp


@pytest.fixture
def cli(loop, aiohttp_client):
    app = ShortenerApp.instanciate().app
    return loop.run_until_complete(aiohttp_client(app))
