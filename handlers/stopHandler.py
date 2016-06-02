#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy


class StopHandler:

    exposed = True

    def POST(self):
        return {'games': []}
