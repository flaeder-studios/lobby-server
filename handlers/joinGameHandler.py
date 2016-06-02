#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy


class JoinGameHandler:
    exposed = True

    def GET(self, gameID):
        return {'games': []}

    @cherrypy.tools.json_out()
    def POST(self, gameID):
        return self.GET(gameID)
