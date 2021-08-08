import pytest

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