#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy
from gameHandler import GameHandler
from mpong.masterGameBuilder import masterGame


class StopHandler:

    exposed = True

    def POST(self):

        playerName = cherrypy.session.get('name')
        currentGame = masterGame.getCurrentGame(playerName)
        masterGame.stopGame(currentGame['id'])
        masterGame.leave(currentGame['id'], playerName)

        game = masterGame.getGameData(currentGame['id'])
        cherrypy.log('StopHandler: stop and leave game %s' % game)
        return {'games':[game]}
