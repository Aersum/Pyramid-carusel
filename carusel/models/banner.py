from sqlalchemy import Column, ForeignKey, Integer, Text, SmallInteger, DateTime
from sqlalchemy.orm import relationship
from .meta import Base
from datetime import datetime


class Banner(Base):
    """ The SQLAlchemy declarative model class for a Banner object. """
    __tablename__ = 'banners'
    id = Column(Integer, primary_key=True)
    title_name = Column(Text, nullable=False, unique=True)
    url_link = Column(Text)
    image = Column(Text)
    position = Column(Integer)
    status = Column(SmallInteger, unique=False, default=0)
    created = Column(DateTime)

    creator_id = Column(ForeignKey('users.id'), nullable=False)
    creator = relationship('User', backref='created_banners')

    def set_datetime(self):
        self.created = datetime.now()
