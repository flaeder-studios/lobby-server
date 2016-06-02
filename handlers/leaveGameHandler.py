#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy
from mpong.masterGameBuilder import masterGame

class LeaveGameHandler:
    
    exposed = True
    
    @cherrypy.tools.json_out()
    def POST(self):
        playerName = cherrypy.session.get('name')
        leaveGameId = masterGame.getCurrentGame(playerName)['id']
        masterGame.leave(leaveGameId, playerName)
        cherrypy.session['currentGame'] = masterGame.getCurrentGame(playerName)
        
        game = masterGame.getGameData(leaveGameId)
        cherrypy.log("LeaveGameHandler: Player %s left game %s" % (playerName,game))
        return {'games': [game]}

