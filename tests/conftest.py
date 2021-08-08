import pytest
from aiohttp import web
from shortener import ShortenerApp


@pytest.fixture
def shortener():
    return ShortenerApp.instanciate(domain_name="localhost")

@pytest.fixture
def cli(loop, aiohttp_client, shortener):
    app = shortener.app
    return loop.run_until_complete(aiohttp_client(app))
