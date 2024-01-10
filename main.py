from fastapi import FastAPI
from database import  engine
import model
from fastapi.middleware.cors import CORSMiddleware

from routers import admin, users
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin.router)
app.include_router(users.router)        

model.Base.metadata.create_all(bind=engine)

@app.get('/')
async def home():
    return "Hello "