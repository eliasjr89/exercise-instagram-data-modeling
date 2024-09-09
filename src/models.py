import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True)
    user_name =  Column(String(250), nullable=False)
    first_name =  Column(String(250), nullable=False)
    second_name =  Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)

class Comment(Base):
    __tablename__ = "Comment"
    id = Column(Integer, primary_key=True)
    comment_text =  Column(String(250), nullable=False)
    author_id = Column(Integer, ForeignKey("User.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("Post.id"), nullable=False)
    author = relationship("User", foreign_keys=[author_id], back_populates="comments")
    post = relationship("Post", foreign_keys=[post_id], back_populates="comments")

class Post(Base):
    __tablename__ = "Post"
    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    content = Column(String(500), nullable=False)
    user_id = Column(Integer, ForeignKey("User.id"), nullable=False)
    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")

class Media(Base):
    __tablename__ = "Media"
    id = Column(Integer, primary_key=True)
    type = Column(String(250))
    url = Column(String(250))
    post_id = Column(Integer, ForeignKey("Post.id"), nullable=False)
    post = relationship("Post", back_populates="media")

class Follower(Base):
    __tablename__ = "Follower"
    id = Column(Integer, primary_key=True)
    user_from_id = Column(Integer, ForeignKey("User.id"), nullable=False)
    user_to_id = Column(Integer, ForeignKey("User.id"), nullable=False)
    user_from = relationship("User", foreign_keys=[user_from_id], back_populates="followers_from")
    user_to = relationship("User", foreign_keys=[user_to_id], back_populates="followers_to")

    @classmethod
    def follow(cls, session, user_from_id, user_to_id):
        follower = cls(user_from_id=user_from_id, user_to_id=user_to_id)
        session.add(follower)
        session.commit()

    @classmethod
    def unfollow(cls, session, user_from_id, user_to_id):
        session.query(cls).filter_by(user_from_id=user_from_id, user_to_id=user_to_id).delete()
        session.commit()

render_er(Base, "diagram.png")
