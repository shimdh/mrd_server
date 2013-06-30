# -*- coding: utf-8 -*-

from models import User, DirtyLog
import datetime
from database import db_session
from sqlalchemy import exc


class ResultCodes(object):
    """docstring for ResultCodes"""
    (
        Success,
        NicknameExist,
        NicknameNonExist,
        UserPasswordWrong,
        InputParamError,
        SessionIdNonExist,
        SessionIdExpired,
        NoData,
        GameVersionError,
        DBInputError,
        DataExist,
        ShortNickname,
        ShortPassword
    ) = range(100, 113)

    AccessError = 200


class ProtocolTypes(object):
    """docstring for ProtocolTypes"""
    (
        RegisterUser, LoginUser, CreateCharacter, GetNotice,
        GetCharacter, CheckGameVersion, AddFriend, GetFriendsList,
        FindFriendByName, GetInventories, SetInventories,
        GetSlots, SetSlots, GetStats, SetStats, WriteMail, ReadMail,
        GetGiftMail, GetMailList, DeleteMails, SetOwnCostumes, GetOwnCostumes,
        GetOwnCostumeBases, SetOwnCostumeBases, RequestFriend,
        GetWaitingFriends, AcceptFriend, GetFriendCharacterInfo,
        AddCompletedEvent, GetFishing, AddOwnCostume, AddOwnCostumeBase,
        SendFriendShipPoint, ReceiveFriendShipPoint,
        SetButtonState, GetButtonState, SetSavedStory, GetSavedStory,
        SetSavedCurrentZone, GetSavedCurrentZone,
        AddPuzzlePiece, GetPuzzlePieces, AddPuzzle, GetPuzzles,
        AddDiary, GetDiaries, SetWornCostume, GetWornCostume,
        SetCash, GetCash,
    ) = range(100, 150)


def checkSessionId(got_session_id):
    got_user = User.query.filter_by(session_id=got_session_id).first()
    if not got_user:
        return ResultCodes.SessionIdNonExist, None
    else:
        if got_user.session_date < (
                datetime.datetime.now() - datetime.timedelta(minutes=20)):
            got_user.session_id = ''
            db_session.add(got_user)
            try:
                db_session.commit()
                return ResultCodes.SessionIdExpired, None
            except exc.SQLAlchemyError:
                return ResultCodes.DBInputError, None
        else:

            got_user.session_date = datetime.datetime.now()
            db_session.add(got_user)
            try:
                db_session.commit()
                return ResultCodes.Success, got_user
            except exc.SQLAlchemyError:
                return ResultCodes.DBInputError, None


def checkContainKeys(my_list, my_dict):
    return len(
        [x for x in my_list if x in my_dict and my_dict[x]]) == len(my_list)


def commitData():
    try:
        db_session.commit()
        return ResultCodes.Success
    except exc.SQLAlchemyError:
        return ResultCodes.DBInputError

def writeDirtyLog(all_string):
    write_log = DirtyLog(all_string)
    db_session.add(write_log)
    db_session.commit()