from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy import Sequence
from sqlalchemy.orm import sessionmaker

import hashlib
import json
import datetime
from random import sample, randrange

engine = create_engine('mysql://root:2629@localhost/mrd_test', echo=True)
engine.execute("select 1").scalar()

Base = declarative_base()

SESS_CHARS = 'abcdefghijkmpqrstuvwxyzABCDEFGHIJKLMNPQRST23456789'


def get_sesseion_id(userid):
    return userid + ''.join(sample(SESS_CHARS, randrange(5, 20)))


class User(Base):
    """docstring for User"""
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    user_id = Column(String(16))
    password = Column(String(250))
    email = Column(String(50))
    gender = Column(String(1), default='M')
    character = Column(Text())
    slot_item = Column(Text())
    resurrect = Column(Text())
    clothes = Column(Text())
    session_id = Column(String(100))
    session_date = Column(DateTime())
    registered_date = Column(DateTime(), default=datetime.datetime.now())

    def __init__(self, user_id, password):
        self.user_id = user_id
        self.password = password

        self.character = json.dumps(self.initChracter())
        self.slot_item = json.dumps(self.initSlotItem())
        self.resurrect = json.dumps(self.initResurrect())

    def __repr__(self):
        return "<User('%s','%s')>" % (self.user_id, self.password)

    def initChracter(self):
        temp_character = {
            "level": 1,
            "weapon_level": 1,
            "hp": 100,
            "exp": 100,
            "weapon_exp": 100,
            "name": "abc",
            "gender": "M",
            "stone_count": 1,
            "hair_color": "aaa",
            "hair_style": "aaa",
            "face_type": "aaa",
            "character_body_type": "aaa",
            "cloak_type": "aaa",
            "weapon_type": "aaa"
        }
        return temp_character

    def initSlotItem(self):
        temp_slot_item = {
            "skill_stone_wide_1": [0, 0, 0],
            "skill_stone_wide_2": [0, 0, 0],
            "skill_stone_wide_3": [0, 0, 0],
            "skill_stone_charge_1": [0, 0, 0],
            "skill_stone_charge_2": [0, 0, 0],
            "skill_stone_charge_3": [0, 0, 0],
            "skill_stone_whirlwind_1": [0, 0, 0],
            "skill_stone_whirlwind_2": [0, 0, 0],
            "skill_stone_whirlwind_3": [0, 0, 0],
            "passive_stone_1": [0, 0, 0],
            "passive_stone_2": [0, 0, 0],
            "passive_stone_3": [0, 0, 0],
            "passive_stone_4": [0, 0, 0]
        }
        return temp_slot_item

    def initResurrect(self):
        temp_resurrect = {
            "map": 0,
            "waypoint": 0
        }
        return temp_resurrect


Base.metadata.create_all(engine)

m = hashlib.md5()
m.update('edspassword')
ed_user = User('ed', m.hexdigest())
print ed_user.user_id
print ed_user.password

ed_user.session_id = get_sesseion_id(ed_user.user_id)
ed_user.session_date = datetime.datetime.now()

# Session = sessionmaker(bind=engine)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

session.add(ed_user)
our_user = session.query(User).filter_by(user_id='ed').first()
print our_user

session.commit()
