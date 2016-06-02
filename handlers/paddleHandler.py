#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy
from mpong.masterGameBuilder import masterGame


class PaddleHandler:

    exposed = True

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def POST(self):
        """ str -> float """

        data = cherrypy.request.json
        requestedSpeed = float(data['speed'])

        playerName = cherrypy.session.get('name')
        if playerName is None:
            raise cherrypy.HTTPError(400, 'No player with name %s' % playerName)

        masterGame.setPlayerSpeed(playerName, float(requestedSpeed))
        cherrypy.log('Set paddle speed to %f' % requestedSpeed)

        return {'currentSpeed': requestedSpeed}

