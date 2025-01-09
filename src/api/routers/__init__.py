"""
Assemble ETL routers
"""

from fastapi import APIRouter

from src.api.routers.ds_routers import ds_router

# Import router
router = APIRouter(prefix="/etl")

# Include routers
router.include_router(ds_router)
