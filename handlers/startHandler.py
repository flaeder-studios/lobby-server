#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy
from mpong.masterGameBuilder import masterGame


class StartHandler:

    exposed = True

    @cherrypy.tools.json_out()
    def POST(self):

        playerName = cherrypy.session.get('name')
        startGameId = masterGame.getCurrentGame(playerName)['id']
        gameStarted = masterGame.getCurrentGame(playerName)['gameStarted']
        if not gameStarted:
            masterGame.startGame(startGameId)

        cherrypy.session['currentGame'] = masterGame.getCurrentGame(playerName)

        game = masterGame.getGameData(startGameId)
        cherrypy.log('StartHandler: Start game %s' % game)
        return {'games': [game] }
