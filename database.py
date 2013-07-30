from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import serverconfig

# engine = create_engine('mysql://mrd_srv:slfmqksk!@127.0.0.1/mrd_test',
#   echo=True, convert_unicode=True)
# engine = create_engine('mysql://mrd_srv:slfmqksk!@210.122.0.211/mrd_test',
#   echo=True, convert_unicode=True)
engine = create_engine(
    serverconfig.DATABASE_URI, echo=True, convert_unicode=True)
db_session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import models

    Base.metadata.create_all(bind=engine)

    if models.Info.query.count() == 0:
        temp_info = models.Info('1.0.0', '1.0.0')
        db_session.add(temp_info)
        db_session.commit()

    if models.Costumebase.query.count() == 0:
        temp_costumebase_1 = models.Costumebase(
            'COB_001', 0, 0, 'COS_001', 'COS_002', 'COS_003', 'COS_004')
        temp_costumebase_2 = models.Costumebase(
            'COB_C01', 1, 5, 'COS_C01', 'COS_C02', 'COS_C03', 'COS_C04')
        temp_costumebase_3 = models.Costumebase(
            'COB_D01', 1, 3, 'COS_D01', 'COS_D02', 'COS_D03', 'COS_D04')
        temp_costumebase_4 = models.Costumebase(
            'COB_C51', 1, 2, 'COS_C51', 'COS_C52', 'COS_C53', 'COS_C54')
        temp_costumebase_5 = models.Costumebase(
            'COB_X01', 1, 1, 'COS_X01', 'COS_X02', 'COS_X03', 'COS_X04')
        temp_costumebase_6 = models.Costumebase(
            'COB_X05', 1, 1, 'COS_X05', 'COS_X06', 'COS_X07', 'COS_X08')
        temp_costumebase_7 = models.Costumebase(
            'COB_X09', 1, 1, 'COS_X09', 'COS_X10', 'COS_X11', 'COS_X12')

        db_session.add_all(
            [temp_costumebase_1, temp_costumebase_2, temp_costumebase_3,
                temp_costumebase_4, temp_costumebase_5, temp_costumebase_6,
                temp_costumebase_7])

        db_session.commit()

    if models.Fishing.query.count() == 0:
        temp_fishing_1 = models.Fishing('ZON_021')
        temp_fishing_1.no_item = 0
        temp_fishing_1.general_ship_index = 'MOB_Y01'
        temp_fishing_1.general_ship_rate = 8
        temp_fishing_1.special_ship_index = 'MOB_Z01'
        temp_fishing_1.special_ship_rate = 2
        temp_fishing_1.item_index_1 = 'WUS_001'
        temp_fishing_1.item_count_1 = 1
        temp_fishing_1.item_rate_1 = 13
        temp_fishing_1.item_index_2 = 'SKS_A01'
        temp_fishing_1.item_count_2 = 1
        temp_fishing_1.item_rate_2 = 18
        temp_fishing_1.item_index_3 = 'SKS_P01'
        temp_fishing_1.item_count_3 = 1
        temp_fishing_1.item_rate_3 = 28
        temp_fishing_1.item_index_4 = 'WUS_001'
        temp_fishing_1.item_count_4 = 2
        temp_fishing_1.item_rate_4 = 5
        temp_fishing_1.item_index_5 = 'SKS_A01'
        temp_fishing_1.item_count_5 = 2
        temp_fishing_1.item_rate_5 = 5
        temp_fishing_1.item_index_6 = 'SKS_P01'
        temp_fishing_1.item_count_6 = 2
        temp_fishing_1.item_rate_6 = 5
        temp_fishing_1.item_index_7 = 'WUS_001'
        temp_fishing_1.item_count_7 = 3
        temp_fishing_1.item_rate_7 = 2
        temp_fishing_1.item_index_8 = 'SKS_A01'
        temp_fishing_1.item_count_8 = 3
        temp_fishing_1.item_rate_8 = 2
        temp_fishing_1.item_index_9 = 'SKS_P01'
        temp_fishing_1.item_count_9 = 3
        temp_fishing_1.item_rate_9 = 2
        temp_fishing_1.item_index_10 = ''
        temp_fishing_1.item_count_10 = 0
        temp_fishing_1.item_rate_10 = 0
        temp_fishing_1.item_index_11 = 'ETC_006'
        temp_fishing_1.item_count_11 = 1
        temp_fishing_1.item_rate_11 = 5
        temp_fishing_1.item_index_12 = 'ETC_006'
        temp_fishing_1.item_count_12 = 2
        temp_fishing_1.item_rate_12 = 4
        temp_fishing_1.item_index_13 = 'ETC_006'
        temp_fishing_1.item_count_13 = 3
        temp_fishing_1.item_rate_13 = 1

        db_session.add(temp_fishing_1)
        db_session.commit()

    if models.Config.query.count() == 0:
        sending_friendship_point = models.Config('sending_friendship_point', str(10))
        receiving_friendship_point = models.Config('receiving_friendship_point', str(10))
        max_friendship_point = models.Config('max_friendship_point', str(100))

        db_session.add_all(
            [
                sending_friendship_point,
                receiving_friendship_point,
                max_friendship_point,
            ]
        )
        db_session.commit()


def del_db():
    import models

    Base.metadata.drop_all(bind=engine)
