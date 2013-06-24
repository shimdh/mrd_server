# -*- coding: utf-8 -*-

from flask import request
from utils import ProtocolTypes, ResultCodes, checkSessionId, checkContainKeys
import json

from database import db_session
from models import User
from sqlalchemy import exc


def addFriend():
    result = {'type': ProtocolTypes.AddFriend}

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])

        from_keys = ['session_id', 'friend_nickname']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                got_friends = {}
                if (got_user.friends is None) or (got_user.friends == ''):
                    got_friends['friend_nickname'] = [got_data['friend_nickname']]
                    got_user.friends = json.dumps(got_friends)
                    db_session.add(got_user)
                    try:
                        db_session.commit()
                    except exc.SQLAlchemyError:
                        result['result'] = ResultCodes.DBInputError
                else:
                    got_friends = json.loads(got_user.friends)

                    if got_friends:
                        got_friends['friend_nickname'].append(got_data['friend_nickname'])
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
                if (got_user.friends is None) or (got_user.friends == ''):
                    result['result'] = ResultCodes.NoData
                else:
                    if (got_user.friends is None) or (got_user.friends == ''):
                        result['result'] = ResultCodes.NoData
                    else:
                        got_friends = json.loads(got_user.friends)
                        if len(got_friends) == 0:
                            result['result'] = ResultCodes.NoData
                        else:
                            result['friends'] = json.dumps(got_friends)
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))

getFriendsList.methods = ['POST']


def findFriendByNickname():
    result = {'type': ProtocolTypes.FindFriendByNickname}

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])

        from_keys = ['session_id', 'friend_nickname']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                got_user_lists = db_session.query(User).filter(
                    User.nickname.like('%' + got_data['friend_nickname'] + '%')).all()
                if got_user_lists:
                    send_user_lists = []
                    for got_user_list in got_user_lists:
                        send_user_lists.append(got_user_list.nickname)

                    result['searched_list'] = json.dumps(send_user_lists)
                else:
                    result['result'] = ResultCodes.NoData
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))

findFriendByNickname.methods = ['POST']


def requestFriends():
    result = {'type': ProtocolTypes.RequestFriends}

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])

        from_keys = ['session_id', 'request_friends']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                got_friends = {}
                if (got_user.request_friends is None) or (got_user.request_friends == ''):
                    got_friends['request_friends'] = [got_data['request_friends']]
                    got_user.friends = json.dumps(got_friends)
                    db_session.add(got_user)
                    try:
                        db_session.commit()
                    except exc.SQLAlchemyError:
                        result['result'] = ResultCodes.DBInputError
                else:
                    got_friends = json.loads(got_user.friends)

                    if got_friends:
                        if got_data['request_friends'] in got_friends:
                            result['result'] = ResultCodes.DataExist
                        else:
                            got_friends['request_friends'].append(got_data['request_friends'])
                            got_user.request_friends = json.dumps(got_friends)
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

requestFriends.methods = ['POST']


