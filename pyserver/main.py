import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute

from pyserver.api.auth.routes import router as auth_router
from pyserver.api.folders import router as folders_router
from pyserver.api.node import router as node_router
from pyserver.api.node.update import router as node_update_router
from pyserver.api.schema import router as schema_router
from pyserver.api.schema.type_properties import router as type_properties_router

from pyserver.api.dependencies import get_storage_context  # ✅ this gets user_id from JWT

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="URLife API")

@app.on_event("startup")
async def print_routes():
    logger.info("📋 Registered Routes:")
    for route in app.routes:
        if isinstance(route, APIRoute):
            methods = ','.join(route.methods)
            logger.info(f"{methods:10s} {route.path}")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(folders_router, prefix="/api", tags=["folders"])
app.include_router(node_router, prefix="/api/node", tags=["node"])
app.include_router(node_update_router, prefix="/api/node/update", tags=["node-update"])
app.include_router(schema_router, prefix="/api/schema", tags=["schema"])
app.include_router(type_properties_router, prefix="/api", tags=["type_properties"])
