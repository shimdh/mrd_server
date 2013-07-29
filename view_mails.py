# -*- coding: utf-8 -*-

from flask import request
from utils import ProtocolTypes, ResultCodes, checkSessionId, checkContainKeys, commitData
import json

from database import db_session
from models import Mail

lst_from_system_mails = [
    -1, #System
    -2, #Ship
    -3,
]

def writeMail():
    result = dict(
        type=ProtocolTypes.WriteMail,
        result=ResultCodes.Success
    )
    if request.form['data']:
        got_data = json.loads(request.form['data'])
        from_keys = ['session_id', 'mail_to', 'content']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                got_friend = User.query.filter_by(user_id=got_data['mail_to']).first()
                if got_friend:
                    got_mail = Mail(
                        got_user.user_id, got_friend.user_id, got_data['content'])
                    db_session.add(got_mail)
                    result['result'] = commitData()
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))


writeMail.methods = ['POST']


def readMail():
    result = dict(
        type=ProtocolTypes.ReadMail,
        result=ResultCodes.Success)

    if request.form['data']:
        got_data = json.loads(request.form['data'])
        from_keys = ['session_id', 'mail_index']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                got_mail = Mail.query.filter_by(
                    id=got_data['mail_index']).first()
                if got_mail:
                    if not got_mail.from_user_id in lst_from_system_mails:
                        from_user_char = Character.query.filter_by(user_id=got_mail.from_user_id).first()
                        if from_user_char:
                            result['mail_index'] = got_mail.id
                            result['from_name'] = from_user_char.name
                            result['from_user_id'] = got_mail.from_user_id
                            result['sent_date'] = got_mail.registered_date.strftime(
                                "%Y,%m,%d,%H,%M")
                            result['title'] = got_mail.from_nickname + u"로부터 메일"
                            result['content'] = got_mail.content
                            if not got_mail.items or got_mail.items == '':
                                result['items'] = ''
                            else:
                                result['items'] = got_mail.items
                        else:
                            result['result'] = ResultCodes.InputParamError
                    else:
                        if got_mail.from_user_id == lst_from_system_mails[0]:
                            temp_mail_system_name = u"시스템"
                            temp_mail_title = u"시스템으로부터의 메일"
                        if got_mail.from_user_id == lst_from_system_mails[1]:
                            temp_mail_system_name = u"해적선"
                            temp_mail_title = u"해적선으로부터의 메일"
                        result['mail_index'] = got_mail.id
                        result['from_name'] = temp_mail_system_name
                        result['from_user_id'] = got_mail.from_user_id
                        result['sent_date'] = got_mail.registered_date.strftime(
                            "%Y,%m,%d,%H,%M")
                        result['title'] = temp_mail_title
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

    if request.form['data']:
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

    if request.form['data']:
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
                        temp_has_gift = 'Y'
                        if not got_mail.items or got_mail.items == '':
                            temp_has_gift = 'N'
                        temp_mail_type = 'N'
                        if got_mail.from_user_id == lst_from_system_mails[0]:
                            temp_mail_type = 'S'
                            temp_mail_system_name = u"시스템"
                            temp_mail_title = u"시스템으로부터의 메일"
                        if got_mail.from_user_id == lst_from_system_mails[1]:
                            temp_mail_type = 'P'
                            temp_mail_system_name = u"해적선"
                            temp_mail_title = u"해적선으로부터의 메일"
                        if not got_mail.from_user_id in lst_from_system_mails:
                            got_friend = User.query.filter_by(user_id=got_mail.from_user_id).first()
                            if got_friend:
                                got_friend_char = Character.query.filter_by(user_id=got_mail.from_user_id).first()
                                find_friend = Friend.query.filter_by(
                                    user_id=got_user.id, friend_id=got_mail.from_user_id,
                                    requested=True, accepted=True).first()
                                if find_friend:
                                    temp_mail_type = 'F'

                                temp_mail = {
                                    'mail_index': got_mail.id,
                                    'from_name': got_friend_char.name,
                                    'mail_type': temp_mail_type,
                                    'sent_date': got_mail.registered_date.strftime(
                                        "%Y,%m,%d,%H,%M"),
                                    'title': got_friend_char.name + u"로부터 메일",
                                    'got_item': got_mail.did_receive_item,
                                    'gift': temp_has_gift,
                                    'request_friend': got_mail.request_friend,
                                }
                                result['mails'].append(temp_mail)
                        else:
                            temp_mail = {
                                'mail_index': got_mail.id,
                                'from_name': temp_mail_system_name,
                                'mail_type': temp_mail_type,
                                'sent_date': got_mail.registered_date.strftime(
                                    "%Y,%m,%d,%H,%M"),
                                'title': temp_mail_title,
                                'got_item': got_mail.did_receive_item,
                                'gift': temp_has_gift,
                                'request_friend': got_mail.request_friend,
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
    if request.form['data']:
        got_data = json.loads(request.form['data'])
        from_keys = ['session_id', 'mail_indexes']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                got_mails = Mail.query.filter(
                    Mail.id.in_(got_data['mail_indexes'])).all()
                if got_mails:
                    for got_mail in got_mails:
                        db_session.delete(got_mail)
                    result['result'] = commitData()
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))

deleteMails.methods = ['POST']
