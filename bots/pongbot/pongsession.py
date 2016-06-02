import requests


URLTAB = {
    'GAME': '/game',
    'JOIN': '/game/method/join/{id}',
    'LEAVE': '/game/method/leave',
    'START': '/game/method/start',
    'QUIT': '/game/method/quit',
    'STATE': '/game/state/{id}',
    'PADDLE': '/game/paddle',
    'PLAYER': '/player'
}


class RequestNotOk(Exception):
    def __init__(self, r):
        self.r = r


def checkRequestResponse(fun):
    def decorated(*args):
        r = fun(*args)

        if r.status_code > 399 or r.status_code < 200:
            print r.json()
            raise RequestNotOk(r)

        return r.json()
    return decorated


class PongSession(requests.Session):

    def __init__(self, host, port):
        requests.Session.__init__(self)
        self.host = host
        self.port = port

    def url(self, service, **kwargs):
        return 'http://' + self.host + ':' + str(self.port) + URLTAB[service].format(**kwargs)

    @checkRequestResponse
    def startSession(self):
        return self.get(self.url('PLAYER'))

    @checkRequestResponse
    def getPlayer(self):
        return self.get(self.url('PLAYER'))

    @checkRequestResponse
    def setName(self, name):
        return self.post(self.url('PLAYER'), json={'player': {'name': name}})

    @checkRequestResponse
    def getGames(self):
        return self.get(self.url('GAME'))

    @checkRequestResponse
    def createGame(self, id, maxPlayers):
        return self.post(self.url('GAME'), json={'maxPlayers': maxPlayers, 'id': id})

    @checkRequestResponse
    def startGame(self):
        return self.post(self.url('START'))

    @checkRequestResponse
    def joinGame(self, id):
        return self.post(self.url('JOIN', id=id))

    def leaveGame(self):
        pass

    def quitGame(self):
        return self.post(self.url('QUIT'))

    @checkRequestResponse
    def getState(self, id):
        return self.get(self.url('STATE', id=id))

    @checkRequestResponse
    def setPaddleSpeed(self, spd):
        return self.post(self.url('PADDLE'), json={'speed': spd})
