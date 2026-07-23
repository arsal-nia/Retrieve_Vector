"""
documents.py
------------------------
API endpoints for uploading and indexing documents
into the vector database.
"""

import os
import uuid
import shutil
import logging
from pathlib import Path
from typing import List

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
    status
)

from pydantic import BaseModel

from services.document_parser import document_parser
from services.embeddings import embedding_service
from services.vector_store import VectorStoreService


# ==========================================================
# Logging
# ==========================================================

logger = logging.getLogger(__name__)


# ==========================================================
# Router
# ==========================================================

router = APIRouter()


# ==========================================================
# Configuration
# ==========================================================

UPLOAD_DIRECTORY = "uploads"

os.makedirs(
    UPLOAD_DIRECTORY,
    exist_ok=True
)


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx"
}


# ==========================================================
# Services
# ==========================================================

vector_store = VectorStoreService()


# ==========================================================
# Response Models
# ==========================================================

class UploadResponse(BaseModel):

    success: bool

    filename: str

    collection: str

    chunks: int

    message: str


class ErrorResponse(BaseModel):

    detail: str


# ==========================================================
# Helper Functions
# ==========================================================

def validate_uploaded_file(
    file: UploadFile
) -> None:
    """
    Validate uploaded document.
    """

    if file.filename is None:

        raise HTTPException(

            status_code=status.HTTP_400_BAD_REQUEST,

            detail="Uploaded file has no filename."
        )

    extension = Path(
        file.filename
    ).suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:

        raise HTTPException(

            status_code=status.HTTP_400_BAD_REQUEST,

            detail=(
                f"Unsupported file format '{extension}'. "
                f"Supported formats: {SUPPORTED_EXTENSIONS}"
            )
        )


def save_uploaded_file(
    file: UploadFile
) -> str:
    """
    Save uploaded file
    inside uploads directory.

    Returns
    -------
    Absolute file path.
    """

    extension = Path(
        file.filename
    ).suffix.lower()

    unique_filename = (
        f"{uuid.uuid4().hex}"
        f"{extension}"
    )

    save_path = os.path.join(
        UPLOAD_DIRECTORY,
        unique_filename
    )

    with open(
        save_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    logger.info(
        f"Uploaded file saved at {save_path}"
    )

    return save_path


def extract_collection_name(
    filename: str
) -> str:
    """
    Convert filename into
    collection name.

    Example

    AI.pdf

    becomes

    ai
    """

    return Path(
        filename
    ).stem.lower().replace(
        " ",
        "_"
    )
# ==========================================================
# Upload Document
# ==========================================================

@router.post(
    "/upload",
    response_model=UploadResponse,
    status_code=status.HTTP_201_CREATED
)
async def upload_document(
    file: UploadFile = File(...)
):
    """
    Upload a PDF/DOCX document.

    Current Flow

    Upload File
            │
            ▼
    Validate File
            │
            ▼
    Save File
            │
            ▼
    Parse Document
            │
            ▼
    Create Chunks
            │
            ▼
    Generate Embeddings

    (Vector storage continues in Part 2B)
    """

    logger.info(
        f"Received upload request: {file.filename}"
    )

    # ------------------------------------------------------
    # Validate uploaded file
    # ------------------------------------------------------

    validate_uploaded_file(file)

    # ------------------------------------------------------
    # Save uploaded file
    # ------------------------------------------------------

    saved_path = save_uploaded_file(file)

    logger.info(
        f"Temporary file stored at: {saved_path}"
    )

    try:

        # --------------------------------------------------
        # Collection name
        # --------------------------------------------------

        collection_name = extract_collection_name(
            file.filename
        )

        logger.info(
            f"Target collection: {collection_name}"
        )

        # --------------------------------------------------
        # Parse document
        # --------------------------------------------------

        parsed_chunks = document_parser.parse_and_chunk(
            saved_path
        )

        if len(parsed_chunks) == 0:

            raise HTTPException(

                status_code=status.HTTP_400_BAD_REQUEST,

                detail="No readable text was found in the document."
            )

        logger.info(
            f"{len(parsed_chunks)} chunks extracted."
        )

        # --------------------------------------------------
        # Prepare data
        # --------------------------------------------------

        ids = []

        texts = []

        metadatas = []

        for chunk in parsed_chunks:

            ids.append(
                chunk["id"]
            )

            texts.append(
                chunk["text"]
            )

            metadatas.append(
                chunk["metadata"]
            )

        logger.info(
            "Preparing embeddings..."
        )

        # --------------------------------------------------
        # Generate embeddings
        # --------------------------------------------------

        embeddings = embedding_service.embed_documents(
            texts
        )

        logger.info(
            f"Generated {len(embeddings)} embeddings."
        )

        # --------------------------------------------------
        # Part 2B starts here
        # --------------------------------------------------
                # --------------------------------------------------
        # Store embeddings in ChromaDB
        # --------------------------------------------------

        success = vector_store.upsert_documents(
            collection_name=collection_name,
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas
        )

        if not success:

            raise HTTPException(

                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,

                detail="Failed to store document embeddings in the vector database."
            )

        logger.info(
            f"Successfully indexed '{file.filename}' into collection '{collection_name}'."
        )

        # --------------------------------------------------
        # Remove temporary uploaded file
        # --------------------------------------------------

        try:

            if os.path.exists(saved_path):

                os.remove(saved_path)

                logger.info(
                    f"Temporary file removed: {saved_path}"
                )

        except Exception as cleanup_error:

            logger.warning(
                f"Unable to remove temporary file: {cleanup_error}"
            )

        # --------------------------------------------------
        # Return Success Response
        # --------------------------------------------------

        return UploadResponse(

            success=True,

            filename=file.filename,

            collection=collection_name,

            chunks=len(texts),

            message="Document uploaded, processed, and indexed successfully."
        )

    # ------------------------------------------------------
    # Exception Handling
    # ------------------------------------------------------

    except HTTPException:

        raise

    except Exception as error:

        logger.exception(
            f"Unexpected error while processing '{file.filename}'."
        )

        raise HTTPException(

            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,

            detail=str(error)

        )

    finally:

        # Ensure temporary file is always deleted
        try:

            if os.path.exists(saved_path):

                os.remove(saved_path)

        except Exception:

            pass