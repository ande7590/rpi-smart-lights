from event import SmartLightEvent, SmartLightEventBase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from config import DB_CONN_STR

class SmartLightEventRepository():

    def __init__(self):
        self.__engine = create_engine(DB_CONN_STR)
        SmartLightEventBase.metadata.bind = self.__engine
        self.__dbSessionMaker = sessionmaker(bind=self.__engine)
        self.__inSession = False
    
    @contextmanager
    def session_scope(self):        
        if self.__inSession == True:
            raise Error("SmartLightEventRepository: already inside of a session")
        else:
            self.__inSession = True

        session = self.__dbSessionMaker()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            self.__inSession = False
            session.close()
