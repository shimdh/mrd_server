# -*- coding: utf-8 -*-

from models import User
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
    ) = range(100, 111)

    AccessError = 200


class ProtocolTypes(object):
    """docstring for ProtocolTypes"""
    (
        RegisterUser, LoginUser, CreateCharacter, GetNotice,
        GetCharacter, CheckGameVersion, AddFriend, GetFriendsList,
        FindFriendByNickname, GetInventories, SetInventories,
        GetSlots, SetSlots, GetStats, SetStats, WriteMail, ReadMail,
        GetGiftMail, GetMailList, DeleteMails, SetOwnCostumes, GetOwnCostumes,
        GetOwnCostumeBases, SetOwnCostumeBases, RequestFriend, GetWaitingFriends,
        AcceptFriend,
    ) = range(100, 127)


def checkSessionId(got_session_id):
    got_user = User.query.filter_by(session_id=got_session_id).first()
    if not got_user:
        return ResultCodes.SessionIdNonExist, None
    else:
        if got_user.session_date < datetime.datetime.now() - datetime.timedelta(minutes=10):
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
    return len([x for x in my_list if x in my_dict]) > 0
