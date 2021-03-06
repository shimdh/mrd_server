# -*- coding: utf-8 -*-

from flask import request
from models import Button, SavedStory, SavedCurrentZone
from utils import ProtocolTypes, ResultCodes, checkSessionId, checkContainKeys, commitData
import json

from database import db_session
from sqlalchemy import exc
import datetime


def setButtonState():
    result = dict(
        type=ProtocolTypes.SetButtonState,
        result=ResultCodes.Success)

    if request.form['data']:
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

                result['result'] = commitData()
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))


setButtonState.methods = ['POST']


def getButtonState():
    result = dict(
        type=ProtocolTypes.GetButtonState,
        result=ResultCodes.Success)

    if request.form['data']:
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
                    result['result'] = ResultCodes.NoData
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))


getButtonState.methods = ['POST']


def setSavedStory():
    result = dict(
        type=ProtocolTypes.SetSavedStory,
        result=ResultCodes.Success)

    if request.form['data']:
        got_data = json.loads(request.form['data'])
        from_keys = [
            'session_id', 
            'zone_index',
            # 'episode_no',
            # 'wave_no',
            # 'position',
            # 'rotation',
        ]
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                find_story = SavedStory.query.filter_by(
                    user_id=got_user.id).first()
                if find_story:
                    find_story.zone_index = got_data['zone_index']
                    find_story.episode_no = got_data['episode_no']
                    find_story.wave_no = got_data['wave_no']
                    find_story.position = json.dumps(got_data['position'])
                    find_story.rotation = json.dumps(got_data['rotation'])
                    find_story.updated_date = datetime.datetime.now()

                    db_session.add(find_story)
                else:
                    made_story = SavedStory(
                        got_user.id, 
                        got_data['zone_index'], 
                        got_data['episode_no'], 
                        got_data['wave_no'])
                    made_story.position = json.dumps(got_data['position'])
                    made_story.rotation = json.dumps(got_data['rotation'])

                    db_session.add(made_story)

                result['result'] = commitData()
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))


setSavedStory.methods = ['POST']


def getSavedStory():
    result = dict(
        type=ProtocolTypes.GetSavedStory,
        result=ResultCodes.Success)

    if request.form['data']:
        got_data = json.loads(request.form['data'])
        from_keys = ['session_id']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                find_story = SavedStory.query.filter_by(
                    user_id=got_user.id).first()
                if find_story:
                    tmp_result = dict(
                        zone_index=find_story.zone_index,
                        episode_no=find_story.episode_no,
                        wave_no=find_story.wave_no,
                        position=find_story.position,
                        rotation=find_story.rotation)
                    result.update(tmp_result)
                else:
                    result['result'] = ResultCodes.NoData
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))


getSavedStory.methods = ['POST']


def setSavedCurrentZone():
    result = dict(
        type=ProtocolTypes.SetSavedCurrentZone,
        result=ResultCodes.Success)

    def useFoundData(got_user_id, zone_index, episode, position, rotation):
        find_current_zone = SavedCurrentZone.query.filter_by(
            user_id=got_user_id).first()
        
        if find_current_zone:
            find_current_zone.zone_index = zone_index
            find_current_zone.episode = json.dumps(episode)
            find_current_zone.position = json.dumps(position)
            find_current_zone.rotation = json.dumps(rotation)
            find_current_zone.updated_date = datetime.datetime.now()

            return find_current_zone

        else:
            made_current_zone = SavedCurrentZone(got_user_id, zone_index)
            made_current_zone.episode = json.dumps(episode)
            made_current_zone.position = json.dumps(position)
            made_current_zone.rotation = json.dumps(rotation)
            made_current_zone.updated_date = datetime.datetime.now()

            return made_current_zone

    if request.form['data']:
        got_data = json.loads(request.form['data'])
        from_keys = [
            'session_id', 'zone_index', 'episode',
            'position', 'rotation']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                db_session.add(
                    useFoundData(
                        got_user.id, 
                        got_data['zone_index'],
                        got_data['episode'],
                        got_data['position'],
                        got_data['rotation']))

                result['result'] = commitData()
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))


setSavedCurrentZone.methods = ['POST']


def getSavedCurrentZone():
    result = dict(
        type=ProtocolTypes.GetSavedCurrentZone,
        result=ResultCodes.Success)

    def useFoundData(got_user_id):
        result_dict = dict()

        find_current_zone = SavedCurrentZone.query.filter_by(
            user_id=got_user_id).first()
        
        if find_current_zone:
            tmp_result = dict(
                zone_index=find_current_zone.zone_index,
                episode=find_current_zone.episode,
                position=find_current_zone.position,
                rotation=find_current_zone.rotation)
            result_dict.update(tmp_result)
        else:
            result_dict['result'] = ResultCodes.NoData

        return result_dict

    if request.form['data']:
        got_data = json.loads(request.form['data'])
        from_keys = ['session_id']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                result.update(useFoundData(got_user.id))                
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))


getSavedCurrentZone.methods = ['POST']
