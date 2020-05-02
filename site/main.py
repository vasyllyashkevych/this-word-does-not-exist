import jinja2
import aiohttp_jinja2
from aiohttp import web
import words
import sys
import argparse

routes = web.RouteTableDef()
word_index = words.WordIndex.load("./data/words.json")


@routes.get("/")
@aiohttp_jinja2.template("index.jinja2")
async def index(request):
    return {"word": word_index.random()}


@routes.get("/favicon.ico")
async def favicon(request):
    return web.FileResponse("./static/favicon.ico")


def app(argv):
    app = web.Application()
    app.add_routes(routes)
    app.add_routes([web.static("/static", "./static")])
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader("./templates"))
    return app


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, help="Unix socket path")
    args = parser.parse_args()
    web.run_app(app(sys.argv), path=args.path)
