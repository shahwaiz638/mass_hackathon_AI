import os
import logging
import uvicorn
from google.adk.cli.fast_api import get_fast_api_app

# Setup Google Cloud Logging
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

AGENT_DIR = os.path.abspath(os.path.dirname(__file__))

app = get_fast_api_app(
    agents_dir=AGENT_DIR,
    # session_service_uri=session_service_uri,
    allow_origins=["*"],
    web=True,
    trace_to_cloud=True,
)

@app.get("/alive")
async def alive():
    """
    Funtion to check the status of the api
    """
    return {"status": "healthy"}

if __name__ == "__main__":
    # Use the PORT environment variable provided by Cloud Run, defaulting to 8080
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))