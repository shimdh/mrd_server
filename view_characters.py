# -*- coding: utf-8 -*-

from flask import request
from utils import ProtocolTypes, ResultCodes, checkSessionId, checkContainKeys
import json

from database import db_session
from sqlalchemy import exc

from models import Character


def createCharacter():
    result = {'type': ProtocolTypes.CreateCharacter}

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])

        from_keys = ['session_id', 'character']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])
            if got_user:
                got_character = Character.query.filter_by(user_id=got_user.id).first()
                if got_character:
                    result['result'] = ResultCodes.DataExist
                else:
                    got_character = got_data['character']
                    got_user.name = got_character['name']
                    db_session.add(got_user)

                    user_character = Character(got_user.id, got_character['name'])
                    user_character.body_type = got_character['body_type']
                    user_character.cloak_type = got_character['cloak_type']
                    user_character.color_r = got_character['color_r']
                    user_character.color_g = got_character['color_g']
                    user_character.color_b = got_character['color_b']
                    user_character.face_type = got_character['face_type']
                    user_character.gender = got_character['gender']
                    user_character.hair_type = got_character['hair_type']
                    user_character.weapon_type = got_character['weapon_type']
                    db_session.add(user_character)
                    try:
                        db_session.commit()
                    except exc.SQLAlchemyError:
                        result['result'] = ResultCodes.DBInputError
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))

createCharacter.methods = ['POST']


def getCharacter():
    result = {'type': ProtocolTypes.GetCharacter}

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])

        from_keys = ['session_id']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                find_character = Character.query.filter_by(user_id=got_user.id).first()
                if find_character:
                    got_character = dict(
                        name=find_character.name,
                        body_type=find_character.body_type,
                        cloak_type=find_character.cloak_type,
                        color_r=find_character.color_r,
                        color_g=find_character.color_g,
                        color_b=find_character.color_b,
                        face_type=find_character.face_type,
                        gender=find_character.gender,
                        hair_type=find_character.hair_type,
                        weapon_type=find_character.weapon_type)

                    result['character'] = json.dumps(got_character)
                else:
                    result['result'] = ResultCodes.NoData
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))

getCharacter.methods = ['POST']
