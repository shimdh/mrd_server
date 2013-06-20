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
    ) = range(100, 110)

    AccessError = 200


class ProtocolTypes(object):
    """docstring for ProtocolTypes"""
    (
        RegisterUser, LoginUser, CreateCharacter, GetNotice,
        GetCharacter, CheckGameVersion, AddFriend, GetFriendsList,
        FindFriendByNickname, GetInventories, SetInventories,
        GetSlots, SetSlots, GetStats, SetStats, WriteMail, ReadMail,
        GetGiftMail, GetMailList, DeleteMails,
    ) = range(100, 120)
