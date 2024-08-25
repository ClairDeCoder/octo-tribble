from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, models_schema as schemas, crud_wire as crud, database, auth
from typing import List
import requests

router = APIRouter()

@router.post("/", response_model=schemas.Device, operation_id="add_device")
def add_device(device: schemas.DeviceCreate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    return crud.create_device(db=db, device=device, user_id=current_user.id)


@router.get("/", response_model=List[schemas.Device], operation_id="list_devices")
def list_devices(db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    devices = crud.get_devices(db=db, user_id=current_user.id)
    return devices

@router.put("/{device_id}/version", response_model=schemas.Device, operation_id="update_device_version")
def update_device_version(device_id: int, new_version: str, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    device = crud.update_device_version(db=db, device_id=device_id, new_version=new_version)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

@router.delete("/{device_id}", response_model=schemas.Device, operation_id="delete_device")
def delete_device(device_id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    device = db.query(models.Device).filter(models.Device.id == device_id, models.Device.owner_id == current_user.id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    db.delete(device)
    db.commit()
    return device

@router.get("/{device_id}", response_model=schemas.Device, operation_id="get_device")
def get_device(device_id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    device = db.query(models.Device).filter(models.Device.id == device_id, models.Device.owner_id == current_user.id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

@router.post("/{device_id}/setup", response_model=schemas.Device)
def setup_device(device_id: int, setup_data: schemas.DeviceSetup, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    device = db.query(models.Device).filter(models.Device.id == device_id, models.Device.owner_id == current_user.id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    # Simulate sending the configuration data to the IoT device
    success = True  # Assume the device setup is successful

    if not success:
        raise HTTPException(status_code=500, detail="Failed to configure device")

    # The IoT device will then return relevant operational data, which can be stored in the backend
    # For example, here we are not modifying the device_name, device_type, model, or version, just the `data` field
    device.data = setup_data.data.dict(exclude_unset=True)
    db.commit()
    db.refresh(device)

    return device

@router.put("/{device_id}/data", response_model=schemas.Device)
def update_device_data(device_id: int, data: schemas.DeviceSetupData, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    device = db.query(models.Device).filter(models.Device.id == device_id, models.Device.owner_id == current_user.id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    # Update the device's data field
    device.data = {**device.data, **data.dict(exclude_unset=True)} if device.data else data.dict(exclude_unset=True)
    db.commit()
    db.refresh(device)
    
    return device


