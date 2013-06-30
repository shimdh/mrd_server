# -*- coding: utf-8 -*-

from flask import request
from models import Diary
from utils import ProtocolTypes, ResultCodes, checkSessionId, checkContainKeys, commitData
import json

from database import db_session
import datetime


def addDiary():
    result = dict(
        type=ProtocolTypes.AddDiary,
        result=ResultCodes.Success
        )

    if request.methods == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])
        from_keys = ['session_id', 'diary_index']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                find_diary = Diary.query.filter_by(
                    user_id=got_user.id, diary_index=got_data['diary_index']).first()
                if find_diary:
                    result['result'] = ResultCodes.DataExist
                else:
                    made_diary = Diary(got_user.id, got_data['diary_index'])
                    db_session.add(made_diary)
                    result['result'] = commitData()
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))

addDiary.methods = ['POST']


def getDiaries():
    result = dict(
        type=ProtocolTypes.GetDiaries,
        result=ResultCodes.Success)
    result['result'] = ResultCodes.NoData

    # if request.form['data']:
    #     got_data = json.loads(request.form['data'])
    #     from_keys = ['session_id']
    #     if checkContainKeys(from_keys, got_data):
    #         result['result'], got_user = checkSessionId(got_data['session_id'])

    #         if got_user:
    #             find_diaries = Diary.query.filter_by(user_id=got_user.id).all()
    #             if find_diaries:
    #                 send_list = list()
    #                 for find_diary in find_diaries:
    #                     send_list.append(find_diary.diary_index)

    #                 result['diaries'] = json.dumps(send_list)
    #             else:
    #                 result['result'] = ResultCodes.NoData
    #     else:
    #         result['result'] = ResultCodes.InputParamError
    # else:
    #     result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))

getDiaries.methods = ['POST']