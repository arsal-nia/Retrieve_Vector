"""
embeddings.py
------------------------
This module is responsible for generating vector embeddings
for text using the Sentence Transformer model.
"""

import logging
from typing import List
import torch
from sentence_transformers import SentenceTransformer

# Rely on centralized logging configured by main.py
logger = logging.getLogger(__name__)

# Fast and widely used embedding model
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Automatically use GPU if available
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
logger.info(f"Embedding service target hardware device: {DEVICE}")


class EmbeddingService:
    """
    Singleton service for generating embeddings.
    The SentenceTransformer model is loaded only once during application startup.
    """

    _instance = None
    _model = None

    def __new__(cls):
        """Create or return the single instance of EmbeddingService."""
        if cls._instance is None:
            logger.info("Initializing unique EmbeddingService instance...")
            cls._instance = super().__new__(cls)
            logger.info(f"Loading transformer model layer: {MODEL_NAME}")
            cls._model = SentenceTransformer(
                MODEL_NAME,
                device=DEVICE
            )
            logger.info("Embedding model loaded successfully into memory.")
        return cls._instance

    @property
    def model(self) -> SentenceTransformer:
        """Return loaded SentenceTransformer model instance."""
        return self._model

    def embed_query(self, query: str) -> List[float]:
        """Generate an embedding for a single user query string."""
        if not isinstance(query, str):
            raise TypeError("Query must be a string.")

        query = query.strip()
        if len(query) == 0:
            raise ValueError("Query cannot be empty.")

        logger.debug("Generating single query embedding vector...")
        embedding = self.model.encode(
            query,
            convert_to_numpy=True,
            normalize_embeddings=True
        )
        return embedding.tolist()

    def embed_documents(self, documents: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple documents.
        Maintains an identical list index length to prevent vector store insertion mismatches.
        """
        if not isinstance(documents, list):
            raise TypeError("Documents must be provided as a list.")
        if len(documents) == 0:
            raise ValueError("Document list cannot be empty.")

        # Strict validation ensuring data integrity across indices
        for i, doc in enumerate(documents):
            if not isinstance(doc, str):
                raise TypeError(f"Document at index {i} must be a string.")
            if len(doc.strip()) == 0:
                raise ValueError(f"Document at index {i} cannot be empty or pure whitespace.")

        logger.info(f"Generating embeddings for array of {len(documents)} document blocks...")
        embeddings = self.model.encode(
            documents,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False
        )
        return embeddings.tolist()

    def batch_embed(self, documents: List[str], batch_size: int = 32) -> List[List[float]]:
        """Generate embeddings in chunks safely. Optimized for large document volumes."""
        if batch_size <= 0:
            raise ValueError("Batch size must be greater than zero.")

        logger.info(f"Batch embedding ingestion sequence started (Batch Size = {batch_size})")
        embeddings = self.model.encode(
            documents,
            batch_size=batch_size,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False
        )
        logger.info("Batch embedding generation completed successfully.")
        return embeddings.tolist()

    def embedding_dimension(self) -> int:
        """Return the dimension output layout of the model (e.g., 384 for MiniLM)."""
        return self.model.get_sentence_embedding_dimension()

    def model_info(self) -> dict:
        """Return general blueprint info about the loaded model architecture."""
        return {
            "model_name": MODEL_NAME,
            "device": DEVICE,
            "embedding_dimension": self.embedding_dimension()
        }

    def health_check(self) -> dict:
        """Verify engine readiness and matrix operations verification."""
        try:
            test_vector = self.embed_query("health check execution context")
            return {
                "status": "healthy",
                "model_loaded": True,
                "embedding_dimension": len(test_vector),
                "device": DEVICE
            }
        except Exception as error:
            logger.exception("Embedding hardware execution runtime failure.")
            return {
                "status": "unhealthy",
                "model_loaded": False,
                "error": str(error)
            }


# Single exposed instantiation usable globally across routers and services
embedding_service = EmbeddingService()