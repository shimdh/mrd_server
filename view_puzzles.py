# -*- coding: utf-8 -*-

from flask import request
from models import OpenedPuzzlePiece
from utils import ProtocolTypes, ResultCodes, checkSessionId, checkContainKeys, commitData
import json

from database import db_session
import datetime


def addOpenedPuzzlePiece():
    result = dict(
        type=ProtocolTypes.AddPuzzlePiece,
        result=ResultCodes.Success
        )

    if request.methods == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])
        from_keys = ['session_id', 'puzzle_index', 'condition']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                find_puzzle_piece = OpenedPuzzlePiece.query.filter_by(
                    user_id=got_user.id, puzzle_index=got_data['puzzle_index']).first()
                if find_puzzle_piece:
                    find_puzzle_piece.condition = got_data['condition']
                    db_session.add(find_puzzle_piece)
                else:
                    made_puzzle_piece = OpenedPuzzlePiece(got_user.id, got_data['puzzle_index'], got_data['condition'])
                    db_session.add(made_puzzle_piece)

                result['result'] = commitData()
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))

addOpenedPuzzlePiece.methods = ['POST']


def getOpenedPuzzlePieces():
    result = dict(
        type=ProtocolTypes.GetPuzzlePieces,
        result=ResultCodes.Success)

    if request.methods == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])
        from_keys = ['session_id']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                find_puzzle_pieces = OpenedPuzzlePiece.query.filter_by(user_id=got_user.id).all()
                if find_puzzle_pieces:
                    send_list = list()
                    for find_puzzle_piece in find_puzzle_pieces:
                        tmp_piece = dict(
                            puzzle_index=find_puzzle_piece.puzzle_index,
                            condition=find_puzzle_piece.condition)
                        send_list.append(tmp_piece)

                    result['puzzle_pieces'] = json.dumps(send_list)
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))

getOpenedPuzzlePieces.methods = ['POST']
