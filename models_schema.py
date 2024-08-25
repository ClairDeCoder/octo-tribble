from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class DeviceBase(BaseModel):
    device_name: str
    device_type: str
    model: str
    version: str
    data: Optional[Dict] = None
    #data: Dict

    class Config:
        from_attributes = True

class DeviceCreate(BaseModel):
    device_name: str
    device_type: str
    model: str
    version: str

    class Config:
        from_attributes = True

class Device(DeviceBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

class DeviceSetupData(BaseModel):
    user_info: Dict

    class Config:
        from_attributes = True

class DeviceSetup(BaseModel):
    data: DeviceSetupData

    class Config:
        from_attributes = True


class UpdateBase(BaseModel):
    version: str
    description: Optional[str] = None
    section: int
    device_type: str
    model: str
    download_url: str

class UpdateCreate(UpdateBase):
    pass

class Update(BaseModel):
    id: int
    version: str
    description: Optional[str] = None
    section: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = None
