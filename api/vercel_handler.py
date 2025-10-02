"""
Vercel-specific handler wrapper for FastAPI application.
This file provides the proper ASGI interface for Vercel's Python runtime.
"""

from api.lib.index import app

# Export the FastAPI app as the handler
handler = app