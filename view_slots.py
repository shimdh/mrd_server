# -*- coding: utf-8 -*-

from flask import request
from utils import ProtocolTypes, ResultCodes, checkSessionId, checkContainKeys
import json


from database import db_session


def setSlots():
    result = {'type': ProtocolTypes.SetSlots}

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])
        from_keys = ['session_id', 'slots']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                got_user.slots = json.dumps(got_data['slots'])
                db_session.add(got_user)
                db_session.commit()
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))


setSlots.methods = ['POST']


def getSlots():
    result = {'type': ProtocolTypes.GetSlots}

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])
        from_keys = ['session_id']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                if (got_user.slots is None) or (got_user.slots == ''):
                    result['result'] = ResultCodes.NoData
                else:
                    result['slots'] = got_user.slots
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))

getSlots.methods = ['POST']
