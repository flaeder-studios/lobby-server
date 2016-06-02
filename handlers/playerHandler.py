#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy


class PlayerHandler:

    exposed = True

    @cherrypy.tools.json_out()
    def GET(self):

        if 'name' not in cherrypy.session:
            return {'player': {}}

        return {'player': {'name': cherrypy.session['name']}}

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self):
        """ This method creates a player. A player name must be unique."""

        data = cherrypy.request.json

        # if exists pull out player name from data
        if 'player' in data and 'name' in data['player']:
            playerName = data['player']['name']
            cherrypy.session['name'] = playerName
            cherrypy.log("set name to %s" % (playerName))

        return self.GET()
