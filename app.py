import os
import uvicorn
import spaces
from backend.app import app as fastapi_app

# Top-level ZeroGPU probe registered at startup
@spaces.GPU
def zerogpu_probe():
    """Top-level function registered so Hugging Face ZeroGPU detects GPU availability."""
    return "ZeroGPU registered"

# Force execution at module import time so ZeroGPU registers it during container launch
try:
    zerogpu_probe()
except Exception:
    pass

if __name__ == "__main__":
    port = int(os.getenv("PORT", 7860))
    uvicorn.run(fastapi_app, host="0.0.0.0", port=port)
