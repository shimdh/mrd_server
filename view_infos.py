# -*- coding: utf-8 -*-

from flask import request
from utils import ProtocolTypes, ResultCodes, checkContainKeys
import json

from models import Notice, Info


def getNotice():
    result = dict(
        type=ProtocolTypes.GetNotice,
        result=ResultCodes.Success
    )

    got_notice = Notice.query.filter_by(opened=True).first()
    if not got_notice:
        result['result'] = ResultCodes.NoData
    else:
        result['title'] = got_notice.title
        result['content'] = got_notice.content

    return str(json.dumps(result))

getNotice.methods = ['POST']


def checkGameVersion():
    result = dict(
        type=ProtocolTypes.CheckGameVersion,
        result=ResultCodes.Success
    )
    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])

        from_keys = ['game_version', 'os_type']
        if checkContainKeys(from_keys, got_data):
            got_info = Info.query.first()
            if not got_info:
                result['result'] = ResultCodes.NoData
            else:
                version_check = lambda ver: ver == got_data['game_version']
                if got_data['os_type'].lower() == 'android':
                    if not version_check(got_info.android_game_version):
                        result['result'] = ResultCodes.GameVersionError
                    # if got_data['game_version'] != got_info.android_game_version:
                    #     result['result'] = ResultCodes.GameVersionError
                elif got_data['os_type'].lower() == 'ios':
                    if not version_check(got_info.ios_game_version):
                        result['result'] = ResultCodes.GameVersionError
                    # if got_data['game_version'] != got_info.ios_game_version:
                    #     result['result'] = ResultCodes.GameVersionError
                else:
                    result['result'] = ResultCodes.GameVersionError
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))

checkGameVersion.methods = ['POST']
