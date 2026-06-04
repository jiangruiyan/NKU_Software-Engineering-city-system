from sqlalchemy import Column, Integer, String, Enum, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum('admin', 'analyst', 'modeler'), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

class Asset(Base):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    type = Column(Enum('plugin', 'model', 'texture'), nullable=False)
    status = Column(Enum('pending', 'approved', 'rejected'), default='pending')
    submitted_by = Column(String(50))
    description = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

class SceneTemplate(Base):
    __tablename__ = "scene_templates"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    template_no = Column(Integer, unique=True, nullable=False)
    tree_count = Column(Integer, default=10)
    road_type = Column(String(50), default='standard')
    seat_count = Column(Integer, default=5)
    description = Column(Text)
    created_by = Column(String(50))
    created_at = Column(DateTime, server_default=func.now())
