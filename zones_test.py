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


class Zone(Base):
    """docstring for Zone"""
    __tablename__ = 'zones'

    id = Column(Integer, Sequence('zone_id_seq'), primary_key=True)
    number = Column(Integer())
    fishing = Column(Text())

    def __init__(self, number):
        self.number = number
        temp_fishing = {
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
        self.fishing = json.dumps(temp_fishing)

    def __repr__(self):
        return "<Zone('%s')>" % (self.number)


Base.metadata.create_all(engine)

ed_zone = Zone(0)
print ed_zone.number

# Session = sessionmaker(bind=engine)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

session.add(ed_zone)
our_zone = session.query(Zone).filter_by(number=0).first()
print our_zone

session.commit()
