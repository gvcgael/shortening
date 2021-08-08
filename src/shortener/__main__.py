import sys
from aiohttp import web
from optparse import OptionParser
from .application import ShortenerApp

if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option(
        "--port",
        dest="port",
        default=30000,
        help="Please select a port",
    )

    parser.add_option(
        "--domain",
        dest="domain_name",
        default="http://localhost:30000",
        help="The domain name of the application",
    )
    (options, args) = parser.parse_args(sys.argv)

    web.run_app(ShortenerApp.instanciate(options.domain_name).app, port=options.port)
