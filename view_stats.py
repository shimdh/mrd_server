# -*- coding: utf-8 -*-

from flask import request
from utils import ProtocolTypes, ResultCodes, checkSessionId, checkContainKeys
import json

from database import db_session


def setStats():
    result = {'type': ProtocolTypes.SetStats}

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])
        from_keys = ['session_id', 'stats']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                got_user.stats = json.dumps(got_data['stats'])
                db_session.add(got_user)
                db_session.commit()
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
                if (got_user.stats is None) or (got_user.stats == ''):
                    result['result'] = ResultCodes.NoData
                else:
                    result['stats'] = got_user.stats
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))

getStats.methods = ['POST']
