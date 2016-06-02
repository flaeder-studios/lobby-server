import model
import cherrypy
import time
import threading

class MasterGameBuilder(object):

    def __init__(self):
        self.games = {}
        self.players = {}

    def createPlayer(self, name):
        if name in self.players:
            raise cherrypy.HTTPError(401, 'MasterGameBuilder: Player %s already exists' % name)
        if name == "":
            raise cherrypy.HTTPError(401, 'MasterGameBuilder: Player name "" illegale')
        cherrypy.log('200','MasterGameBuilder: create player %s' % name)
        self.players[name] = [model.Player(name), time.time()]

    def createGame(self, gameID, maxPlayers, createdBy):
        player = self.isPlayerName(createdBy)
        if gameID == "":
            raise cherrypy.HTTPError(404, 'MasterGameBuilder: Game name "" illegale')
        if gameID in self.games:
            raise cherrypy.HTTPError(404, 'MasterGameBuilder: Game already %s exists' % gameID)
        self.games[gameID] = [model.MPongGame(gameID, maxPlayers, createdBy), time.time()]
        player.setCreatedGames(self.getGameData(gameID))
        if gameID == 'TerminatorConnan':
            self.join(gameID, 'Arnold')
        cherrypy.log('200','MasterGameBuilder: create game %s' % gameID)
        return self.getGameData(gameID)

    def isGameID(self, gameID):
        """ Check if a gameID exist in self.games ."""
        if gameID not in self.games:
            raise cherrypy.HTTPError(404, 'MasterGameBuilder: No game with id %s found.' % (gameID))
        self.games[gameID][1] = time.time()
        return self.games[gameID][0]

    def isPlayerName(self, playerName):
        """ Check if a playerName exist in self.players ."""
        if playerName not in self.players:
            raise cherrypy.HTTPError(401, 'MasterGameBuilder: No player with name %s found' % playerName)
        self.players[playerName][1] = time.time()
        return self.players[playerName][0]

    def getCurrentGame(self, playerName):
        player = self.isPlayerName(playerName)
        cherrypy.log('200', 'MasterGameBuilder: returning currentGame for player %s' % playerName)
        return player.getCurrentGame()

    def getCreatedGames(self, playerName):
        player = self.isPlayerName(playerName)
        cherrypy.log('200', 'MasterGameBuilder: returning currentGame for player %s' % playerName)
        return player.getCreatedGames()

    def getPlayerData(self, playerName):
        player = self.isPlayerName(playerName)
        cherrypy.log('200', 'MasterGameBuilder: returning currentGame for player %s' % playerName)
        return player.getPlayerData()

    def getGameData(self, gameID):
        game = self.isGameID(gameID)
        cherrypy.log('200', 'MasterGameBuilder: returning GameData for game %s' % gameID)
        return game.getGameData()

    def getAllGameData(self):
        return [value[0].getGameData() for key, value in self.games.items()]

    def updatePlayers(self, game):
        for player in game.joinedPlayers:
            player.setCurrentGame(game.getGameData())

    def join(self, gameID, playerName):
        game = self.isGameID(gameID)
        player = self.isPlayerName(playerName)
        game.joinPlayer(player)
        self.updatePlayers(game)
        cherrypy.log('200','MasterGameBuilder: player %s joined game %s' % (playerName, gameID))

    def leave(self, gameID, playerName):
        game = self.isGameID(gameID)
        player = self.isPlayerName(playerName)
        game.leavePlayer(player)
        player.setCurrentGame(None)
        self.updatePlayers(game)
        cherrypy.log('200','MasterGameBuilder: player %s left game %s' % (playerName, gameID))

    def startGame(self, gameID):
        game = self.isGameID(gameID)
        if not game.maxPlayers == len(game.joinedPlayers):
            raise cherrypy.HTTPError(404, 'MasterGameBuilder: Not enough players joined')
        if game.isAlive():
            raise cherrypy.HTTPError(404, 'MasterGameBuilder: Game already started')
        game.start()
        self.updatePlayers(game)
        cherrypy.log('200','MasterGameBuilder: start game %s' % gameID)

    def stopGame(self, gameID):
        game = self.isGameID(gameID)
        game.stop()
        self.updatePlayers(game)
        cherrypy.log('200','MasterGameBuilder: stop game %s' % gameID)

    def setPlayerSpeed(self, playerName, speedY):
        """ Set player speed in y-direction."""
        player = self.isPlayerName(playerName)
        player.velocity = model.Vector(0, float(speedY))
        cherrypy.log('200','MasterGameBuilder: set player %s speed in y-direction to %f' % (playerName, speedY))

    def gameState(self, gameID):
        game = self.isGameID(gameID)
        cherrypy.log('200','MasterGameBuilder: game %s state %s' % (gameID, self.games[gameID][0].getState()))
        return game.getState()

    def deletePlayer(self, playerName):
        player = self.isPlayerName(playerName)
        if player.currentGame is not None:
            raise cherrypy.HTTPError(401, 'MasterGameBuilder: Cannot delete player %s while currentGame is not None' % playerName)
        removedPlayer = player.name
        del self.players[playerName]
        cherrypy.log('200','MasterGameBuilder: delete player %s' % playerName)
        return removedPlayer

    def deleteGame(self, gameID):
        game = self.isGameID(gameID)
        if game.isAlive():
            raise cherrypy.HTTPError(404, 'MasterGameBuilder: Cannot delete active game %s ' % gameID)
        if len(game.joinedPlayers) > 0:
            raise cherrypy.HTTPError(404, 'MasterGameBuilder: Cannot delete game %s, joinedPlayers not empty' % gameID)
        removedGame = game.getGameData()
        del self.games[gameID]
        cherrypy.log('200','MasterGameBuilder: delete game %s' % gameID)
        return removedGame


masterGame = MasterGameBuilder()
masterGame.createPlayer('Arnold')
