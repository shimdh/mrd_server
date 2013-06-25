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
                if (got_user.friends is None) or (got_user.friends == ''):
                    result['result'] = ResultCodes.NoData
                else:
                    got_friends = json.loads(got_user.friends)
                    if len(got_friends) == 0:
                        result['result'] = ResultCodes.NoData
                    else:
                        friends_info = list()
                        for friend_nickname in got_friends:
                            tmp_friend = User.query.filter_by(nickname=friend_nickname).first()
                            if tmp_friend:
                                dict_friend = dict()
                                dict_friend['name'] = tmp_friend.name
                                tmp_stat = json.loads(tmp_friend.stats)
                                dict_friend['level'] = tmp_stat['level']
                                friends_info.append(dict_friend)
                        result['friends'] = json.dumps(friends_info)
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


def requestFriend():
    result = {'type': ProtocolTypes.RequestFriend}

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])

        from_keys = ['session_id', 'request_friend']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:                
                if (got_user.request_friends is None) or (got_user.request_friends == ''):
                    got_friend = list(got_data['request_friend'])
                    got_user.request_friends = json.dumps(got_friend)
                    db_session.add(got_user)
                    requested_friend = User.query.filter_by(nickname=got_data['request_friend']).first()
                    if requested_friend:
                        if (requested_friend.waiting_friends is None) or (requested_friend.waiting_friends == ''):
                            tmp_friends = list(got_data['request_friends'])                              
                            requested_friend.waiting_friends = json.dumps(tmp_friends)
                            db_session.add(requested_friend)
                        else:
                            tmp_friends = json.loads(got_user.requested_friend.waiting_friends)
                            if len(tmp_friends) == 0:
                                tmp_friends = list(got_data['request_friends'])                              
                                requested_friend.waiting_friends = json.dumps(tmp_friends)
                                db_session.add(requested_friend)
                            else:
                                tmp_friends.append(got_data['request_friend'])
                                requested_friend.waiting_friends = json.dumps(tmp_friends)
                                db_session.add(requested_friend)
                             
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
                            
                            requested_friend = User.query.filter_by(nickname=got_data['request_friends']).first()
                            if requested_friend:
                                if (requested_friend.waiting_friends is None) or (requested_friend.waiting_friends == ''):
                                    tmp_friends = list(got_data['request_friends'])                              
                                    requested_friend.waiting_friends = json.dumps(tmp_friends)
                                    db_session.add(requested_friend)
                                else:
                                    tmp_friends = json.loads(got_user.requested_friend.waiting_friends)
                                    if len(tmp_friends) == 0:
                                        tmp_friends = list(got_data['request_friends'])                              
                                        requested_friend.waiting_friends = json.dumps(tmp_friends)
                                        db_session.add(requested_friend)
                                    else:
                                        tmp_friends.append(got_data['request_friend'])
                                        db_session.add(requested_friend)
                                    
                            try:
                                db_session.commit()
                            except exc.SQLAlchemyError:
                                result['result'] = ResultCodes.DBInputError
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
                if (got_user.waiting_friends is None) or (got_user.waiting_friends == ''):
                    result['result'] = ResultCodes.NoData
                else:
                    got_friends = json.loads(got_user.waiting_friends)
                    if len(got_friends) == 0:
                        result['result'] = ResultCodes.NoData
                    else:
                        result['waiting_friends'] = json.dumps(got_friends)
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
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:                
                if (got_user.waiting_friends is None) or (got_user.waiting_friends == ''):
                    result['result'] = ResultCodes.NoData
                else:
                    waited_friends = json.loads(got_user.waiting_friends)
                    if len(waited_friends) == 0:
                        result['result'] = ResultCodes.NoData
                    else:
                        waited_friends.remove(result['accept_friend'])
                        if (got_user.friends is None) or (got_user.friends == ''):
                            got_user.friends = json.dumps(list(result['accept_friend']))
                            db_session.add(got_user)
                        else:
                            tmp_friends = json.loads(got_user.friends)
                            if len(tmp_friends) == 0:
                                got_user.friends = json.dumps(list(result['accept_friend']))
                                db_session.add(got_user)
                            else:
                                tmp_friends.append(result['accept_friend'])
                                got_user.friends = json.dumps(tmp_friends)
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

acceptFriend.methods = ['POST']


