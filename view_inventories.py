# -*- coding: utf-8 -*-

from flask import request
from utils import ProtocolTypes, ResultCodes, checkSessionId, checkContainKeys
import json

from database import db_session
from sqlalchemy import exc


def getInventories():
    result = {'type': ProtocolTypes.GetInventories}

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])

        from_keys = ['session_id']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                if (got_user.inventories is None) or (got_user.inventories == ''):
                    result['result'] = ResultCodes.NoData
                else:
                    got_inventories = json.loads(got_user.inventories)
                    if got_inventories:
                        if len(got_inventories) == 0:
                            result['result'] = ResultCodes.NoData
                        else:
                            result['inventories'] = got_user.inventories
                    else:
                        result['result'] = ResultCodes.NoData
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))


getInventories.methods = ['POST']


def setInventories():
    result = {'type': ProtocolTypes.SetInventories}

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])

        from_keys = ['session_id', 'inventories']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                got_user.inventories = json.dumps(got_data['inventories'])
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

setInventories.methods = ['POST']
