import pytest
import asyncio

async def test_request_api_check_100000s(cli, shortener):
    responses = []
    for i in range(100000):
        url = "https//element.io/{}".format(i)
        responses.append(cli.post('/api/v1/shorten/{}'.format(url)))
    results = await asyncio.gather(*responses)
    for res in results:
        assert res.status == 200
    assert shortener.nb_shortened_links() == 100000
    assert len(results) == 100000

async def test_request_api_existing(cli):
    response = await cli.post('/api/v1/shorten/https://element.io/blog/element-raises-30m-as-matrix-explodes/')
    print(await response.text())
    assert response.status == 200
    identifier = await response.text()
    assert len(identifier) == 10
    
    response = await cli.get('/api/v1/lookup/{}'.format(identifier))
    assert response.status == 200
    url = await response.text()
    assert url == "https://element.io/blog/element-raises-30m-as-matrix-explodes/"


async def test_request_api_404(cli):
    response = await cli.get('/api/v1/lookup/https://random-non-existent-site.io')
    assert response.status == 404