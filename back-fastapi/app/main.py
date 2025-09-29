from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from .services import get_count, increment_count, startup_event

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Add frontend URLs
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup():
    startup_event()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

@app.get("/count")
def read_count():
    count = get_count()
    return {"count": count}

@app.post("/count/increment")
def increment_count_endpoint():
    # Call the database function to increment the count
    new_count = increment_count()
    return {"count": new_count}

# localhost:8000/docs# pour accéder à la doc de l'api