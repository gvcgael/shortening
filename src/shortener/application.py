from aiohttp import web
from attr import attrib
import attr
import hashlib


@attr.s
class ShortenerApp:
  app = attrib()
  _domain_name = attrib()
  _shortened = attrib(default=dict())

  @classmethod
  def instanciate(cls, domain_name):
    app = web.Application(middlewares=[cls.middleware_factory])

    shortener = cls(app, domain_name)
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
              resp = await handler(request)
              return resp
          except web.HTTPNotFound:
              return web.Response(status=404, body="404 error",
                                  headers={'Content-Type': 'application/json'})

      return middleware_handler
  
  async def shorten(self, request):
      url = request.match_info.get('url')
      identifier = hashlib.shake_128(url.encode()).hexdigest(5)
      try:
        # Check if the identifier (hash) is already in the shortened links
        existing = self._shortened[identifier]
        # If the URL matches the one in the shortened links, lets return it
        if existing == url:
          return web.Response(text="{}/{}".format(self._domain_name, identifier))
        # Else we return a 409 (Conflict) to the first link using this identifier
        # This should be really rare since it needs a hash collision but
        # this could happen since we are using a short version of shake 128 
        else:
          print("{} : {} != {}".format(identifier, existing, url))
          return web.Response(text="{}/{}".format(self._domain_name, existing), status=409)
      except KeyError:
        self._shortened[identifier] = url
        return web.Response(text="{}/{}".format(self._domain_name, identifier))

  async def lookup(self, request):
      identifier = request.match_info.get('identifier')
      try:
        return web.Response(text=self._shortened[identifier])
      except KeyError:
        raise web.HTTPNotFound
