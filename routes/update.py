from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models_schema, crud_wire, database, auth, models
from typing import List


router = APIRouter()


@router.post("/", response_model=models_schema.Update)
def create_update(update: models_schema.UpdateCreate, db: Session = Depends(database.get_db), current_user: models_schema.User = Depends(auth.get_current_user)):
    db_update = models.Update(
        version=update.version,
        description=update.description,
        section=update.section,
        device_type=update.device_type,
        model=update.model,
        download_url=update.download_url
    )
    db.add(db_update)
    db.commit()
    db.refresh(db_update)
    return db_update



@router.get("/", response_model=List[models_schema.Update])
def get_updates(db: Session = Depends(database.get_db), current_user: models_schema.User = Depends(auth.get_current_user)):
    updates = db.query(models.Update).all()
    return updates

@router.get("/next", response_model=models_schema.Update)
def get_next_update(device_type: str, model: str, db: Session = Depends(database.get_db), current_user: models_schema.User = Depends(auth.get_current_user)):
    # Find the device for the current user
    device = db.query(models.Device).filter(
        models.Device.owner_id == current_user.id,
        models.Device.device_type == device_type,
        models.Device.model == model
    ).first()

    if not device:
        raise HTTPException(status_code=404, detail="Device not found for this user")

    # Check for updates available for this device type and model
    update = db.query(models.Update).filter(
        models.Update.device_type == device_type,
        models.Update.model == model,
        models.Update.version > device.version  # Only return updates newer than current version
    ).first()

    if not update:
        raise HTTPException(status_code=404, detail="No updates available")

    return update




def determine_user_section(user_id: int):
    # Implement logic to determine which section a user belongs to
    # This could be based on the order of registration, a fixed algorithm, or another method
    return 1  # Example, returning section 1 for simplicity
