from sqlalchemy import Column, ForeignKey, Integer, Text, Boolean, Date
from sqlalchemy.orm import relationship
from .meta import Base


class Banner(Base):
    """ The SQLAlchemy declarative model class for a Banner object. """
    __tablename__ = 'banners'
    id = Column(Integer, primary_key=True)
    title_name = Column(Text, nullable=False, unique=True)
    url_link = Column(Text)
    image = Column(Text)
    position = Column(Integer)
    status = Column(Boolean, unique=False, default=False, create_constraint=False)
    created = Column(Date)

    creator_id = Column(ForeignKey('users.id'), nullable=False)
    creator = relationship('User', backref='created_banners')
