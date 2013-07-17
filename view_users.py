# -*- coding: utf-8 -*-

from flask import request
from utils import ProtocolTypes, ResultCodes, checkContainKeys, commitData, checkSessionId, writeDirtyLog
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

    def checkValidNicknamePassword(nickname, password):
        import re

        check_all_letters = lambda given_value: re.match("^[A-Za-z0-9_-]*$", given_value)
        if (
                not check_all_letters(nickname) or
                not check_all_letters(password)
        ):
            return False
        else:
            return True

    def checkReservedNickname(nickname):
        reserved_nickname = [
            'system', 'admin', 'administrator', 'root'
        ]
        if nickname in reserved_nickname:
            return False
        else:
            return True
            
    def checkFindNickname(nickname):
        finding_user = User.query.filter_by(nickname=nickname).first()

        if finding_user:
            return True
        else:
            return False

    if request.form['data']:
        got_data = json.loads(request.form['data'])

        from_keys = ['nickname', 'password']
        if checkContainKeys(from_keys, got_data):
            got_nickname, got_password = got_data['nickname'], got_data['password']

            if got_nickname == '' or got_password == '':
                result["result"] = ResultCodes.InputParamError
            else:
                if len(got_nickname) < 4:
                    result['result'] = ResultCodes.ShortNickname
                elif len(got_password) < 4:
                    result['result'] = ResultCodes.ShortPassword
                else:
                    if (checkValidNicknamePassword(
                        got_nickname, 
                        got_password
                        ) and checkReservedNickname(got_nickname)):
                        if checkFindNickname(got_nickname):
                            result['result'] = ResultCodes.NicknameExist
                        else:
                            user_data = User(
                                got_nickname,
                                got_password)
                            db_session.add(user_data)
                            result['result'] = commitData()
                    else:
                        result["result"] = ResultCodes.InputParamError
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

    if request.form['data']:
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


def setCash():
    result = dict(
        type=ProtocolTypes.SetCash,
        result=ResultCodes.Success)

    writeDirtyLog('setCash: ' + request.form['data'])

    if request.form['data']:
        got_data = json.loads(request.form['data'])
        from_keys = [
            'session_id', 'cash']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                got_user.cash = got_data['cash'] or 0
                db_session.add(got_user)

                result['result'] = commitData()
            else:
                result['result'] = ResultCodes.NoData
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))


setCash.methods = ['POST']


def getCash():
    result = dict(
        type=ProtocolTypes.GetCash,
        result=ResultCodes.Success)

    if request.form['data']:
        got_data = json.loads(request.form['data'])
        from_keys = [
            'session_id']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                result['cash'] = got_user.cash
            else:
                result['result'] = ResultCodes.NoData
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))


getCash.methods = ['POST']

