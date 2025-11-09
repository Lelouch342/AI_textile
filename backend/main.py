from fastapi import FastAPI
from controller import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Include routes
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
