# -*- coding: utf-8 -*-

from flask import request
from utils import ProtocolTypes, ResultCodes, checkSessionId, checkContainKeys
import json

from database import db_session
from sqlalchemy import exc


def createCharacter():
    result = {'type': ProtocolTypes.CreateCharacter}

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])

        from_keys = ['session_id', 'character']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])
            if got_user:
                got_character = got_data['character']
                got_user.name = got_character['name']
                got_user.character = json.dumps(got_character)
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

createCharacter.methods = ['POST']


def getCharacter():
    result = {'type': ProtocolTypes.GetCharacter}

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])

        from_keys = ['session_id']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                if (got_user.character is None) or (got_user.character == ''):
                    result['result'] = ResultCodes.NoData
                else:
                    result['character'] = got_user.character
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))

getCharacter.methods = ['POST']
