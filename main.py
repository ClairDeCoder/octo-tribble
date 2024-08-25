from fastapi import FastAPI, Depends
from database import engine
from models import Base
from routes import user, device, update
from auth import get_current_user

app = FastAPI()

app.include_router(device.router, prefix="/devices")

# Create the database tables
Base.metadata.create_all(bind=engine)

# Include the routes
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(device.router, prefix="/devices", tags=["Devices"], dependencies=[Depends(get_current_user)])
app.include_router(update.router, prefix="/updates", tags=["Updates"], dependencies=[Depends(get_current_user)])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
