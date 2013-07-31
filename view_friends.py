# -*- coding: utf-8 -*-

from flask import request
from utils import ProtocolTypes, ResultCodes, checkSessionId, checkContainKeys
from utils import commitData, writeDirtyLog
import json

from database import db_session
from models import User, Friend, Character, Stat, WornCostume, Mail, Config
import datetime
from sqlalchemy import and_


def addFriend():
    result = dict(
        type=ProtocolTypes.AddFriend,
        result=ResultCodes.Success)

    if request.form['data']:
        got_data = json.loads(request.form['data'])

        from_keys = ['session_id', 'name']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                pass
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))

addFriend.methods = ['POST']

def getFriendsList():
    result = dict(
        type=ProtocolTypes.GetFriendsList,
        result=ResultCodes.Success)

    if request.form['data']:
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
                        got_friend = User.query.filter_by(
                            id=find_friend.friend_id).first()
                        if got_friend:
                            friend_level = -1
                            if not find_friend.friend_id == 1:
                                find_friend_stat = Stat.query.filter_by(
                                    user_id=find_friend.friend_id).first()
                                if find_friend_stat:
                                    friend_level = find_friend_stat.level

                            friend_character_info = dict()
                            if not find_friend.friend_id == 1:
                                find_friend_character = Character.query.filter_by(
                                    user_id=find_friend.friend_id).first()
                                if find_friend_character:
                                    friend_character_info = dict(
                                        color_r=find_friend_character.color_r,
                                        color_g=find_friend_character.color_g,
                                        color_b=find_friend_character.color_b,
                                        gender=find_friend_character.gender,
                                        body_type=find_friend_character.body_type,
                                        hair_type=find_friend_character.hair_type,
                                        cloak_type=find_friend_character.cloak_type,
                                        face_type=find_friend_character.face_type,
                                        weapon_type=find_friend_character.weapon_type,
                                    )

                            friend_costume_info = list()
                            if not find_friend.friend_id == 1:
                                find_friend_costume = WornCostume.query.filter_by(
                                    user_id=find_friend.friend_id).first()
                                if find_friend_costume:
                                    friend_costume_info = json.loads(find_friend_costume.costumes)

                            can_send_friendship = True
                            can_receive_friendship = True

                            sent_friend = Friend.query.filter_by(user_id=find_friend.friend_id,
                                friend_id=got_user.id).first()
                            if sent_friend:
                                if sent_friend.friendship_sent_date:
                                    if sent_friend.friendship_sent_date == datetime.date.today():
                                        can_send_friendship = False

                                if not find_friend.friendship_sent_date:
                                    can_receive_friendship = False
                                else:
                                    if find_friend.friendship_sent_date != datetime.date.today():
                                        can_receive_friendship = False
                                    else:
                                        if find_friend.friendship_received_date == datetime.date.today():
                                            can_receive_friendship = False
                            else:
                                result['result'] = ResultCodes.InputParamError

                            tmp_friend_info = dict(
                                user_id=got_friend.id,
                                name=got_friend.name,
                                can_send_friendship=can_send_friendship,
                                can_receive_friendship=can_receive_friendship,
                                level=friend_level,
                                character=friend_character_info,
                                costume=friend_costume_info,
                            )

                            if find_friend.friend_id == 1 or not got_friend.login_date:
                                tmp_friend_info['last_login'] = datetime.datetime.now().strftime("%Y,%m,%d")
                            else:
                                tmp_friend_info['last_login'] = got_friend.login_date.strftime("%Y,%m,%d")

                            friends_info.append(tmp_friend_info)

                    result['friends'] = friends_info
                else:
                    result['result'] = ResultCodes.NoData
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))

getFriendsList.methods = ['POST']


def findFriendByName():
    result = dict(
        type=ProtocolTypes.FindFriendByName,
        result=ResultCodes.Success)

    if request.form['data']:
        got_data = json.loads(request.form['data'])

        from_keys = ['session_id', 'friend_name']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                # got_user_lists = db_session.query(User).filter(
                #     User.name.like('%' + got_data['friend_nickname'] + '%')).all()
                got_user_lists = User.query.filter(
                    User.name.like('%' + got_data['friend_name'] + '%')).all()
                if got_user_lists:
                    send_user_lists = []
                    for got_user_list in got_user_lists:
                        tmp_friend = dict(
                            user_id=got_user_list.id,
                            name=got_user_list.name,
                            last_login=got_user_list.login_date.strftime("%Y,%m,%d")
                        )
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
    result = dict(
        type=ProtocolTypes.RequestFriend,
        result=ResultCodes.Success)

    if request.form['data']:
        got_data = json.loads(request.form['data'])

        from_keys = ['session_id', 'request_friend']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                find_friend = Friend.query.filter_by(user_id=got_user.id, friend_id=got_data['request_friend']).first()
                if not find_friend:
                    friend_data = Friend(got_user.id, got_data['request_friend'])
                    db_session.add(friend_data)
                    write_mail = Mail(got_user.id, got_data['request_friend'], u"친구 신청")
                    write_mail.request_friend = True
                    db_session.add(write_mail)
                    result['result'] = commitData()
                else:
                    result['result'] = ResultCodes.DataExist
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))

requestFriend.methods = ['POST']


def getWaitingFriends():
    result = dict(
        type=ProtocolTypes.GetWaitingFriends,
        result=ResultCodes.Success)

    if request.form['data']:
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
                                last_login=friend_data.login_date.strftime("%Y,%m,%d")
                            )
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
    #writeDirtyLog('acceptFriend: ' + request.form['data'])
    result = dict(
        type=ProtocolTypes.AcceptFriend,
        result=ResultCodes.Success)

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
                        my_friend = Friend.query.filter_by(
                            user_id=got_user.id, friend_id=got_data['accept_friend']).first()
                        if my_friend:
                            my_friend.request = True
                            my_friend.accepted = True
                            db_session.add(my_friend)
                        else:
                            regist_friend = Friend(got_user.id, got_data['accept_friend'])
                            regist_friend.request = True
                            regist_friend.accepted = True
                            db_session.add(regist_friend)
                        result['result'] = commitData()
                    else:
                        result['result'] = ResultCodes.NoData
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))

acceptFriend.methods = ['POST']


def getFriendCharacterInfo():
    result = dict(
        type=ProtocolTypes.GetFriendCharacterInfo,
        result=ResultCodes.Success)

    if request.form['data']:
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

    if request.form['data']:
        got_data = json.loads(request.form['data'])

        from_keys = ['session_id', 'friend_id']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                find_friend = Friend.query.filter_by(
                    user_id=got_data['friend_id'], friend_id=got_user.id).first()
                if find_friend:
                    if not find_friend.friendship_sent_date:
                        find_friend.friendship_sent_date = datetime.date.today()

                        db_session.add(find_friend)

                        got_friend_user = User.query.filter_by(id=got_data['friend_id']).first()
                        if got_friend_user:
                            friend_point = Config.query.filter_by(str_key='sending_friendship_point').first()
                            if friend_point:
                                got_friend_user.friendship_point += int(friend_point.str_value)
                                db_session.add(got_friend_user)

                            got_point = Config.query.filter_by(str_key='sent_receiving_friendship_point').first()
                            if got_point:
                                got_user.friendship_point += int(got_point.str_value)
                                db_session.add(got_point)
                        else:
                            result['result'] = ResultCodes.InputParamError

                        result['result'] = commitData()
                    else:
                        if find_friend.friendship_sent_date == datetime.date.today():
                            result['result'] = ResultCodes.InputParamError
                        else:
                            find_friend.friendship_sent_date = datetime.date.today()

                            db_session.add(find_friend)

                            got_friend_user = User.query.filter_by(id=got_data['friend_id']).first()
                            if got_friend_user:
                                friend_point = Config.query.filter_by(str_key='sending_friendship_point').first()
                                if friendship_point:
                                    got_friend_user.friendship_point += int(friendship_point.str_value)
                                    db_session.add(got_friend_user)

                                got_point = Config.query.filter_by(str_key='sent_receiving_friendship_point').first()
                                if got_point:
                                    got_user.friendship_point += int(got_point.str_value)
                                    db_session.add(got_point)
                            else:
                                result['result'] = ResultCodes.InputParamError

                            result['result'] = commitData()
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

    if request.form['data']:
        got_data = json.loads(request.form['data'])

        from_keys = ['session_id', 'friend_id']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                find_me = Friend.query.filter_by(
                    user_id=got_user.id, friend_id=got_data['friend_id']).first()
                if find_me:
                    if not find_me.friendship_sent_date:
                        result['result'] = ResultCodes.InputParamError
                    else:
                        if not find_me.friendship_received_date:
                            find_me.friendship_received_date = datetime.datetime.now()

                            db_session.add(find_me)

                            friendship_point = Config.query.filter_by(str_key='receiving_friendship_point').first()
                            if friendship_point:
                                got_user.friendship_point += int(friendship_point.str_value)
                                db_session.add(got_user)
                            result['result'] = commitData()
                        else:
                            if find_me.friendship_sent_date == datetime.date.today():
                                if not find_me.friendship_received_date or (
                                    find_me.friendship_received_date != datetime.date.today()):
                                    find_me.friendship_received_date = datetime.date.today()

                                    db_session.add(find_me)

                                    friendship_point = Config.query.filter_by(str_key='receiving_friendship_point').first()
                                    if friendship_point:
                                        got_user.friendship_point += int(friendship_point.str_value)
                                        db_session.add(got_user)
                                    result['result'] = commitData()
                                else:
                                    result['result'] = ResultCodes.InputParamError
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


def useFriendShipPoint():
    result = dict(
        type=ProtocolTypes.UseFriendShipPoint,
        result=ResultCodes.Success
    )

    if request.form['data']:
        got_data = json.loads(request.form['data'])

        from_keys = ['session_id']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                max_friendship_point = Config.query.filter_by(str_key='max_friendship_point').first()
                if max_friendship_point:
                    if got_user.friendship_point > int(max_friendship_point.str_value):
                        got_user.friendship_point -= int(max_friendship_point.str_value)


                        import random

                        got_cash_rates = [16] + [7] * 12
                        found_rate = random.random() * 100
                        rate_sum = 0
                        got_cash_amount = 0

                        for x in range(len(got_cash_rates)):
                            rate_sum += got_cash_rates[x]

                            if found_rate <= rate_sum:
                                got_cash_amount = x + 1
                                break

                        except_amount = range(1, 13)
                        except_amount.remove(got_cash_amount)

                        dummy_amount = list()

                        for num in range(4):
                            got_num = random.choice(except_amount)
                            except_amount.remove(got_num)
                            dummy_amount.append(got_num)


                        got_user.cash += got_cash_amount
                        db_session.add(got_user)
                        result['result'] = commitData()
                        result['cash_amount'] = got_cash_amount
                        result['dummy_amount'] = dummy_amount
                    else:
                        result['result'] = ResultCodes.InputParamError
                else:
                    result['result'] = ResultCodes.NoData
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))

useFriendShipPoint.methods = ['POST']


def getFriendShipPointInfo():
    result = dict(
        type=ProtocolTypes.GetFriendShipPointInfo,
        result=ResultCodes.Success
    )

    if request.form['data']:
        got_data = json.loads(request.form['data'])

        from_keys = ['session_id']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                result['friendship_point'] = got_user.friendship_point
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))

getFriendShipPointInfo.methods = ['POST']


def getRecommendFriendsList():
    result = dict(
        type=ProtocolTypes.GetRecommendFriendsList,
        result=ResultCodes.Success)

    def getLastLoginUserLists(my_index, last_login_range):
        my_now = datetime.datetime.now()
        find_users = User.query.filter(
                and_(
                    User.id != my_index,
                    User.login_date >= my_now - datetime.timedelta(
                        days=last_login_range),
                    User.id != 1
                )
        ).all()

        if find_users:
            return find_users
        else:
            return None


    def getUsersStatInRangeLevel(my_index, level_range, users_list):
        my_stat = Stat.query.filter_by(user_id=my_index).first()
        if my_stat:
            got_user_list = list()

            for temp_user in users_list:
                temp_stat = Stat.query.filter_by(user_id=temp_user.id).first()
                if temp_stat:
                    if my_stat.level - level_range <= temp_stat.level <= my_stat.level + level_range:
                        temp_user_info = dict(
                            user_id=temp_user.id,
                            name=temp_user.name,
                            level=temp_stat.level,
                            last_login=temp_user.login_date.strftime("%Y,%m,%d"),
                        )
                        got_user_list.append(temp_user_info)

            if len(got_user_list) > 0:
                return got_user_list[:20]
            else:
                return None
        else:
            return None


    if request.form['data']:
        got_data = json.loads(request.form['data'])

        from_keys = ['session_id']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                find_users = getLastLoginUserLists(got_user.id, 7)
                if find_users:
                    find_range_users = getUsersStatInRangeLevel(got_user.id, 10, find_users)
                    if find_range_users:
                        result['users'] = find_range_users
                    else:
                        result['result'] = ResultCodes.NoData
                else:
                    result['result'] = ResultCodes.NoData
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))

getRecommendFriendsList.methods = ['POST']

def acceptFriendWithTara(user_nickname):
    got_user = User.query.filter_by(nickname=user_nickname).first()
    if got_user:
        regist_friend = Friend(got_user.id, 1)
        regist_friend.request = True
        regist_friend.accepted = True
        db_session.add(regist_friend)

        tara_friend = Friend(1, got_user.id)
        tara_friend.request = True
        tara_friend.accepted = True
        db_session.add(tara_friend)

        db_session.commit()


def sendFriendShipPointFromTara(user_id):
    my_friend = Friend.query.filter_by(
        user_id=user_id, friend_id=1).first()
    if my_friend:
        if not my_friend.friendship_sent_date:
            my_friend.friendship_sent_date = datetime.datetime.now()

            db_session.add(my_friend)
            db_session.commit()

        else:
            if my_friend.friendship_sent_date.strftime(
                    "%Y,%m,%d") != datetime.datetime.now().strftime("%Y,%m,%d"):
                my_friend.friendship_sent_date = datetime.datetime.now()

                db_session.add(my_friend)
                db_session.commit()

