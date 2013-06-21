# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from database import Base

import hashlib
import json
import datetime
from random import sample, randrange

SESS_CHARS = 'abcdefghijkmpqrstuvwxyzABCDEFGHIJKLMNPQRST23456789'


def get_sesseion_id(nickname):
    return nickname + ''.join(sample(SESS_CHARS, randrange(5, 20)))


class Info(Base):
    """docstring for Info"""
    __tablename__ = 'infos'

    id = Column(Integer, primary_key=True)
    ap_recharged_time = Column(Integer())
    ios_game_version = Column(String(10))
    android_game_version = Column(String(10))

    def __init__(self, ios_game_version, android_game_version):
        self.ios_game_version = ios_game_version
        self.android_game_version = android_game_version

    def __repr__(self):
        return '<Info %s>' % (self.ap_recharged_time)


class User(Base):
    """docstring for User"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    nickname = Column(String(20), unique=True)
    name = Column(String(30))
    password = Column(String(200))
    email = Column(String(100), unique=True)
    gender = Column(String(1), default='M')
    character = Column(Text())
    slots = Column(Text())
    stats = Column(Text())
    resurrect = Column(Text())
    clothes = Column(Text())
    friends = Column(Text())
    inventories = Column(Text())
    session_id = Column(String(100))
    session_date = Column(DateTime())
    registered_date = Column(DateTime(), default=datetime.datetime.now())
    login_date = Column(DateTime())

    def __init__(self, nickname, name, password, email):
        self.nickname = nickname
        self.name = name
        self.password = password
        self.email = email

        self.resurrect = json.dumps(self.initResurrect())

    def __repr__(self):
        return '<User %s>' % (self.name)

    def initResurrect(self):
        temp_resurrect = {
            "map": 0,
            "waypoint": 0
        }
        return temp_resurrect


class Zone(Base):
    """docstring for Zone"""
    __tablename__ = 'zones'

    id = Column(Integer, primary_key=True)
    number = Column(Integer())
    fishing = Column(Text())

    def __init__(self, number):
        self.number = number
        self.fishing = json.dumps(self.initFishing)

    def __repr__(self):
        return "<Zone('%s')>" % (self.number)

    def initFishing(self):
        temp_fishing = {
            "pirateship_index": "",
            "pirateship_rate": 8,
            "special_pirateship_index": "",
            "special_pirateship_rate": 2,
            "itemindex_1": "",
            "count_1": 1,
            "rate_1": 13,
            "itemindex_2": "",
            "count_2": 1,
            "rate_2": 13,
            "itemindex_3": "",
            "count_3": 1,
            "rate_3": 13,
            "itemindex_4": "",
            "count_4": 1,
            "rate_4": 13,
            "itemindex_5": "",
            "count_5": 1,
            "rate_5": 13,
            "itemindex_6": "",
            "count_6": 1,
            "rate_6": 13,
            "itemindex_7": "",
            "count_7": 1,
            "rate_7": 13,
            "itemindex_8": "",
            "count_8": 1,
            "rate_8": 13,
            "itemindex_9": "",
            "count_9": 1,
            "rate_9": 13,
            "itemindex_10": "",
            "count_10": 1,
            "rate_10": 13,
            "itemindex_11": "",
            "count_11": 1,
            "rate_11": 13,
            "itemindex_12": "",
            "count_12": 1,
            "rate_12": 13,
            "itemindex_13": "",
            "count_13": 1,
            "rate_13": 13
        }
        return temp_fishing


class Notice(Base):
    """docstring for Notice"""
    __tablename__ = 'notices'

    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    content = Column(Text())
    opened = Column(Boolean(), default=False)
    modified_date = Column(DateTime(), default=datetime.datetime.now())

    def __init__(self, title, content):
        self.title = title
        self.content = content

    def __repr__(self):
        return "<Notice('%s')>" % (self.title)


class Mail(Base):
    """docstring for Mail"""
    __tablename__ = 'mails'

    id = Column(Integer, primary_key=True)
    from_nickname = Column(String(50))
    to_user_id = Column(String(50))
    content = Column(Text())
    items = Column(Text())
    registered_date = Column(DateTime(), default=datetime.datetime.now())

    def __init__(self, from_nickname, to_user_id, content, items=None):
        self.from_nickname = from_nickname
        self.to_user_id = to_user_id
        self.content = content
        self.items = items

    def __repr__(self):
        return "<Mail('%s')>" % (self.title)
