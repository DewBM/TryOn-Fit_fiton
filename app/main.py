from fastapi import FastAPI
from app.routes import user
from app.routes import fiton
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()




# Include the user routes
app.include_router(user.router)
app.include_router(fiton.router)

# Root route
@app.get("/")
def root():
    return {"message": "Welcome to the Image Upload API!"}
