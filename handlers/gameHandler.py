#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy


class GameHandler:

    exposed = True

    def getAllGames(self):
        return {'games': []}

    def getGame(self, gameID):
        return {'games': []}

    @cherrypy.tools.json_out()
    def GET(self, gameID=None):
        if not cherrypy.session.get('name'):
            raise cherrypy.HTTPError(401)

        if gameID is None:
            return self.getAllGames()
        else:
            return self.getGame(gameID)

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self, gameID=None):
        if not cherrypy.session.get('name'):
            raise cherrypy.HTTPError(401, 'name not set')
        playerName = cherrypy.session.get('name')

        game = cherrypy.request.json
        if u'id' not in game:
            if gameID:
                game[u'id'] = gameID
            else:
                raise cherrypy.HTTPError(400, 'game id not set')
        if u'maxPlayers' not in game:
            raise cherrypy.HTTPError(400, 'game maxPlayers not set')
        game[u'maxPlayers'] = int(game[u'maxPlayers'])
        # gameID != game[u'id']

        masterGame.createGame(game[u'id'], int(game[u'maxPlayers']), playerName)
        cherrypy.session['createdGames'] = masterGame.getCreatedGames(playerName)

        game = masterGame.getGameData(game[u'id'])
        cherrypy.log("GameHandler: created game %s" % game)
        return {'games': [game]}

    @cherrypy.tools.json_out()
    def DELETE(self, gameID):
        if not cherrypy.session.get('name'):
            raise cherrypy.HTTPError(401, 'name not set')

        return {'games': []}
