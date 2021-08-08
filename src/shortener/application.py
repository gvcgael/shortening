from aiohttp import web
from attr import attrib
import attr
import hashlib


@attr.s
class ShortenerApp:
  app = attrib()
  _shortened = attrib(default=dict())

  @classmethod
  def instanciate(cls):
    app = web.Application(middlewares=[cls.middleware_factory])

    shortener = cls(app)
    app.add_routes(
      [
        web.post(r'/api/v1/shorten/{url:.+}', shortener.shorten),
        web.get(r'/api/v1/lookup/{identifier:.+}', shortener.lookup)
      ]
    )
    return shortener

  @classmethod
  async def middleware_factory(cls, app, handler):
      async def middleware_handler(request):
          try:
              print(request.path)
              print([r for r in app.router.routes()])
              resp = await handler(request)
              return resp
          except web.HTTPNotFound:
              return web.Response(status=404, body="404 error",
                                  headers={'Content-Type': 'application/json'})

      return middleware_handler
  
  async def shorten(self, request):
      print("shorten")
      url = request.match_info.get('url')
      identifier = hashlib.shake_128(url.encode()).hexdigest(5)
      self._shortened[identifier] = url
      return web.Response(text=identifier)

  async def lookup(self, request):
      print("lookup")
      identifier = request.match_info.get('identifier')
      try:
        return web.Response(text=self._shortened[identifier])
      except KeyError:
        raise web.HTTPNotFound
