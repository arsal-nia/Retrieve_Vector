"""
chat.py
------------------------
REST API endpoints for interacting with the
Retrieval-Augmented Generation (RAG) engine.
"""

import logging
from typing import List, Dict, Any

from fastapi import (
    APIRouter,
    HTTPException,
    status
)

from pydantic import BaseModel, Field

from services.rag_engine import rag_engine


# ==========================================================
# Logging
# ==========================================================

logger = logging.getLogger(__name__)


# ==========================================================
# Router
# ==========================================================

router = APIRouter()


# ==========================================================
# Request Models
# ==========================================================

class ChatRequest(BaseModel):
    """
    User request for the RAG engine.
    """

    query: str = Field(
        ...,
        min_length=1,
        description="Question asked by the user."
    )

    collection_name: str = Field(
        ...,
        min_length=1,
        description="Target ChromaDB collection."
    )


# ==========================================================
# Response Models
# ==========================================================

class ChatResponse(BaseModel):
    """
    Response returned by the RAG engine.
    """

    answer: str

    sources: List[Dict[str, Any]]

    context_retrieved: bool


# ==========================================================
# Health Endpoint
# ==========================================================

@router.get(
    "/health",
    summary="Health Check"
)
async def health_check():
    """
    Verify that the chat router is active.
    """

    logger.info("Chat router health check requested.")

    return {
        "status": "healthy",
        "service": "chat_router"
    }


# ==========================================================
# Validation Helper
# ==========================================================

def validate_chat_request(
    request: ChatRequest
) -> None:
    """
    Validate incoming chat request.
    """

    if not request.query.strip():

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query cannot be empty."
        )

    if not request.collection_name.strip():

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Collection name cannot be empty."
        )

    logger.info(
        f"Validated request for collection '{request.collection_name}'."
    )
    # ==========================================================
# Chat Endpoint
# ==========================================================

@router.post(
    "/",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Ask a question using RAG"
)
async def chat(
    request: ChatRequest
):
    """
    Main endpoint for interacting with the RAG engine.

    Workflow

    User Question
            │
            ▼
    Validate Request
            │
            ▼
    Retrieve Relevant Context
            │
            ▼
    Generate Answer
            │
            ▼
    Return Response
    """

    logger.info("Received chat request.")

    # ------------------------------------------------------
    # Validate Request
    # ------------------------------------------------------

    validate_chat_request(request)

    try:

        logger.info(
            f"Generating response for collection '{request.collection_name}'."
        )

        # --------------------------------------------------
        # Call RAG Engine
        # --------------------------------------------------

        result = rag_engine.generate_answer(
            query=request.query,
            collection_name=request.collection_name
        )

        logger.info(
            "RAG engine successfully generated a response."
        )

        # --------------------------------------------------
        # Return Response
        # --------------------------------------------------

        return ChatResponse(

            answer=result.get(
                "answer",
                "No answer generated."
            ),

            sources=result.get(
                "sources",
                []
            ),

            context_retrieved=result.get(
                "context_retrieved",
                False
            )
        )

    # ------------------------------------------------------
    # Handle HTTP Exceptions
    # ------------------------------------------------------

    except HTTPException:

        raise

    # ------------------------------------------------------
    # Handle Unexpected Errors
    # ------------------------------------------------------

    except Exception as error:

        logger.exception(
            "Unexpected error while processing chat request."
        )

        raise HTTPException(

            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,

            detail=f"Chat service failed: {str(error)}"

        )
    