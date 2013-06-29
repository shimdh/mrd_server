# -*- coding: utf-8 -*-

from flask import request
from utils import ProtocolTypes, ResultCodes, checkSessionId, checkContainKeys, commitData
import json

from database import db_session
from models import Mail
from sqlalchemy import exc


def writeMail():
    result = dict(
        type=ProtocolTypes.WriteMail,
        result=ResultCodes.Success
    )
    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])
        from_keys = ['session_id', 'mail_to', 'content']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                got_mail = Mail(
                    got_user.nickname, got_data['mail_to'], got_data['content'])
                db_session.add(got_mail)
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


writeMail.methods = ['POST']


def readMail():
    result = {'type': ProtocolTypes.ReadMail}

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])
        from_keys = ['session_id', 'mail_index']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                got_mail = Mail.query.filter_by(
                    id=got_data['mail_index']).first()
                if got_mail:
                    result['mail_index'] = got_mail.id
                    result['from_nickname'] = got_mail.from_nickname
                    result['sent_date'] = got_mail.registered_date.strftime(
                        "%Y,%m,%d,%H,%M")
                    result['title'] = got_mail.from_nickname + u"로부터 메일"
                    result['content'] = got_mail.content
                    if not got_mail.items or got_mail.items == '':
                        result['items'] = ''
                    else:
                        result['items'] = got_mail.items
                else:
                    result['result'] = ResultCodes.NoData
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))

readMail.methods = ['POST']


def getGiftMail():
    result = dict(
        type=ProtocolTypes.GetGiftMail,
        result=ResultCodes.Success
    )

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])
        from_keys = ['session_id', 'mail_index']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                got_mail = Mail.query.filter_by(
                    id=got_data['mail_index']).first()
                if got_mail:
                    got_mail.items = None
                    db_session.add(got_mail)
                    result['result'] = commitData()
                    # try:
                    #     db_session.commit()
                    # except exc.SQLAlchemyError:
                    #     result['result'] = ResultCodes.DBInputError
                else:
                    result['result'] = ResultCodes.NoData
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))

getGiftMail.methods = ['POST']


def getMailList():
    result = dict(
        type=ProtocolTypes.GetMailList,
        result=ResultCodes.Success
    )
    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])
        from_keys = ['session_id']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                got_mails = Mail.query.filter_by(
                    to_user_id=got_user.nickname).all()
                if got_mails:
                    result['mails'] = list()
                    for got_mail in got_mails:
                        temp_has_gift = 'N' if got_mail.items is None else 'Y'
                        temp_mail = {
                            'mail_index': got_mail.id,
                            'from_nickname': got_mail.from_nickname,
                            'sent_date': got_mail.registered_date.strftime(
                                "%Y,%m,%d,%H,%M"),
                            'title': got_mail.from_nickname + u"로부터 메일",
                            'gift': temp_has_gift,
                        }
                        result['mails'].append(temp_mail)
                else:
                    result['result'] = ResultCodes.NoData
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))

getMailList.methods = ['POST']


def deleteMails():
    result = dict(
        type=ProtocolTypes.DeleteMails,
        result=ResultCodes.Success
    )
    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])
        from_keys = ['session_id', 'mail_indexes']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                got_mails = db_session.query(Mail).filter(
                    Mail.id.in_(got_data['mail_indexes']))
                if got_mails:
                    for got_mail in got_mails:
                        db_session.delete(got_mail)
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

deleteMails.methods = ['POST']
