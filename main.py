import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import app.models as models
from app.db import engine
from app.routers import user, token, anime

app = FastAPI(title = "ANIME API", description= "")
origins = ["*"] 

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

app.include_router(user.router)
app.include_router(token.router)
app.include_router(anime.router)


@app.on_event("startup")
def configure():    
    models.Base.metadata.create_all(bind=engine)
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8002)