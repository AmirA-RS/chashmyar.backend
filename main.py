from fastapi import FastAPI
from router import user
from Db.Db import engine, Base
app = FastAPI()
Base.metadata.create_all(engine)
app.include_router(user.router)#2