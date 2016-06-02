import pongbot
import time
import sys


if __name__ == '__main__':

    nbots = 16
    if len(sys.argv) > 1:
        nbots = int(sys.argv[1])

    print 'starting %d bots...' % nbots
    bots = [pongbot.PongBot() for c in xrange(nbots)]

    for bot in bots:
        bot.start()
        time.sleep(1.0)

    while True:
        time.sleep(10)
        print '---------------'
        print 'getStateDelay:', min([bot.getStateStatistics.min for bot in bots]), sum([bot.getStateStatistics.mean for bot in bots]) / len(bots), max([bot.getStateStatistics.max for bot in bots])
        print 'setPaddleSpeedDelay:', min([bot.setPaddleSpeedStatistics.min for bot in bots]), sum([bot.setPaddleSpeedStatistics.mean for bot in bots]) / len(bots), max([bot.setPaddleSpeedStatistics.max for bot in bots])
