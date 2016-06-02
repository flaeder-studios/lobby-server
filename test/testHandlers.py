import requests
from nose import *
import cherrypy


root = 'http://localhost:8080/'
s = requests.Session()

# tests for one player
def testPlayer():
    r = s.post(root + 'player/', json={'player': {'name': 'Leibnitz'}})
    assert r.json()['player']['name'] == 'Leibnitz'

def testPlayerAgain():
    r = s.post(root + 'player/', json={'player': {'name': 'Leibnitz'}})
    assert r.json().get('player') == None

def testCreateGame():
    r = s.post(root + 'game/', json={'id': 'TerminatorDaniel', 'maxPlayers': 2})
    assert r.json()['games'][0]['id'] == 'TerminatorDaniel'

def testJoin():
    r = s.post(root + 'game/method/join/TerminatorDaniel')
    assert r.json()['games'][0]['joinedPlayers'][0] == 'Leibnitz'

def testJoinAgain():
    r = s.post(root + 'game/method/join/TerminatorDaniel')
    assert r.status_code == 401

def testLeave():
    r = s.post(root + 'game/method/leave')
    assert len(r.json()['games'][0]['joinedPlayers']) == 0 

def testDeleteGame():
    r = s.delete(root + 'game/TerminatorDaniel')
    assert r.json()['games'][0]['id'] == 'TerminatorDaniel'


# Add one more player to test start and stop game
s2 = requests.Session()

def testStart():
    r = s2.post(root + 'player/', json={'player': {'name': 'Newton'}})
    r = s2.post(root + 'game/', json={'id': 'ChuckNorris', 'maxPlayers': 2})
    r = s2.post(root + 'game/method/join/ChuckNorris')
    r = s.post(root + 'game/method/join/ChuckNorris')
    r = s.post(root + 'game/method/start')
    assert r.json()['games'][0]['gameStarted']

def testStop():
    r = s2.post(root + 'game/method/quit')
    assert r.status_code
