"""
Main entry point for Vercel deployment.
This module imports and exposes the FastAPI app from the backend.
"""
from backend.main import app

# Expose the app for Vercel
__all__ = ["app"]
