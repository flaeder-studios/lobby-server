#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy


class StartHandler:

    exposed = True

    @cherrypy.tools.json_out()
    def POST(self):
        return {'games': []}
