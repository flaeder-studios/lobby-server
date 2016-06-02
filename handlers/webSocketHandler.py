import cherrypy
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
WebSocketPlugin(cherrypy.engine).subscribe()
cherrypy.tools.websocket = WebSocketTool()

class WebSocketHandler(object):

    @cherrypy.expose
    def index(self):
        return "hello, world"

    @cherrypy.expose
    def ws(self):
        handler = cherrypy.request.ws_handler
