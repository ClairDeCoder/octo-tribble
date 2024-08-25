from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    
    devices = relationship("Device", back_populates="owner")

class Device(Base):
    __tablename__ = "devices"
    
    id = Column(Integer, primary_key=True, index=True)
    device_name = Column(String, index=True)
    device_type = Column(String)
    model = Column(String)
    version = Column(String)
    mode = Column(String)  # Mode is now a top-level field in the model
    data = Column(JSON)  # This will store the device_data part as JSON
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="devices")

class Update(Base):
    __tablename__ = "updates"
    
    id = Column(Integer, primary_key=True, index=True)
    version = Column(String, index=True)
    description = Column(String)
    section = Column(Integer)
    device_type = Column(String, index=True)
    model = Column(String, index=True)
    download_url = Column(String)