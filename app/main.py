from fastapi import FastAPI

from app.qualifications.routes import router as qualifications_router

# Instantiate a FastAPI class.
app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World!"}


@app.get("/health")
def get_app_health():
    return {"status": "ok"}


app.include_router(qualifications_router)
