from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    f_name = Column(String, index=True)
    l_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Constraint(Base):
    __tablename__ = 'constraints'
    id = Column(Integer, primary_key=True, index=True)
    constraint_json = Column(JSON)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    user = relationship("User", backref="constraints")