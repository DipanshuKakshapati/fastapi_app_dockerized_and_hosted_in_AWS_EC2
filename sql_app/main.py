"""
This module initializes a FastAPI application and includes routing configurations.

It imports and registers routers from the routes.date module, setting up endpoints for
date-related data operations. The FastAPI app is configured to run with Uvicorn as the ASGI server,
listening on all network interfaces at port 8000.

To run this module directly:
    - Use the command: python -m sql_app.main (without the `.py` extension)
    - Make sure you are in the environment where FastAPI and Uvicorn are installed.
    - The server will be accessible via: http://0.0.0.0:8000

Example:
    To add another router:
    from routes.another_module import router as another_router
    app.include_router(another_router)
"""

from fastapi import FastAPI
import uvicorn
from sql_app.route import router as date_router

app = FastAPI()

# including the router in the FastAPI app from the routes.date
app.include_router(date_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    print("Server running at http://0.0.0.0:8000")


