import pytest
import asyncio

async def test_request_api_check_3000s(cli, shortener):
    for i in range(3):
        responses = []
        for i in range(3000):
            url = "https//element.io/{}".format(i)
            responses.append(cli.post('/api/v1/shorten/{}'.format(url)))
        results = await asyncio.gather(*responses)
        for res in results:
            assert res.status == 200
        assert len(shortener._shortened) == 3000
        assert len(results) == 3000


async def test_request_api_existing(cli):
    response = await cli.post('/api/v1/shorten/https://element.io/blog/element-raises-30m-as-matrix-explodes/')
    print(await response.text())
    assert response.status == 200
    identifier = await response.text()
    assert len(identifier.split('/')[-1]) == 10
    
    response = await cli.get('/api/v1/lookup/{}'.format(identifier.split('/')[-1]))

    assert response.status == 200
    url = await response.text()
    assert url == "https://element.io/blog/element-raises-30m-as-matrix-explodes/"

    # if we request it again, we get a 200
    response = await cli.post('/api/v1/shorten/https://element.io/blog/element-raises-30m-as-matrix-explodes/')
    print(await response.text())
    assert response.status == 200
    identifier = await response.text()
    assert len(identifier.split('/')[-1]) == 10


async def test_request_api_404(cli):
    response = await cli.get('/api/v1/lookup/https://random-non-existent-site.io')
    assert response.status == 404