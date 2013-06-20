# -*- coding: utf-8 -*-

from flask import request
from utils import ProtocolTypes, ResultCodes, checkContainKeys
import json

from models import Notice, Info


def getNotice():
    result = {'type': ProtocolTypes.GetNotice}

    got_notice = Notice.query.filter_by(opened=True).first()
    if not got_notice:
        result['result'] = ResultCodes.NoData
    else:
        result['result'] = ResultCodes.Success
        result['title'] = got_notice.title
        result['content'] = got_notice.content

    return str(json.dumps(result))

getNotice.methods = ['POST']


def checkGameVersion():
    result = {'type': ProtocolTypes.CheckGameVersion}

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])

        from_keys = ['game_version', 'os_type']
        if checkContainKeys(from_keys, got_data):
            got_info = Info.query.first()
            if not got_info:
                result['result'] = ResultCodes.NoData
            else:
                if got_data['os_type'] == 'android':
                    if got_data['game_version'] == got_info.android_game_version:
                        result['result'] = ResultCodes.Success
                    else:
                        result['result'] = ResultCodes.GameVersionError
                elif got_data['os_type'] == 'ios':
                    if got_data['game_version'] == got_info.ios_game_version:
                        result['result'] = ResultCodes.Success
                    else:
                        result['result'] = ResultCodes.GameVersionError
                else:
                    result['result'] = ResultCodes.GameVersionError
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))

checkGameVersion.methods = ['POST']
