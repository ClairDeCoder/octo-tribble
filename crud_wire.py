from sqlalchemy.orm import Session
import models, models_schema
from auth import get_password_hash

def create_user(db: Session, user: models_schema.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(db_user)
    db.commit()

def create_device(db: Session, device: models_schema.DeviceCreate, user_id: int):
    db_device = models.Device(**device.dict(), owner_id=user_id)
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

def get_devices(db: Session, user_id: int):
    return db.query(models.Device).filter(models.Device.owner_id == user_id).all()


def update_device_version(db: Session, device_id: int, new_version: str):
    device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if device:
        device.version = new_version
        db.commit()
        db.refresh(device)
    return device

def create_update(db: Session, update: models_schema.UpdateCreate):
    db_update = models.Update(**update.dict())
    db.add(db_update)
    db.commit()
    db.refresh(db_update)
    return db_update

def update_device_data(db: Session, device_id: int, user_info: dict, dev_info: dict):
    device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if device:
        # Assuming device.data is a JSON column and is a dictionary
        if device.data is None:
            device.data = {}

        # Update or add the sub-arrays
        device.data['user_info'] = user_info
        device.data['dev_info'] = dev_info

        db.commit()
        db.refresh(device)
    return device