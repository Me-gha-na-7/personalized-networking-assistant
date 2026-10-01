import os
import uvicorn
from backend.app import app as fastapi_app

if __name__ == "__main__":
    # Hugging Face Spaces provides PORT env variable (default 7860)
    port = int(os.getenv("PORT", 7860))
    uvicorn.run(fastapi_app, host="0.0.0.0", port=port)