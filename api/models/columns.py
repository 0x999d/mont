from datetime import datetime

from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DateTime,
    Float
)


DB = declarative_base()

class Users(DB):
    __tablename__ = 'users'

    username = Column(String, primary_key=True)
    password = Column(String, nullable=False)

    urls = relationship(
        "TrackedUrls",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True
    )


class TrackedUrls(DB):
    __tablename__ = 'trackedurls'

    id = Column(Integer, primary_key=True, autoincrement=True)  # site id
    interval = Column(Integer, nullable=False)  # seconds
    url = Column(String, nullable=False)  # url

    owner = Column(
        String,
        ForeignKey('users.username', ondelete='CASCADE'),
        nullable=False
    )

    user = relationship("Users", back_populates="urls")

    history = relationship(
        "TrackHistory",
        backref="site",
        cascade="all, delete-orphan",
        passive_deletes=True
    )


class TrackHistory(DB):
    __tablename__ = 'trackhistory'

    id = Column(Integer, primary_key=True, autoincrement=True)
    latency = Column(Float, nullable=True)  # in milliseconds
    http_status = Column(Integer, nullable=True)
    is_ok = Column(Boolean, nullable=False, default=True)  # uptime/downtime
    hash_reqbytes = Column(String, nullable=True)  # request text hash, for detect changes
    date = Column(DateTime, nullable=False, default=datetime.now)
    
    site_id = Column(
        Integer,
        ForeignKey('trackedurls.id', ondelete='CASCADE'),
        nullable=False
    )
