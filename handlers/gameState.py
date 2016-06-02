# -*- coding: utf-8 -*-

import cherrypy
from mpong.masterGameBuilder import masterGame


class GameState:

    exposed = True

    @cherrypy.tools.json_out()
    def GET(self, gameId):
        return masterGame.gameState(gameId)
