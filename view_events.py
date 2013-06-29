# -*- coding: utf-8 -*-

from flask import request
from utils import ProtocolTypes, ResultCodes, checkSessionId, checkContainKeys, commitData
import json

from database import db_session
from sqlalchemy import exc
from models import CompletedEvent


def addCompletedEvent():
    result = {'type': ProtocolTypes.AddCompletedEvent}

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])
        from_keys = ['session_id', 'event_index']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                find_event = CompletedEvent.query.filter_by(
                    user_id=got_user.id, event_index=got_data['event_index']).first()
                if find_event:
                    result['result'] = ResultCodes.DataExist
                else:
                    new_event = CompletedEvent(got_user.id, got_data['event_index'])
                    db_session.add(new_event)
                    result['result'] = commitData()
                    # try:
                    #     db_session.commit()
                    # except exc.SQLAlchemyError:
                    #     result['result'] = ResultCodes.DBInputError
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))

addCompletedEvent.methods = ['POST']