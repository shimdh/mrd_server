# -*- coding: utf-8 -*-

from flask import request
from utils import ProtocolTypes, ResultCodes, checkSessionId, checkContainKeys
import json

from database import db_session
from sqlalchemy import exc


def setOwnCostumes():
    result = {'type': ProtocolTypes.SetSlots}

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])
        from_keys = ['session_id', 'own_costumes']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                got_user.own_costumes = json.dumps(got_data['own_costumes'])
                db_session.add(got_user)
                try:
                    db_session.commit()
                except exc.SQLAlchemyError:
                        result["result"] = ResultCodes.DBInputError                
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))


setOwnCostumes.methods = ['POST']


def getOwnCostumes():
    result = {'type': ProtocolTypes.GetSlots}

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])
        from_keys = ['session_id']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                if (got_user.own_costumes is None) or (got_user.own_costumes == ''):
                    result['result'] = ResultCodes.NoData
                else:
                    result['own_costumes'] = got_user.own_costumes
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))

getOwnCostumes.methods = ['POST']


def setOwnCostumebases():
    result = {'type': ProtocolTypes.SetSlots}

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])
        from_keys = ['session_id', 'own_costumebases']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                got_user.own_costumebases = json.dumps(got_data['own_costumebases'])
                db_session.add(got_user)
                try:
                    db_session.commit()
                except exc.SQLAlchemyError:
                        result["result"] = ResultCodes.DBInputError                
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))


setOwnCostumebases.methods = ['POST']


def getOwnCostumebases():
    result = {'type': ProtocolTypes.GetSlots}

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])
        from_keys = ['session_id']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                if (got_user.own_costumebases is None) or (got_user.own_costumebases == ''):
                    result['result'] = ResultCodes.NoData
                else:
                    result['own_costumebases'] = got_user.own_costumebases
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))

getOwnCostumebases.methods = ['POST']



