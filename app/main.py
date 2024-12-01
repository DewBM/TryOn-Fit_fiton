from fastapi import FastAPI
from app.routes import user

app = FastAPI()

# Include the user routes
app.include_router(user.router)


# Root route
@app.get("/")
def root():
    return {"message": "Welcome to the Image Upload API!"}
