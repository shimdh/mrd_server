# -*- coding: utf-8 -*-

from flask import request
from utils import ProtocolTypes, ResultCodes, checkSessionId, checkContainKeys
import json

from database import db_session
from models import User, Friend
from sqlalchemy import exc


def addFriend():
    result = {'type': ProtocolTypes.AddFriend}

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])

        from_keys = ['session_id', 'friend_nickname']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                if (got_user.friends is None) or (got_user.friends == ''):
                    got_friends = list(got_data['friend_nickname'])
                    got_user.friends = json.dumps(got_friends)
                    db_session.add(got_user)
                    try:
                        db_session.commit()
                    except exc.SQLAlchemyError:
                        result['result'] = ResultCodes.DBInputError
                else:
                    got_friends = json.loads(got_user.friends)
                    if got_friends:
                        if len(got_friends) == 0:
                            got_friends = list(got_data['friend_nickname'])
                            got_user.friends = json.dumps(got_friends)
                            db_session.add(got_user)
                        else:
                            got_friends.append(got_data['friend_nickname'])
                            got_user.friends = json.dumps(got_friends)
                            db_session.add(got_user)
                        try:
                            db_session.commit()
                        except exc.SQLAlchemyError:
                            result['result'] = ResultCodes.DBInputError
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))

addFriend.methods = ['POST']


def getFriendsList():
    result = {'type': ProtocolTypes.GetFriendsList}

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])

        from_keys = ['session_id']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                find_friends = Friend.query.filter_by(
                    user_id=got_user.id, requested=True, accepted=True).all()
                if find_friends:
                    friends_info = list()
                    for find_friend in find_friends:
                        got_friend = User.query.filter_by(id=find_friend.friend_id).first()
                        if got_friend:
                            tmp_friend_info = dict()
                            tmp_friend_info['user_id'] = got_friend.id
                            tmp_friend_info['name'] = got_friend.name
                            tmp_friend_info['last_login'] = got_friend.login_date.strftime("%Y,%m,%d")

                            friends_info.append(tmp_friend_info)

                    result['friends'] = json.dumps(friends_info)
                else:
                    result['result'] = ResultCodes.NoData
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))

getFriendsList.methods = ['POST']


def findFriendByName():
    result = {'type': ProtocolTypes.FindFriendByName}

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])

        from_keys = ['session_id', 'friend_nickname']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                got_user_lists = db_session.query(User).filter(
                    User.name.like('%' + got_data['friend_nickname'] + '%')).all()
                if got_user_lists:
                    send_user_lists = []
                    for got_user_list in got_user_lists:
                        tmp_friend = dict()
                        tmp_friend['user_id'] = got_user_list.id
                        tmp_friend['name'] = got_user_list.name
                        tmp_friend['last_login'] = got_user_list.login_date.strftime("%Y,%m,%d")

                        send_user_lists.append(tmp_friend)

                    result['searched_list'] = json.dumps(send_user_lists)
                else:
                    result['result'] = ResultCodes.NoData
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))

findFriendByName.methods = ['POST']


def requestFriend():
    result = {'type': ProtocolTypes.RequestFriend}

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])

        from_keys = ['session_id', 'request_friend']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                find_friend = Friend.query.filter_by(user_id=got_user.id, friend_id=got_data['request_friend']).first()
                if not find_friend:
                    friend_data = Friend(got_user.id, got_data['request_friend'])
                    db_session.add(friend_data)
                    try:
                        db_session.commit()
                    except exc.SQLAlchemyError:
                        result['result'] = ResultCodes.DBInputError
                else:
                    result['result'] = ResultCodes.DataExist
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))

requestFriend.methods = ['POST']


def getWaitingFriends():
    result = {'type': ProtocolTypes.GetWaitingFriends}

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])

        from_keys = ['session_id']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                find_friends = Friend.query.filter_by(
                    friend_id=got_user.id, requested=True, accepted=False).all()
                if find_friends:
                    friends_data = list()
                    for find_friend in find_friends:
                        tmp_friend = dict()
                        tmp_friend[id] = find_friend.user_id
                        friend_data = User.query.filter_by(id=find_friend.user_id).first()
                        if friend_data:
                            tmp_friend['name'] = friend_data.name
                            tmp_friend['nickname'] = friend_data.nickname
                            tmp_friend['last_login'] = tmp_friend.login_date.strftime("%Y,%m,%d")

                        friends_data.append(tmp_friend)

                        if len(friends_data) == 0:
                            result['result'] = ResultCodes.NoData
                        else:
                            result['waiting_friends'] = json.dumps(friends_data)
                else:
                    result['result'] = ResultCodes.NoData
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))

getWaitingFriends.methods = ['POST']


def acceptFriend():
    result = {'type': ProtocolTypes.AcceptFriend}

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])

        from_keys = ['session_id', 'accept_friend']
        if checkContainKeys(from_keys, got_data):
            if (got_data['accept_friend'] is None) or (got_data['accept_friend'] == ''):
                result['result'] = ResultCodes.InputParamError
            else:
                result['result'], got_user = checkSessionId(got_data['session_id'])

                if got_user:
                    find_friend = Friend.query.filter_by(
                        user_id=got_data['accept_friend'], friend_id=got_user.id, requested=True, accepted=False).first()
                    if find_friend:
                        find_friend.accepted = True
                        db_session.add(find_friend)
                        try:
                            db_session.commit()
                        except exc.SQLAlchemyError:
                            result['result'] = ResultCodes.DBInputError
                    else:
                        result['result'] = ResultCodes.NoData
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))

acceptFriend.methods = ['POST']


