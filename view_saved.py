# -*- coding: utf-8 -*-

from flask import request
from models import Button
from utils import ProtocolTypes, ResultCodes, checkSessionId, checkContainKeys
import json

from database import db_session
from sqlalchemy import exc


def setButtonState():
    result = dict(
        type=ProtocolTypes.SetButtonState,
        result=ResultCodes.Success)

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])
        from_keys = ['session_id', 'button']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                find_button = Button.query.filter_by(
                    user_id=got_user.id).first()
                if find_button:
                    find_button.state = got_data['button']
                    db_session.add(find_button)
                else:
                    made_button = Button(got_user.id, got_data['button'])
                    db_session.add(made_button)

                try:
                    db_session.commit()
                except exc.SQLAlchemyError:
                    result['result'] = ResultCodes.DBInputError
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))


setButtonState.methods = ['POST']


def getButtonState():
    result = dict(
        type=ProtocolTypes.getButtonState,
        result=ResultCodes.Success)

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])
        from_keys = ['session_id']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                find_button = Button.query.filter_by(
                    user_id=got_user.id).first()
                if find_button:
                    result['button'] = find_button.state
                else:
                    result['return'] = ResultCodes.NoData
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))


getButtonState.methods = ['POST']


def setSavedStory():
    result = dict(
        type=ProtocolTypes.SetButtonState,
        result=ResultCodes.Success)

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])
        from_keys = [
            'session_id', 'zone_index', 'episode_no', 'wave_no',
            'position', 'rotation']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                find_button = Button.query.filter_by(
                    user_id=got_user.id).first()
                if find_button:
                    find_button.state = got_data['button']
                    db_session.add(find_button)
                else:
                    made_button = Button(got_user.id, got_data['button'])
                    db_session.add(made_button)

                try:
                    db_session.commit()
                except exc.SQLAlchemyError:
                    result['result'] = ResultCodes.DBInputError
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))


setSavedStory.methods = ['POST']
