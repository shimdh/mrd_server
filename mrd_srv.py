#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Main file"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask
from database import db_session
import serverconfig
import view_events
import view_fishing

import view_users
import view_costumes
import view_infos
import view_characters
import view_friends
import view_inventories
import view_slots
import view_stats
import view_mails
import view_saved
import view_puzzles
import view_diaries

app = Flask(__name__)


@app.route('/')
def index():
    """Default"""
    return 'Index Page'

app.add_url_rule(
    '/register', 'register',
    view_users.register)
app.add_url_rule(
    '/login', 'login',
    view_users.login)
app.add_url_rule(
    '/create_character', 'create_character',
    view_characters.createCharacter)
app.add_url_rule(
    '/get_notice', 'get_notice',
    view_infos.getNotice)
app.add_url_rule(
    '/get_character', 'get_character',
    view_characters.getCharacter)
app.add_url_rule(
    '/check_gameversion', 'check_gameversion',
    view_infos.checkGameVersion)
app.add_url_rule(
    '/add_friend', 'add_friend',
    view_friends.addFriend)
app.add_url_rule(
    '/get_friendslist', 'get_friendslist',
    view_friends.getFriendsList)
app.add_url_rule(
    '/find_friendbyname', 'find_friendbyname',
    view_friends.findFriendByName)
app.add_url_rule(
    '/get_inventories', 'get_inventories',
    view_inventories.getInventories)
app.add_url_rule(
    '/set_inventories', 'set_inventories',
    view_inventories.setInventories)
app.add_url_rule(
    '/set_slots', 'set_slots',
    view_slots.setSlots)
app.add_url_rule(
    '/get_slots', 'get_slots',
    view_slots.getSlots)
app.add_url_rule(
    '/set_stats', 'set_stats',
    view_stats.setStats)
app.add_url_rule(
    '/get_stats', 'get_stats',
    view_stats.getStats)
app.add_url_rule(
    '/write_mail', 'write_mail',
    view_mails.writeMail)
app.add_url_rule(
    '/read_mail', 'read_mail',
    view_mails.readMail)
app.add_url_rule(
    '/get_giftmail', 'get_giftmail',
    view_mails.getGiftMail)
app.add_url_rule(
    '/get_maillist', 'get_maillist',
    view_mails.getMailList)
app.add_url_rule(
    '/delete_mails', 'delete_mails',
    view_mails.deleteMails)
app.add_url_rule(
    '/set_owncostumes', 'set_owncostumes',
    view_costumes.setOwnCostumes)
app.add_url_rule(
    '/get_owncostumes', 'get_owncostumes',
    view_costumes.getOwnCostumes)
app.add_url_rule(
    '/set_owncostumebases', 'set_owncostumebases',
    view_costumes.setOwnCostumebases)
app.add_url_rule(
    '/get_owncostumebases', 'get_owncostumebases',
    view_costumes.getOwnCostumebases)
app.add_url_rule(
    '/request_friend', 'request_friend',
    view_friends.requestFriend)
app.add_url_rule(
    '/get_waitingfriends', 'get_waitingfriends',
    view_friends.getWaitingFriends)
app.add_url_rule(
    '/accept_friend', 'accept_friend',
    view_friends.acceptFriend)
app.add_url_rule(
    '/get_friendcharacterinfo', 'get_friendcharacterinfo',
    view_friends.getFriendCharacterInfo)
app.add_url_rule(
    '/add_completedevent', 'add_completedevent',
    view_events.addCompletedEvent)
app.add_url_rule(
    '/get_fishing', 'get_fishing',
    view_fishing.getFishing)
app.add_url_rule(
    '/add_owncostume', 'add_owncostume',
    view_costumes.addOwnCostume)
app.add_url_rule(
    '/add_owncostumebase', 'add_owncostumebase',
    view_costumes.addOwnCostumeBase)
app.add_url_rule(
    '/send_friendshippoint', 'send_friendshippoint',
    view_friends.sendFriendShipPoint)
app.add_url_rule(
    '/receive_friendshippoint', 'receive_friendshippoint',
    view_friends.receiveFriendShipPoint)
app.add_url_rule(
    '/set_buttonstate', 'set_buttonstate',
    view_saved.setButtonState)
app.add_url_rule(
    '/get_buttonstate', 'get_buttonstate',
    view_saved.getButtonState)
app.add_url_rule(
    '/set_savedstory', 'set_savedstory',
    view_saved.setSavedStory)
app.add_url_rule(
    '/get_savedstory', 'get_savedstory',
    view_saved.getSavedStory)
app.add_url_rule(
    '/set_savedcurrentzone', 'set_savedcurrentzone',
    view_saved.setSavedCurrentZone)
app.add_url_rule(
    '/get_savedcurrentzone', 'get_savedcurrentzone',
    view_saved.getSavedCurrentZone)
app.add_url_rule(
    '/add_puzzlepiece', 'add_puzzlepiece',
    view_puzzles.addOpenedPuzzlePiece)
app.add_url_rule(
    '/get_puzzlepieces', 'get_puzzlepieces',
    view_puzzles.getOpenedPuzzlePieces)
app.add_url_rule(
    '/add_puzzle', 'add_puzzle',
    view_puzzles.addOpenedPuzzle)
app.add_url_rule(
    '/get_puzzles', 'get_puzzles',
    view_puzzles.getOpenedPuzzles)
app.add_url_rule(
    '/add_diary', 'add_diary',
    view_diaries.addDiary)
app.add_url_rule(
    '/get_diaries', 'get_diaries',
    view_diaries.getDiaries)
app.add_url_rule(
    '/set_worncostume', 'set_worncostume',
    view_costumes.setWornCostume)
app.add_url_rule(
    '/get_worncostume', 'get_worncostume',
    view_costumes.getWornCostume)
app.add_url_rule(
    '/set_cash', 'set_cash',
    view_users.setCash)
app.add_url_rule(
    '/get_cash', 'get_cash',
    view_users.getCash)
app.add_url_rule(
    '/got_cashfromcostumebase', 'got_cashfromcostumebase',
    view_costumes.gotCashFromCostumeBase)
app.add_url_rule(
    '/got_cashfromcostumebases', 'got_cashfromcostumebases',
    view_costumes.gotCashFromCostumeBases)
app.add_url_rule(
    '/open_mail', 'open_mail',
    view_mails.openMail)
app.add_url_rule(
    '/check_newmail', 'check_newmail',
    view_mails.checkNewMail)


@app.route('/hello')
def hello():
    """Example"""
    return 'Hello World'


@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.debug = True
    # app.run(host='0.0.0.0')
    app.run(host=serverconfig.HOST, port=serverconfig.PORT)
