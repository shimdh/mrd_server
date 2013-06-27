# -*- coding: utf-8 -*-

from flask import request
from models import Stat
from utils import ProtocolTypes, ResultCodes, checkSessionId, checkContainKeys
import json

from database import db_session
from sqlalchemy import exc


def setStats():
    result = {'type': ProtocolTypes.SetStats}

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])
        from_keys = ['session_id', 'stats']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                got_stat = got_data['stats']
                find_stat = Stat.query.filter_by(user_id=got_user.id).first()
                if find_stat:
                    find_stat.exp = got_stat['exp']
                    find_stat.level = got_stat['level']
                    find_stat.hp = got_stat['hp']
                    find_stat.weapon_level = got_data['weapon_level']
                    find_stat.weapon_exp = got_data['weapon_exp']
                    find_stat.visited_zone_no = got_data['visited_zone_no']

                    db_session.add(find_stat)
                else:
                    made_stat = Stat(got_user.id)
                    made_stat.exp = got_stat['exp']
                    made_stat.level = got_stat['level']
                    made_stat.hp = got_stat['hp']
                    made_stat.weapon_level = got_stat['weapon_level']
                    made_stat.weapon_exp = got_stat['weapon_exp']
                    made_stat.visited_zone_no = got_stat['visited_zone_no']

                    db_session.add(made_stat)

                try:
                    db_session.commit()
                except exc.SQLAlchemyError:
                    result['result'] = ResultCodes.DBInputError
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))


setStats.methods = ['POST']


def getStats():
    result = {'type': ProtocolTypes.GetStats}

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])
        from_keys = ['session_id']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                find_stat = Stat.query.filter_by(user_id=got_user.id).first()
                if find_stat:
                    send_stat = dict(
                        exp=find_stat.exp,
                        level=find_stat.level,
                        hp=find_stat.hp,
                        weapon_level=find_stat.weapon_level,
                        weapon_exp=find_stat.weapon_exp,
                        visited_zone_no=find_stat.visited_zone_no,
                    )
                    # send_stat['exp'] = find_stat.exp
                    # send_stat['level'] = find_stat.level
                    # send_stat['hp'] = find_stat.hp
                    # send_stat['weapon_level'] = find_stat.weapon_level
                    # send_stat['weapon_exp'] = find_stat.weapon_exp
                    # send_stat['visited_zone_no'] = find_stat.visited_zone_no

                    result['stats'] = json.dumps(send_stat)
                else:
                    result['result'] = ResultCodes.NoData
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))

getStats.methods = ['POST']
