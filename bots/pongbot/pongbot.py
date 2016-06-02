import pongsession
import names
import time
import threading


class Statistics:
    def __init__(self):
        self.min = float('Inf')
        self.max = -float('Inf')
        self.mean = 0.0
        self.div = 0.0

    def update(self, newValue):
        if newValue < self.min:
            self.min = newValue

        if newValue > self.max:
            self.max = newValue

        self.mean += (newValue - self.mean) * 0.0125

    def __str__(self):
        return 'min: %6.5f, mean: %6.5f, max: %6.5f' % (self.min, self.mean, self.max)


class PongBot(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

        self.daemon = True

        # set a default name
        self.name = names.get_last_name()
        self.quit = False

        self.getStateStatistics = Statistics()
        self.setPaddleSpeedStatistics = Statistics()

    def printStats(self):
        print self.name, str(self.getStateStatistics)

    def run(self):
        s = pongsession.PongSession('localhost', 8080)

        self.name = names.get_last_name()
        s.startSession()
        s.setName(self.name)

        hasJoined = False
        while not hasJoined:
            try:
                games = s.getGames()

                for g in games['games']:
                    if len(g['joinedPlayers']) < g['maxPlayers']:
                        try:
                            s.joinGame(g['id'])
                            hasJoined = True
                            break
                        except pongsession.RequestNotOk:
                            continue

                else:
                    s.createGame(self.name, 2)
                    s.joinGame(self.name)
                    hasJoined = True

            except:
                continue

        player = s.getPlayer()['player']
        currentGame = player['currentGame']
        name = player['name']
        while len(currentGame['joinedPlayers']) < currentGame['maxPlayers']:
            print 'waiting for oponent (%d / %d joined)' % (len(currentGame['joinedPlayers']), currentGame['maxPlayers'])
            time.sleep(1.0)
            player = s.getPlayer()['player']
            currentGame = player['currentGame']

        if currentGame['createdBy'] == self.name:
            print "starting game"
            s.startGame()

        state = s.getState(currentGame['id'])
        while not state['gameStarted']:
            print "waiting for game to start... (%d)" % state['gameStarted']
            state = s.getState(currentGame['id'])
            time.sleep(1.0)

        print "here we go!"
        P = 4
        I = 4
        pt = time.time()
        posint = 0
        while not state['winner']:

            tmp = time.time()
            state = s.getState(currentGame['id'])
            tmp = time.time() - tmp

            self.getStateStatistics.update(tmp)

            t = time.time()

            paddle = state['paddles'][name]
            ball = state['balls']['gameBall']

            if (paddle['position'][0] < 0 and ball['velocity'][0] < 0) or (paddle['position'][0] > 0 and ball['velocity'][0] > 0):
                poserr = ball['position'][1] - paddle['position'][1]
                P = 4
                I = 4
            else:
                poserr = -paddle['position'][1]
                posint = 0
                I = 0
                P = 1

            posint += poserr * (t - pt)

            # print "(poserr %f, posint %f)" % (poserr, posint)
            tmp = time.time()
            s.setPaddleSpeed(poserr * P + posint * I)
            tmp = time.time() - tmp

            self.setPaddleSpeedStatistics.update(tmp)

            pt = t

            if self.quit:
                print 'quitting...'
                s.quitGame()

        print "game over! %s won" % state['winner']
        s.quitGame()
