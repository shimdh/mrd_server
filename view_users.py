# -*- coding: utf-8 -*-

from flask import request
from utils import ProtocolTypes, ResultCodes, checkContainKeys
import json
import datetime

from database import db_session
from models import User, get_session_id
from sqlalchemy import exc


def register():
    result = dict(
        type=ProtocolTypes.RegisterUser,
        result=ResultCodes.Success
    )

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
                    import re
                    if (
                        (not re.match(
                            "^[A-Za-z0-9_-]*$",
                            got_data['nickname'])) or
                        (not re.match(
                            "^[A-Za-z0-9_-]*$",
                            got_data['password']))
                    ):
                        ResultCodes.InputParamError
                    else:
                        if User.query.filter_by(
                                nickname=got_data['nickname']).first():
                            result['result'] = ResultCodes.NicknameExist
                        else:
                            user_data = User(
                                got_data['nickname'],
                                got_data['password']
                            )
                            db_session.add(user_data)
                            try:
                                db_session.commit()
                            except exc.SQLAlchemyError:
                                result["result"] = ResultCodes.DBInputError

        else:
            result["result"] = ResultCodes.InputParamError
    else:
        result["result"] = ResultCodes.AccessError

    return str(json.dumps(result))

register.methods = ['POST']


def login():
    result = dict(
        type=ProtocolTypes.LoginUser,
        result=ResultCodes.Success
    )

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])

        from_keys = ['nickname', 'password']
        if checkContainKeys(from_keys, got_data):
            if got_data['nickname'] == '' or got_data['password'] == '':
                result["result"] = ResultCodes.InputParamError
            else:
                got_user = User.query.filter_by(
                    nickname=got_data['nickname']).first()
                if got_user:
                    if got_user.password == got_data['password']:
                        got_user.session_id = get_session_id(got_user.nickname)
                        got_user.session_date = datetime.datetime.now()
                        got_user.login_date = datetime.datetime.now()
                        db_session.add(got_user)
                        try:
                            db_session.commit()
                            result['session_id'] = got_user.session_id
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
