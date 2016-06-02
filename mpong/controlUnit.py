import time
import threading
from handlers.gameHandler import GameHandler
from mpong.masterGameBuilder import masterGame
import cherrypy


class ControlUnit(threading.Thread):

    def __init__(self, mgb):
        super(ControlUnit, self).__init__(target=self.run)
        self.mgb = mgb
        self.daemon = True
        self.deleteGames = []
        self.deletePlayers = []

    def run(self):
        while True:
            time.sleep(10)
            pt = time.time()
            for playerName, value in self.mgb.players.items():
                startTime = value[1]
                if pt - startTime > 3000:
                    cherrypy.log('200','ControlUnit: player %s timeout' % playerName)
                    self.deletePlayers.append(playerName)
            for playerName in self.deletePlayers:
                self.mgb.deletePlayer(playerName)
            self.deletePlayers = []
            self.deleteGames = []


cu = ControlUnit(masterGame)
