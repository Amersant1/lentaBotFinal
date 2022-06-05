from email.policy import default
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    Float,
    DateTime,
    Boolean,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    subscribes = relationship("Subscribe", back_populates="user")


class Channel(Base):
    __tablename__ = "channels"
    id = Column(Integer, primary_key=True, autoincrement=True)
    сhannel_name = Column(Text)
    сhannel_title = Column(Text)
    сhannel_id = Column(Integer)
    сhannel_link = Column(Text)
    subscription = Column(Boolean, default=False)
    subs = relationship("Subscribe", back_populates="channel")

    def get_link(self):
        return self.сhannel_link


class Subscribe(Base):
    __tablename__ = "subscribes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    channel_id = Column(Integer, ForeignKey("channels.id"))
    channel = relationship("Channel", back_populates="subs")
    user = relationship("User", back_populates="subscribes")


class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(Text)


class ChannelPopular(Base):
    __tablename__ = "popular_channels"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text)


class Message(Base):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer)
    message_id = Column(Integer)
    text = Column(Text)
    user_id = Column(Integer)


class MediaGroupInfo(Base):
    __tablename__ = "media_group_info"
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer)
    message_id = Column(Integer)
