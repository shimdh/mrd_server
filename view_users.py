# -*- coding: utf-8 -*-

from flask import request
from utils import ProtocolTypes, ResultCodes, checkContainKeys
import json
import datetime

from database import db_session
from models import User, get_sesseion_id
from sqlalchemy import exc


def register():
    result = {'type': ProtocolTypes.RegisterUser}

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])

        from_keys = ['nickname', 'name', 'password', 'email']
        if checkContainKeys(from_keys, got_data):
            if got_data['nickname'] == '' or got_data['password'] == '':
                result["result"] = ResultCodes.InputParamError
            else:
                if User.query.filter_by(nickname=got_data['nickname']).first():
                    result['result'] = ResultCodes.NicknameExist
                else:
                    user_data = User(
                        got_data['nickname'],
                        got_data['name'],
                        got_data['password'],
                        got_data['email']
                    )
                    db_session.add(user_data)
                    try:
                        db_session.commit()
                        result["result"] = ResultCodes.Success
                    except exc.SQLAlchemyError:
                        result["result"] = ResultCodes.DBInputError
        else:
            result["result"] = ResultCodes.InputParamError
    else:
        result["result"] = ResultCodes.AccessError

    return str(json.dumps(result))

register.methods = ['POST']


def login():
    result = {'type': ProtocolTypes.LoginUser}

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])

        from_keys = ['nickname', 'password']
        if checkContainKeys(from_keys, got_data):
            if not User.query.filter_by(nickname=got_data['nickname']).first():
                result['result'] = ResultCodes.NicknameNonExist
            else:
                got_user = User.query.filter_by(
                    nickname=got_data['nickname'],
                    password=got_data['password']).first()
                if got_user:
                    got_user.session_id = get_sesseion_id(got_user.nickname)
                    got_user.session_date = datetime.datetime.now()
                    got_user.login_date = datetime.datetime.now()
                    db_session.add(got_user)
                    try:
                        db_session.commit()
                        result['session_id'] = got_user.session_id
                        result['result'] = ResultCodes.Success
                    except exc.SQLAlchemyError:
                        result['result'] = ResultCodes.DBInputError
                else:
                    result['result'] = ResultCodes.UserPasswordWrong
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))

login.methods = ['POST']
