#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy


class LeaveGameHandler:

    exposed = True

    @cherrypy.tools.json_out()
    def POST(self):
        return {'games': []}
