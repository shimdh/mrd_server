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

    if not models.Info.query.first():
        temp_info = models.Info('1.0.0', '1.0.0')
        db_session.add(temp_info)
        db_session.commit()


def del_db():
    infos = Table('infos', Base.metadata)
    infos.drop(engine)

    users = Table('users', Base.metadata)
    users.drop(engine)

    zones = Table('zones', Base.metadata)
    zones.drop(engine)

    notices = Table('notices', Base.metadata)
    notices.drop(engine)

    mails = Table('mails', Base.metadata)
    mails.drop(engine)

