from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn
from routes.RestrictedWordsRoutes import restricted_words_router

app = FastAPI(
    title="Trade Mark Sarthi", description="apis for new paper ", version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def root():
    return {"status": "success", "message": "Server is running!"}


# All Validate Title Routes
app.include_router(restricted_words_router)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
