# -*- coding: utf-8 -*-

from flask import request
from utils import ProtocolTypes, ResultCodes, checkSessionId, checkContainKeys
import json

from database import db_session
from models import User, Friend, Character
from sqlalchemy import exc
import datetime


def addFriend():
    result = {'type': ProtocolTypes.AddFriend}

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])

        from_keys = ['session_id', 'name']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                pass
                # if (got_user.friends is None) or (got_user.friends == ''):
                #     got_friends = list(got_data['name'])
                #     got_user.friends = json.dumps(got_friends)
                #     db_session.add(got_user)
                #     try:
                #         db_session.commit()
                #     except exc.SQLAlchemyError:
                #         result['result'] = ResultCodes.DBInputError
                # else:
                #     got_friends = json.loads(got_user.friends)
                #     if got_friends:
                #         if len(got_friends) == 0:
                #             got_friends = list(got_data['name'])
                #             got_user.friends = json.dumps(got_friends)
                #             db_session.add(got_user)
                #         else:
                #             got_friends.append(got_data['name'])
                #             got_user.friends = json.dumps(got_friends)
                #             db_session.add(got_user)
                #         try:
                #             db_session.commit()
                #         except exc.SQLAlchemyError:
                #             result['result'] = ResultCodes.DBInputError
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
                            tmp_friend_info = dict(
                                user_id=got_friend.id,
                                name=got_friend.name,
                                last_login=got_friend.login_date.strftime("%Y,%m,%d")
                                )
                            # tmp_friend_info['user_id'] = got_friend.id
                            # tmp_friend_info['name'] = got_friend.name
                            # tmp_friend_info['last_login'] = got_friend.login_date.strftime("%Y,%m,%d")

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
                        tmp_friend = dict(
                            user_id=got_user_list.id,
                            name=got_user_list.name,
                            last_login=got_user_list.login_date.strftime("%Y,%m,%d")
                        )
                        # tmp_friend['user_id'] = got_user_list.id
                        # tmp_friend['name'] = got_user_list.name
                        # tmp_friend['last_login'] = got_user_list.login_date.strftime("%Y,%m,%d")

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
                        friend_data = User.query.filter_by(id=find_friend.user_id).first()
                        if friend_data:
                            tmp_friend = dict(
                                id=find_friend.user_id,
                                name=friend_data.name,
                                nickname=friend_data.nickname,
                                last_login=tmp_friend.login_date.strftime("%Y,%m,%d")
                            )
                            # tmp_friend[id] = find_friend.user_id
                            # tmp_friend['name'] = friend_data.name
                            # tmp_friend['nickname'] = friend_data.nickname
                            # tmp_friend['last_login'] = tmp_friend.login_date.strftime("%Y,%m,%d")

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


def getFriendCharacterInfo():
    result = {'type': ProtocolTypes.GetFriendCharacterInfo}

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])

        from_keys = ['session_id', 'friend_id']
        if checkContainKeys(from_keys, got_data):
            if (got_data['friend_id'] is None) or (got_data['friend_id'] == ''):
                result['result'] = ResultCodes.InputParamError
            else:
                result['result'], got_user = checkSessionId(got_data['session_id'])

                if got_user:
                    find_friend_character = Character.query.filter_by(id=got_data['friend_id']).first()
                    if find_friend_character:
                        send_friend_info = dict(
                            user_id=got_data['friend_id'],
                            name=find_friend_character.name,
                            level=find_friend_character.level,
                            body_type=find_friend_character.body_type,
                            cloak_type=find_friend_character.cloak_type,
                            color_r=find_friend_character.color_r,
                            color_g=find_friend_character.color_g,
                            color_b=find_friend_character.color_b,
                            exp=find_friend_character.exp,
                            face_type=find_friend_character.face_type,
                            hp=find_friend_character.hp,
                            gender=find_friend_character.gender,
                            hair_type=find_friend_character.hair_type,
                            weapon_exp=find_friend_character.weapon_exp,
                            weapon_level=find_friend_character.weapon_level,
                            weapon_type=find_friend_character.weapon_type,
                        )
                        # send_friend_info['user_id'] = got_data['friend_id']
                        # send_friend_info['name'] = find_friend_character.name
                        # send_friend_info['level'] = find_friend_character.level
                        # send_friend_info['body_type'] = find_friend_character.body_type
                        # send_friend_info['cloak_type'] = find_friend_character.cloak_type
                        # send_friend_info['color_r'] = find_friend_character.color_r
                        # send_friend_info['color_g'] = find_friend_character.color_g
                        # send_friend_info['color_b'] = find_friend_character.color_b
                        # send_friend_info['exp'] = find_friend_character.exp
                        # send_friend_info['face_type'] = find_friend_character.face_type
                        # send_friend_info['hp'] = find_friend_character.hp
                        # send_friend_info['gender'] = find_friend_character.gender
                        # send_friend_info['hair_type'] = find_friend_character.hair_type
                        # send_friend_info['weapon_exp'] = find_friend_character.weapon_exp
                        # send_friend_info['weapon_level'] = find_friend_character.weapon_level
                        # send_friend_info['weapon_type'] = find_friend_character.weapon_type

                        result['friend_info'] = json.dumps(send_friend_info)
                    else:
                        result['result'] = ResultCodes.NoData
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))

getFriendCharacterInfo.methods = ['POST']


def sendFriendShipPoint():
    result = dict(
        type=ProtocolTypes.SendFriendShipPoint,
        result=ResultCodes.Success
    )

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])

        from_keys = ['session_id', 'friend_id']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                find_friend = Friend.query.filter_by(
                    user_id=got_user.id, friend_id=got_data['friend_id']).first()
                if find_friend:
                    if find_friend.friendship_sent_date.strftime(
                            "%Y,%m,%d") == datetime.datetime.now().strftime(
                            "%Y,%m,%d") or find_friend.friendship_received_date.strftime(
                            "%Y,%m,%d") == datetime.datetime.now().strftime("%Y,%m,%d"):
                        result['result'] = ResultCodes.InputParamError
                    else:
                        find_friend.friendship_sent_date = datetime.datetime.now()

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


sendFriendShipPoint.methods = ['POST']


def receiveFriendShipPoint():
    result = dict(
        type=ProtocolTypes.ReceiveFriendShipPoint,
        result=ResultCodes.Success
    )

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])

        from_keys = ['session_id', 'friend_id']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                find_me = Friend.query.filter_by(
                    user_id=got_data['friend_id'], friend_id=got_user.id).first()
                if find_me:
                    if find_me.friendship_sent_date.strftime(
                            "%Y,%m,%d") == datetime.datetime.now().strftime(
                            "%Y,%m,%d") and find_me.friendship_received_date.strftime(
                            "%Y,%m,%d") != datetime.datetime.now().strftime("%Y,%m,%d"):
                        find_me.friendship_received_date = datetime.datetime.now()

                        db_session.add(find_me)
                        try:
                            db_session.commit()
                        except exc.SQLAlchemyError:
                            result['result'] = ResultCodes.DBInputError
                    else:
                        result['result'] = ResultCodes.InputParamError
                else:
                    result['result'] = ResultCodes.NoData
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))


receiveFriendShipPoint.methods = ['POST']