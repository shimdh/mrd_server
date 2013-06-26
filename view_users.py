# -*- coding: utf-8 -*-

from flask import request
from utils import ProtocolTypes, ResultCodes, checkContainKeys
import json
import datetime

from database import db_session
from models import User, get_session_id
from sqlalchemy import exc


def register():
    result = {'type': ProtocolTypes.RegisterUser}

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])

        from_keys = ['nickname', 'password']
        if checkContainKeys(from_keys, got_data):
            if got_data['nickname'] == '' or got_data['password'] == '':
                result["result"] = ResultCodes.InputParamError
            else:
                if len(got_data['nickname']) < 4:
                    result['result'] = ResultCodes.ShortNickname
                elif len(got_data['password']) < 4:
                    result['result'] = ResultCodes.ShortPassword
                else:
                    if len(
                            [e for e in got_data['nickname'] if e.isalnum()]
                    ) != len(
                            got_data['nickname']
                    ) or len(
                            [e for e in got_data['password'] if e.isalnum()]
                    ) != len(got_data['password']):
                        ResultCodes.InputParamError
                    else:
                        if User.query.filter_by(nickname=got_data['nickname']).first():
                            result['result'] = ResultCodes.NicknameExist
                        else:
                            user_data = User(
                                got_data['nickname'],
                                got_data['password']
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
            got_user = User.query.filter_by(nickname=got_data['nickname']).first()
            if got_user:
                if got_user.password == got_data['password']:
                    got_user.session_id = get_session_id(got_user.nickname)
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
                result['result'] = ResultCodes.NicknameNonExist
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))

login.methods = ['POST']
