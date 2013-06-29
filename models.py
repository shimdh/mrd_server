# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy import DateTime, Boolean, Date, Float
from database import Base

import json
import datetime
from random import sample, randrange

SESS_CHARS = 'abcdefghijkmpqrstuvwxyzABCDEFGHIJKLMNPQRST23456789'


def get_session_id(nickname):
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
    nickname = Column(String(20), unique=True, nullable=False)
    name = Column(String(30), unique=True)
    password = Column(String(200), nullable=False)
    email = Column(String(100), unique=True)
    gender = Column(String(1), default='M')
    character = Column(Text())
    slots = Column(Text())
    resurrect = Column(Text())
    clothes = Column(Text())
    friendship_point = Column(Integer(), default=0)
    inventories = Column(Text())
    cashes = Column(Integer(), default=0)
    session_id = Column(String(100))
    session_date = Column(DateTime())
    registered_date = Column(DateTime(), default=datetime.datetime.now())
    login_date = Column(DateTime())

    def __init__(self, nickname, password):
        self.nickname = nickname
        self.password = password

        self.resurrect = json.dumps(self.initResurrect())

    def __repr__(self):
        return '<User %s>' % (self.name)

    def initResurrect(self):
        temp_resurrect = {
            "map": 0,
            "waypoint": 0
        }
        return temp_resurrect


class SavedStory(Base):
    """docstring for SavedStory"""
    __tablename__ = 'saved_stories'

    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer())
    zone_index = Column(String(10))
    episode_no = Column(Integer())
    wave_no = Column(Integer())
    position = Column(Text())
    rotation = Column(Text())
    updated_date = Column(DateTime(), default=datetime.datetime.now())

    def __init__(self, user_id, zone_index, episode_no, wave_no):
        self.user_id = user_id
        self.zone_index = zone_index
        self.episode_no = episode_no
        self.wave_no = wave_no

    def __repr__(self):
        return '<SavedStory %s>' % self.zone_index


class SavedCurrentZone(Base):
    """docstring for SavedCurrentZone"""
    __tablename__ = 'saved_current_zones'

    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer())
    zone_index = Column(String(10))
    episode = Column(Text())
    position = Column(Text())
    rotation = Column(Text())
    updated_date = Column(DateTime(), default=datetime.datetime.now())

    def __init__(self, user_id, zone_index):
        self.user_id = user_id
        self.zone_index = zone_index

    def __repr__(self):
        return '<SavedCurrentZone %s>' % self.zone_index


class OpenedPuzzlePiece(Base):
    """docstring for OpendedPuzzlePiece"""
    __tablename__ = 'opended_puzzle_pieces'

    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer())
    puzzle_index = Column(Integer())
    condition = Column(Integer())

    def __init__(self, user_id, puzzle_index, condition):
        self.user_id = user_id
        self.puzzle_index = puzzle_index
        self.condition = condition
                        

class OpenedPuzzle(Base):
    """docstring for OpenedPuzzle"""
    __tablename__ = 'opened_puzzles'

    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer())
    puzzle_index = Column(Integer())
    opened = Column(Integer()) 

    def __init__(self, user_id, puzzle_index, opened):
        self.user_id = user_id
        self.puzzle_index = puzzle_index
        self.opened = opened


class Diary(Base):
    """docstring for Diary"""
    __tablename__ = 'diaries'

    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer())
    index = Column(Integer())
    opened = Column(Boolean())

    def __init__(self, user_id, index, opened):
        self.user_id = user_id
        self.index = index
        self.opened = opened

        
class WornCostume(Base):
    """docstring for WornCostume"""
    __tablename__ = 'worn_costumes'

    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer())
    costumes = Column(Text())

    def __init__(self, user_id, costumes):
        super(WornCostume, self).__init__()
        self.user_id = user_id
        self.costumes = costumes
        

class Button(Base):
    """docstring for Button"""
    __tablename__ = 'buttons'

    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer())
    state = Column(Text())

    def __init__(self, user_id, state):
        self.user_id = user_id
        self.state = state

    def __repr__(self):
        return '<Button %s>' % self.user_id


class Character(Base):
    __tablename__ = 'characters'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer())
    name = Column(String(20))
    level = Column(String(10))
    color_r = Column(String(15))
    color_g = Column(String(15))
    color_b = Column(String(15))
    gender = Column(String(1))
    hp = Column(String(20))
    weapon_level = Column(String(10))
    body_type = Column(String(100))
    hair_type = Column(String(100))
    cloak_type = Column(String(100))
    weapon_exp = Column(String(100))
    face_type = Column(String(100))
    weapon_type = Column(String(100))
    exp = Column(String(10))

    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

    def __repr__(self):
        return '<Character %s>' % self.name


class Stat(Base):
    __tablename__ = 'stats'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer())
    exp = Column(Integer())
    level = Column(Integer())
    hp = Column(Integer())
    weapon_level = Column(Integer())
    weapon_exp = Column(Integer())
    visited_zone_no = Column(String(10))
    updated_date = Column(DateTime(), default=datetime.datetime.now())

    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return '<Stat %d>' % self.user_id


class OwnCostumebase(Base):
    __tablename__ = 'own_costumebases'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer())
    costumebase_index = Column(String(10))
    lastdate_from_gotcash = Column(DateTime(), default=datetime.datetime.now())
    created_datetime = Column(DateTime(), default=datetime.datetime.now())

    def __init__(self, user_id, costumebase_index):
        self.user_id = user_id
        self.costumebase_index = costumebase_index

    def __repr__(self):
        return '<OwnCostumebase %s>' % self.costumebase_index


class OwnCostume(Base):
    __tablename__ = 'own_costumes'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer())
    costume_index = Column(String(10))
    created_datetime = Column(DateTime(), default=datetime.datetime.now())

    def __init__(self, user_id, costume_index):
        self.user_id = user_id
        self.costume_index = costume_index

    def __repr__(self):
        return '<OwnCostume %s>' % self.costume_index


class CompletedEvent(Base):
    __tablename__ = 'completed_events'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer())
    event_index = Column(String(20))
    created_datetime = Column(DateTime(), default=datetime.datetime.now())

    def __init__(self, user_id, event_index):
        self.user_id = user_id
        self.event_index = event_index

    def __repr__(self):
        return '<CompletedEvent %s>' % self.event_index


class LastVisitedWave(Base):
    """docstring for LastVisitedWave"""
    __tablename__ = 'last_visited_waves'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer())
    zone_index = Column(String(10))
    episode_no = Column(Integer())
    wave_no = Column(Integer())

    def __init__(self, user_id, zone_index, episode_no, wave_no):
        self.user_id = user_id
        self.zone_index = zone_index
        self.episode_no = episode_no
        self.wave_no = wave_no

    def __repr__(self):
        return '<LastVisitedWave %s>' % self.zone_index


class Friend(Base):
    __tablename__ = 'friends'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer())
    friend_id = Column(Integer())
    requested = Column(Boolean(), default=True)
    accepted = Column(Boolean(), default=False)
    friendship_received_date = Column(Date())
    friendship_sent_date = Column(Date())

    def __init__(self, user_id, friend_id):
        self.user_id = user_id
        self.friend_id = friend_id

    def __repr__(self):
        return '<Friend %s>' % (self.user_id)


class Costumebase(Base):
    __tablename__ = 'costumebases'
    id = Column(Integer, primary_key=True)
    index = Column(String(10), unique=True)
    cash_count = Column(Integer)
    duration = Column(Integer)
    weapon_index = Column(String(10))
    helmet_index = Column(String(10))
    armor_index = Column(String(10))
    cloak_index = Column(String(10))

    def __init__(
            self, index, cash_count, duration,
            weapon_index, helmet_index,
            armor_index, cloak_index):
        self.index = index
        self.cash_count = cash_count
        self.duration = duration
        self.weapon_index = weapon_index
        self.helmet_index = helmet_index
        self.armor_index = armor_index
        self.cloak_index = cloak_index

    def __repr__(self):
        return '<Costumebase %s>' % (self.index)


class Fishing(Base):
    __tablename__ = 'fishing'
    id = Column(Integer(), primary_key=True)
    zone_index = Column(String(10))
    no_item = Column(Float())
    general_ship_index = Column(String(10))
    general_ship_rate = Column(Float())
    special_ship_index = Column(String(10))
    special_ship_rate = Column(Float())
    item_index_1 = Column(String(10))
    item_count_1 = Column(Integer())
    item_rate_1 = Column(Float())
    item_index_2 = Column(String(10))
    item_count_2 = Column(Integer())
    item_rate_2 = Column(Float())
    item_index_3 = Column(String(10))
    item_count_3 = Column(Integer())
    item_rate_3 = Column(Float())
    item_index_4 = Column(String(10))
    item_count_4 = Column(Integer())
    item_rate_4 = Column(Float())
    item_index_5 = Column(String(10))
    item_count_5 = Column(Integer())
    item_rate_5 = Column(Float())
    item_index_6 = Column(String(10))
    item_count_6 = Column(Integer())
    item_rate_6 = Column(Float())
    item_index_7 = Column(String(10))
    item_count_7 = Column(Integer())
    item_rate_7 = Column(Float())
    item_index_8 = Column(String(10))
    item_count_8 = Column(Integer())
    item_rate_8 = Column(Float())
    item_index_9 = Column(String(10))
    item_count_9 = Column(Integer())
    item_rate_9 = Column(Float())
    item_index_10 = Column(String(10))
    item_count_10 = Column(Integer())
    item_rate_10 = Column(Float())
    item_index_11 = Column(String(10))
    item_count_11 = Column(Integer())
    item_rate_11 = Column(Float())
    item_index_12 = Column(String(10))
    item_count_12 = Column(Integer())
    item_rate_12 = Column(Float())
    item_index_13 = Column(String(10))
    item_count_13 = Column(Integer())
    item_rate_13 = Column(Float())

    def __init__(self, zone_index):
        self.zone_index = zone_index

    def __repr__(self):
        return '<Fishing %s>' % self.zone_index


class PirateShip(Base):
    __tablename__ = 'pirate_ships'

    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer())
    type = Column(String(1), default='g')
    hp = Column(Integer())
    died = Column(Boolean(), default=False)
    created_datetime = Column(DateTime(), default=datetime.datetime.now())

    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return '<PirateShip %s>' % self.user_id


class AttackedShipUser(Base):
    __tablename__ = 'attacked_ship_users'

    id = Column(Integer(), primary_key=True)
    ship_id = Column(Integer())
    user_id = Column(Integer())
    attack_point = Column(Integer())

    def __init__(self, ship_id, user_id):
        self.ship_id = ship_id
        self.user_id = user_id

    def __repr__(self):
        return '<AttackedShipUser %s>' % self.ship_id


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
