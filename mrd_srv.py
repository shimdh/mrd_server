# -*- coding: utf-8 -*-
"""Main file"""
from flask import Flask
from database import db_session
import serverconfig

import view_users
import view_costumes
import view_infos
import view_characters
import view_friends
import view_inventories
import view_slots
import view_stats
import view_mails

app = Flask(__name__)


@app.route('/')
def index():
    """Default"""
    return 'Index Page'


app.add_url_rule(
    '/register', 'register', view_users.register)
app.add_url_rule(
    '/login', 'login', view_users.login)
app.add_url_rule(
    '/create_character', 'create_character', view_characters.createCharacter)
app.add_url_rule(
    '/get_notice', 'get_notice', view_infos.getNotice)
app.add_url_rule(
    '/get_character', 'get_character', view_characters.getCharacter)
app.add_url_rule(
    '/check_gameversion', 'check_gameversion', view_infos.checkGameVersion)
app.add_url_rule(
    '/add_friend', 'add_friend', view_friends.addFriend)
app.add_url_rule(
    '/get_friendslist', 'get_friendslist', view_friends.getFriendsList)
app.add_url_rule(
    '/find_friendbynickname', 'find_friendbynickname',
    view_friends.findFriendByNickname)
app.add_url_rule(
    '/get_inventories', 'get_inventories', view_inventories.getInventories)
app.add_url_rule(
    '/set_inventories', 'set_inventories', view_inventories.setInventories)
app.add_url_rule(
    '/set_slots', 'set_slots', view_slots.setSlots)
app.add_url_rule(
    '/get_slots', 'get_slots', view_slots.getSlots)
app.add_url_rule(
    '/set_stats', 'set_stats', view_stats.setStats)
app.add_url_rule(
    '/get_stats', 'get_stats', view_stats.getStats)
app.add_url_rule(
    '/write_mail', 'write_mail', view_mails.writeMail)
app.add_url_rule(
    '/read_mail', 'read_mail', view_mails.readMail)
app.add_url_rule(
    '/get_giftmail', 'get_giftmail', view_mails.getGiftMail)
app.add_url_rule(
    '/get_maillist', 'get_maillist', view_mails.getMailList)
app.add_url_rule(
    '/delete_mails', 'delete_mails', view_mails.deleteMails)
app.add_url_rule(
    '/set_owncostumes', 'set_owncostumes', view_costumes.setOwnCostumes)
app.add_url_rule(
    '/get_owncostumes', 'get_owncostumes', view_costumes.getOwnCostumes)
app.add_url_rule(
    '/set_owncostumebases', 'set_owncostumebases', view_costumes.setOwnCostumebases)
app.add_url_rule(
    '/get_owncostumebases', 'get_owncostumebases', view_costumes.getOwnCostumebases)
app.add_url_rule(
                 '/request_friends', 'request_friends', view_friends.requestFriends)


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
