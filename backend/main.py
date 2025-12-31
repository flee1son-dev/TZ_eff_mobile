from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.core.database import engine, Base
from backend.modules.auth.routers import router as auth_routers
from backend.modules.users.routers import router as users_routers
from backend.modules.tasks.routers import router as tasks_routers


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials=True,
    allow_methods=["PUT","GET","DELETE","POST"],
    allow_headers=["Authorization", "Content-Type"]
)

app.include_router(auth_routers)
app.include_router(users_routers)
app.include_router(tasks_routers)

Base.metadata.create_all(engine)

@app.get("ping")
def ping():
    return {"status": "ok"}
