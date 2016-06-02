import handlers
import cherrypy


def handleError():
    cherrypy.response.status = 500
    cherrypy.response.body = ["An error occurred..."]


class Root:
    _cp_config = {'request.error_response': handleError}


root = Root()

root.game = Root()
root.game.state = handlers.GameState()
root.game.paddle = handlers.PaddleHandler()

root.lobby = Root()
root.lobby.game = handlers.GameHandler()
root.lobby.player = handlers.PlayerHandler()
root.lobby.method = Root()
root.lobby.method.join = handlers.JoinGameHandler()
root.lobby.method.leave = handlers.LeaveGameHandler()
root.lobby.method.start = handlers.StartHandler()
root.lobby.method.quit = handlers.StopHandler()

root.ws = handlers.WebSocketHandler()
