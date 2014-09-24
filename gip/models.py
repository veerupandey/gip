from sqlalchemy import (
    Column,
    Integer,
    Text,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class MyModel(Base):
    __tablename__ = 'hostinfo'
    host = Column(Text, primary_key=True)
    ip=Column(Text)
    country = Column(Text)
    city = Column(Text)
    coordinates=Column(Text)
    
    def __init__(self, host, ip, country,city, coordinates):
        self.host = host
        self.ip = ip
        self.country = country
        self.city=city
        self.coordinates = coordinates
    

    @classmethod
    def get_by_host(cls, host):
        return DBSession.query(cls).filter(cls.host == host).first()

    @classmethod
    def exists(cls, host):
        return DBSession.query(cls).filter(cls.host == host).all()
