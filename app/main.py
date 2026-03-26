from fastapi import FastAPI
from database import create_tables
import routes

app = FastAPI()

@app.on_event("startup")
def startup():
    create_tables()

app.include_router(routes.router)

@app.get("/")
def root():
    return {"message": "Expense Tracker API is running"}