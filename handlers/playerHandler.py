#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy
from mpong.masterGameBuilder import masterGame


class PlayerHandler:

    exposed = True

    @cherrypy.tools.json_out()
    def GET(self):

        if 'name' not in cherrypy.session:
            return {'player': {}}

        playerName = cherrypy.session['name']
        cherrypy.session['currentGame'] = None
        cherrypy.session['createdGames'] = None

        playerData = masterGame.getPlayerData(playerName)
        cherrypy.log("player: %s" % playerData)

        return {'player': playerData}

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self):
        """ This method creates a player. A player name must be unique."""

        data = cherrypy.request.json

        # if exists pull out player name from data
        if 'player' in data and 'name' in data['player']:
            playerName = data['player']['name']
            masterGame.createPlayer(playerName)
            cherrypy.session['name'] = playerName
            cherrypy.log("set name to %s" % (playerName))

        return self.GET()
