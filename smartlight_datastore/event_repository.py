import os, sys
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class SmartLightEventRepository():

    def __init__(self):
        pass

class SmartLightEvent(Base):
    __tablename__ = 'smartlight_event'

    
