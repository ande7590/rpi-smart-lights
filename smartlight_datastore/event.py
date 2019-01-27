import os, sys, datetime 
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from config import DB_CONN_STR

SmartLightEventBase = declarative_base()

class SmartLightEvent(SmartLightEventBase):
    """Database Entity for representing a lightbulb event""" 
    __tablename__ = 'smartlight_event'
    event_id = Column(Integer, primary_key=True, autoincrement=True)
    event_priority = Column(Integer, default=100, nullable=False)
    event_start = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    event_end = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    event_data = Column(String, nullable=False)

engine = create_engine(DB_CONN_STR)

SmartLightEventBase.metadata.create_all(engine)