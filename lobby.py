#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy
import os
import json
import stat
from lobbyApplication import root


def standardErrorMessage(status, message, traceback, version):
    response = cherrypy.response
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'status': status, 'message': message, 'traceback': traceback, 'version': version})


def setSocketPermissions():
    os.chmod(cherrypy.config.get('server.socket_file'), stat.S_IROTH | stat.S_IWOTH)

cherrypy.engine.subscribe('start', setSocketPermissions, 100)

cherrypy.config.update({'error_page.default': standardErrorMessage})
cherrypy.config.update({'log.screen': True,
                        'log.access_file': '',
                        'log.error_file': '',
                        'server.thread_pool': 30,
                        'server.socket_file': '/tmp/flaeder/lobby/socket'})
cfgFile = os.path.dirname(os.path.realpath(__file__)) + '/lobby.conf'
cherrypy.quickstart(root, '/', cfgFile)
