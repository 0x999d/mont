from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True, nullable=False)
    password = Column(String, nullable=False)
    jwt_token = Column(String, nullable=True)
    refresh_token = Column(String, nullable=True)

    urls = relationship("URL", back_populates="user", cascade="all, delete")

class URL(Base):
    __tablename__ = "urls"

    id = Column(String, nullable=True, primary_key=True)
    interval = Column(Float, nullable=True)
    username = Column(String, ForeignKey("users.username"), nullable=False)

    user = relationship("User", back_populates="urls")