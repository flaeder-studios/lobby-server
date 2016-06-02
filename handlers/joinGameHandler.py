#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy
from mpong.masterGameBuilder import masterGame


class JoinGameHandler:
    exposed = True

    def GET(self, gameID):
        playerName = cherrypy.session.get('name')
        joinGameId = masterGame.getCurrentGame(playerName)['id']
        game = masterGame.getGameData(joinGameId)
        cherrypy.log("JoinGameHandler: Player %s joined game %s" % (playerName, game))
        return {'games': [game]}

    @cherrypy.tools.json_out()
    def POST(self, gameID):

        # Add player to game. This allows him to pick up a websocket to the game. Return adress to ws.
        playerName = cherrypy.session.get('name')

        masterGame.join(gameID, playerName)
        cherrypy.session['currentGame'] = masterGame.getCurrentGame(playerName)

        return self.GET(gameID)
