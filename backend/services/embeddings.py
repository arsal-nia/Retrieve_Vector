"""
embeddings.py
------------------------

This module is responsible for generating vector embeddings
for text using the Sentence Transformer model.

Responsibilities
----------------
1. Load embedding model only once.
2. Generate embeddings for queries.
3. Generate embeddings for documents.
4. Support batch embedding generation.
5. Provide helper methods for RAG Engine.

Used By
-------
rag_engine.py
vector_store.py
document_parser.py
"""

# ============================================================
# Imports
# ============================================================

import logging
from typing import List

import torch
from sentence_transformers import SentenceTransformer

# ============================================================
# Logging Configuration
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# ============================================================
# Model Configuration
# ============================================================

# Small, fast and widely used embedding model
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Automatically use GPU if available
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

logger.info(f"Embedding device selected: {DEVICE}")

# ============================================================
# Embedding Service
# ============================================================


class EmbeddingService:
    """
    Singleton service for generating embeddings.

    The SentenceTransformer model is loaded only once
    during application startup.

    Other modules will import this class and use its
    methods instead of loading the model again.
    """

    _instance = None
    _model = None

    def __new__(cls):
        """
        Create only one instance of EmbeddingService.
        """

        if cls._instance is None:
            logger.info("Creating EmbeddingService instance...")

            cls._instance = super().__new__(cls)

            logger.info("Loading embedding model...")

            cls._model = SentenceTransformer(
                MODEL_NAME,
                device=DEVICE
            )

            logger.info("Embedding model loaded successfully.")

        return cls._instance

    @property
    def model(self):
        """
        Return loaded SentenceTransformer model.
        """

        return self._model


# ============================================================
# Create Global Instance
# ============================================================

embedding_service = EmbeddingService()
    # ============================================================
    # Generate Embedding for a Single Query
    # ============================================================

    def embed_query(self, query: str) -> List[float]:
        """
        Generate an embedding for a single query.

        Parameters
        ----------
        query : str
            User's question or search query.

        Returns
        -------
        List[float]
            Vector representation of the query.
        """

        if not isinstance(query, str):
            raise TypeError("Query must be a string.")

        query = query.strip()

        if len(query) == 0:
            raise ValueError("Query cannot be empty.")

        logger.info("Generating query embedding...")

        embedding = self.model.encode(
            query,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        logger.info("Query embedding generated successfully.")

        return embedding.tolist()

    # ============================================================
    # Generate Embeddings for Multiple Documents
    # ============================================================

    def embed_documents(
        self,
        documents: List[str]
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple documents.

        Parameters
        ----------
        documents : List[str]

        Returns
        -------
        List[List[float]]
        """

        if not isinstance(documents, list):
            raise TypeError("Documents must be provided as a list.")

        if len(documents) == 0:
            raise ValueError("Document list cannot be empty.")

        cleaned_documents = []

        for document in documents:

            if not isinstance(document, str):
                raise TypeError(
                    "Each document must be a string."
                )

            document = document.strip()

            if len(document) == 0:
                continue

            cleaned_documents.append(document)

        if len(cleaned_documents) == 0:
            raise ValueError(
                "No valid documents found."
            )

        logger.info(
            f"Generating embeddings for "
            f"{len(cleaned_documents)} documents..."
        )

        embeddings = self.model.encode(
            cleaned_documents,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False
        )

        logger.info("Document embeddings generated.")

        return embeddings.tolist()

    # ============================================================
    # Batch Embedding Generator
    # ============================================================

    def batch_embed(
        self,
        documents: List[str],
        batch_size: int = 32
    ) -> List[List[float]]:
        """
        Generate embeddings in batches.

        Useful for large PDF collections.

        Parameters
        ----------
        documents : List[str]

        batch_size : int

        Returns
        -------
        List[List[float]]
        """

        if batch_size <= 0:
            raise ValueError(
                "Batch size must be greater than zero."
            )

        logger.info(
            f"Batch embedding started "
            f"(Batch Size = {batch_size})"
        )

        embeddings = self.model.encode(
            documents,
            batch_size=batch_size,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=True
        )

        logger.info("Batch embedding completed.")

        return embeddings.tolist()

    # ============================================================
    # Embedding Dimension
    # ============================================================

    def embedding_dimension(self) -> int:
        """
        Return the dimension of the embedding model.

        Returns
        -------
        int
        """

        return self.model.get_sentence_embedding_dimension()

    # ============================================================
    # Model Information
    # ============================================================

    def model_info(self) -> dict:
        """
        Return information about
        the loaded embedding model.
        """

        return {
            "model_name": MODEL_NAME,
            "device": DEVICE,
            "embedding_dimension":
                self.embedding_dimension()
        }
    # ============================================================
    # Validate Embedding
    # ============================================================

    def validate_embedding(self, embedding: List[float]) -> bool:
        """
        Validate that an embedding has the correct dimension.

        Parameters
        ----------
        embedding : List[float]

        Returns
        -------
        bool
        """

        if not isinstance(embedding, list):
            return False

        return len(embedding) == self.embedding_dimension()

    # ============================================================
    # Validate Multiple Embeddings
    # ============================================================

    def validate_embeddings(
        self,
        embeddings: List[List[float]]
    ) -> bool:
        """
        Validate a list of embeddings.

        Parameters
        ----------
        embeddings : List[List[float]]

        Returns
        -------
        bool
        """

        if not isinstance(embeddings, list):
            return False

        return all(
            self.validate_embedding(vector)
            for vector in embeddings
        )

    # ============================================================
    # Get Device
    # ============================================================

    def get_device(self) -> str:
        """
        Return the device currently
        being used by the embedding model.
        """

        return DEVICE

    # ============================================================
    # Get Model Name
    # ============================================================

    def get_model_name(self) -> str:
        """
        Return embedding model name.
        """

        return MODEL_NAME

    # ============================================================
    # Health Check
    # ============================================================

    def health_check(self) -> dict:
        """
        Verify that the embedding model
        is loaded and operational.
        """

        try:

            test_embedding = self.embed_query("health check")

            return {
                "status": "healthy",
                "model_loaded": True,
                "embedding_dimension": len(test_embedding),
                "device": DEVICE
            }

        except Exception as error:

            logger.exception("Embedding health check failed.")

            return {
                "status": "unhealthy",
                "model_loaded": False,
                "error": str(error)
            }


