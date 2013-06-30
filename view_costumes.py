# -*- coding: utf-8 -*-

from flask import request
from utils import ProtocolTypes, ResultCodes, checkSessionId, checkContainKeys, commitData
import json

from database import db_session
from sqlalchemy import exc
from models import OwnCostume, OwnCostumebase, WornCostume


def setOwnCostumes():
    result = {'type': ProtocolTypes.SetOwnCostumes}

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])
        from_keys = ['session_id', 'own_costumes']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                if got_data['own_costumes'] == '':
                    result['result'] = ResultCodes.InputParamError
                else:
                    for got_costume_index in got_data['own_costumes']:
                        find_costume = OwnCostume.query.filter_by(
                            user_id=got_user.id, costume_index=got_costume_index).first()
                        if not find_costume:
                            temp_costume = OwnCostume(got_user.id, got_costume_index)
                            db_session.add(temp_costume)
                    result['result'] = commitData()
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))


setOwnCostumes.methods = ['POST']


def getOwnCostumes():
    result = {'type': ProtocolTypes.GetOwnCostumes}

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])
        from_keys = ['session_id']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                find_own_costumes = OwnCostume.query.filter_by(user_id=got_user.id).all()
                if find_own_costumes:
                    found_own_costume_indexes = list()
                    for find_own_costume in find_own_costumes:
                        found_own_costume_indexes.append(find_own_costume.costume_index)
                    result['own_costumes'] = json.dumps(found_own_costume_indexes)
                else:
                    result['result'] = ResultCodes.NoData
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))

getOwnCostumes.methods = ['POST']


def setOwnCostumebases():
    result = {'type': ProtocolTypes.SetOwnCostumeBases}

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])
        from_keys = ['session_id', 'own_costumebases']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                if got_data['own_costumebases'] == '':
                    result['result'] = ResultCodes.InputParamError
                else:
                    for got_costumebase_index in got_data['own_costumebases']:
                        find_costumebase = OwnCostumebase.query.filter_by(
                            user_id=got_user.id, costumebase_index=got_costumebase_index).first()
                        if not find_costumebase:
                            temp_costumebase = OwnCostumebase(got_user.id, got_costumebase_index)
                            db_session.add(temp_costumebase)
                    result['result'] = commitData()
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))


setOwnCostumebases.methods = ['POST']


def getOwnCostumebases():
    result = {'type': ProtocolTypes.GetOwnCostumeBases}

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])
        from_keys = ['session_id']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                find_own_costumebases = OwnCostumebase.query.filter_by(user_id=got_user.id).all()
                if find_own_costumebases:
                    found_own_costumebase_list = list()
                    for find_own_costumebase in find_own_costumebases:
                        temp_costumebase_dict = dict()
                        temp_costumebase_dict['costumebase_index'] = find_own_costumebase.costumebase_index
                        temp_costumebase_dict['lastdate_from_gotcash'] = find_own_costumebase.lastdate_from_gotcash.strftime(
                            "%Y,%m,%d")
                        found_own_costumebase_list.append(temp_costumebase_dict)
                    result['own_costumebases'] = json.dumps(found_own_costumebase_list)
                else:
                    result['result'] = ResultCodes.NoData
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))

getOwnCostumebases.methods = ['POST']


def addOwnCostume():
    result = {'type': ProtocolTypes.AddOwnCostume}

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])
        from_keys = ['session_id', 'own_costume']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                if got_data['own_costume'] == '':
                    result['result'] = ResultCodes.InputParamError
                else:
                    find_costume = OwnCostume.query.filter_by(
                        user_id=got_user.id, costume_index=got_data['own_costume']).first()
                    if not find_costume:
                        temp_costume = OwnCostume(got_user.id, got_data['own_costume'])
                        db_session.add(temp_costume)
                    result['result'] = commitData()
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))


addOwnCostume.methods = ['POST']


def addOwnCostumeBase():
    result = dict(
        type=ProtocolTypes.AddOwnCostumeBase,
        result=ResultCodes.Success)

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])
        from_keys = ['session_id', 'own_costumebase']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                if got_data['own_costumebase'] == '':
                    result['result'] = ResultCodes.InputParamError
                else:
                    find_costumebase = OwnCostumebase.query.filter_by(
                        user_id=got_user.id, costumebase_index=got_data['own_costumebase']).first()
                    if not find_costumebase:
                        temp_costumebase = OwnCostumebase(got_user.id, got_data['own_costumebase'])
                        db_session.add(temp_costumebase)
                    result['result'] = commitData()
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))


addOwnCostumeBase.methods = ['POST']


def setWornCostume():
    result = dict(
        type=ProtocolTypes.SetWornCostume,
        result=ResultCodes.Success)

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])
        from_keys = ['session_id', 'costumes']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                find_worn_costume = WornCostume.query.filter_by(user_id=got_user.id).first()
                if find_worn_costume:
                    find_worn_costume.costumes = json.dumps(got_data['costumes'])
                    db_session.add(find_worn_costume)
                else:
                    made_worn_costume = WornCostume(user_id=got_user.id, costumes=json.dumps(got_data['costumes']))
                    db_session.add(made_worn_costume)

                result['result'] = commitData()
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError


    return str(json.dumps(result))

setWornCostume.methods = ['POST']

def getWornCostume():
    result = dict(
        type=ProtocolTypes.GetWornCostume,
        result=ResultCodes.Success)

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])
        from_keys = ['session_id']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                find_worn_costume = WornCostume.query.filter_by(user_id=got_user.id).first()
                if find_worn_costume:
                    result['costumes'] = find_worn_costume.costumes
                else:
                    result['result'] = ResultCodes.NoData
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError


    return str(json.dumps(result))

getWornCostume.methods = ['POST']

