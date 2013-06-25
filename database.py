from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table
import serverconfig

# engine = create_engine('mysql://mrd_srv:slfmqksk!@127.0.0.1/mrd_test', echo=True, convert_unicode=True)
# engine = create_engine('mysql://mrd_srv:slfmqksk!@210.122.0.211/mrd_test', echo=True, convert_unicode=True)
engine = create_engine(serverconfig.DATABASE_URI, echo=True, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

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
        temp_costumebase_1 = models.Costumebase('COB_001', 0, 0, 'COS_001', 'COS_002', 'COS_003', 'COS_004')
        temp_costumebase_2 = models.Costumebase('COB_C01', 1, 5, 'COS_C01', 'COS_C02', 'COS_C03', 'COS_C04')
        temp_costumebase_3 = models.Costumebase('COB_D01', 1, 3, 'COS_D01', 'COS_D02', 'COS_D03', 'COS_D04')
        temp_costumebase_4 = models.Costumebase('COB_C51', 1, 2, 'COS_C51', 'COS_C52', 'COS_C53', 'COS_C54')
        temp_costumebase_5 = models.Costumebase('COB_X01', 1, 1, 'COS_X01', 'COS_X02', 'COS_X03', 'COS_X04')
        temp_costumebase_6 = models.Costumebase('COB_X05', 1, 1, 'COS_X05', 'COS_X06', 'COS_X07', 'COS_X08')
        temp_costumebase_7 = models.Costumebase('COB_X09', 1, 1, 'COS_X09', 'COS_X10', 'COS_X11', 'COS_X12')
        
        db_session.add(temp_costumebase_1)
        db_session.add(temp_costumebase_2)
        db_session.add(temp_costumebase_3)
        db_session.add(temp_costumebase_4)
        db_session.add(temp_costumebase_5)
        db_session.add(temp_costumebase_6)
        db_session.add(temp_costumebase_7)
        
        db_session.commit()      
      

def del_db():
    Base.metadata.drop_all(bind=engine)


