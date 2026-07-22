"""
document_parser.py
------------------------
Responsible for reading and extracting text from supported
document formats such as PDF and DOCX.

This module DOES NOT generate embeddings.
It simply extracts clean raw text that will later be
chunked and embedded.
"""

import os
import logging
from pathlib import Path
from typing import List, Dict, Any

import fitz                     # PyMuPDF
from docx import Document


# ==========================================================
# Logging
# ==========================================================

logger = logging.getLogger(__name__)


# ==========================================================
# Supported File Types
# ==========================================================

SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx"
}


# ==========================================================
# Parser Service
# ==========================================================

class DocumentParserService:
    """
    Service responsible for reading documents
    and extracting raw text.

    Supported formats

    • PDF
    • DOCX
    """

    def __init__(self):

        logger.info("Initializing DocumentParserService...")

    # ======================================================
    # Validate File
    # ======================================================

    def validate_file(
        self,
        file_path: str
    ) -> None:
        """
        Validate file before parsing.

        Raises
        ------
        FileNotFoundError
        ValueError
        """

        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"File does not exist: {file_path}"
            )

        extension = Path(file_path).suffix.lower()

        if extension not in SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type: {extension}"
            )

    # ======================================================
    # Parse PDF
    # ======================================================

    def parse_pdf(
        self,
        file_path: str
    ) -> List[Dict[str, Any]]:
        """
        Extract text from every page of a PDF.

        Returns
        -------
        List of page dictionaries.
        """

        logger.info(f"Opening PDF: {file_path}")

        pages = []

        pdf = fitz.open(file_path)

        try:

            total_pages = len(pdf)

            logger.info(
                f"PDF contains {total_pages} pages."
            )

            for page_number in range(total_pages):

                page = pdf.load_page(page_number)

                text = page.get_text("text")

                pages.append(
                    {
                        "page": page_number + 1,
                        "text": text
                    }
                )

            logger.info(
                "PDF parsed successfully."
            )

            return pages

        finally:

            pdf.close()

    # ======================================================
    # Parse DOCX
    # ======================================================

    def parse_docx(
        self,
        file_path: str
    ) -> List[Dict[str, Any]]:
        """
        Extract text from a DOCX document.

        Returns
        -------
        List containing one dictionary.
        """

        logger.info(f"Opening DOCX: {file_path}")

        document = Document(file_path)

        paragraphs = []

        for paragraph in document.paragraphs:

            paragraphs.append(paragraph.text)

        full_text = "\n".join(paragraphs)

        logger.info(
            "DOCX parsed successfully."
        )

        return [
            {
                "page": 1,
                "text": full_text
            }
        ]

    # ======================================================
    # Parse Document
    # ======================================================

    def parse_document(
        self,
        file_path: str
    ) -> List[Dict[str, Any]]:
        """
        Automatically determine the
        document type and parse it.
        """

        self.validate_file(file_path)

        extension = Path(file_path).suffix.lower()

        if extension == ".pdf":

            return self.parse_pdf(file_path)

        elif extension == ".docx":

            return self.parse_docx(file_path)

        raise ValueError(
            "Unsupported document format."
        )


# ==========================================================
# Global Instance
# ==========================================================

document_parser = DocumentParserService()

    # ======================================================
    # Clean Text
    # ======================================================

    def clean_text(
        self,
        text: str
    ) -> str:
        """
        Clean extracted text.

        Removes excessive whitespace,
        blank lines and tabs.
        """

        if not isinstance(text, str):
            raise TypeError("Text must be a string.")

        text = text.replace("\t", " ")

        lines = []

        for line in text.splitlines():

            cleaned = line.strip()

            if cleaned:
                lines.append(cleaned)

        cleaned_text = " ".join(lines)

        while "  " in cleaned_text:
            cleaned_text = cleaned_text.replace("  ", " ")

        return cleaned_text.strip()

    # ======================================================
    # Chunk Text
    # ======================================================

    def chunk_text(
        self,
        text: str,
        chunk_size: int = 800,
        overlap: int = 100
    ) -> List[str]:
        """
        Split text into overlapping chunks.

        Parameters
        ----------
        chunk_size : Maximum characters per chunk

        overlap : Characters repeated between
                  consecutive chunks.
        """

        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive.")

        if overlap >= chunk_size:
            raise ValueError(
                "overlap must be smaller than chunk_size."
            )

        if len(text.strip()) == 0:
            return []

        chunks = []

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            start += chunk_size - overlap

        logger.info(
            f"Generated {len(chunks)} text chunks."
        )

        return chunks

    # ======================================================
    # Create Metadata
    # ======================================================

    def create_metadata(
        self,
        source_file: str,
        page: int,
        chunk_number: int
    ) -> Dict[str, Any]:
        """
        Generate metadata for every chunk.
        """

        return {
            "source": os.path.basename(source_file),
            "page": page,
            "chunk": chunk_number
        }

    # ======================================================
    # Parse and Chunk
    # ======================================================

    def parse_and_chunk(
        self,
        file_path: str,
        chunk_size: int = 800,
        overlap: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Complete preprocessing pipeline.

        File

        ↓

        Extract Text

        ↓

        Clean

        ↓

        Chunk

        ↓

        Metadata
        """

        pages = self.parse_document(file_path)

        all_chunks = []

        chunk_counter = 1

        for page in pages:

            cleaned_text = self.clean_text(
                page["text"]
            )

            chunks = self.chunk_text(
                cleaned_text,
                chunk_size,
                overlap
            )

            for chunk in chunks:

                all_chunks.append(
                    {
                        "id": f"chunk_{chunk_counter}",

                        "text": chunk,

                        "metadata": self.create_metadata(
                            source_file=file_path,
                            page=page["page"],
                            chunk_number=chunk_counter
                        )
                    }
                )

                chunk_counter += 1

        logger.info(
            f"Document processed into {len(all_chunks)} chunks."
        )

        return all_chunks
    # ======================================================
    # Validate Chunks
    # ======================================================

    def validate_chunks(
        self,
        chunks: List[Dict[str, Any]]
    ) -> bool:
        """
        Validate parsed chunks before sending them
        to the embedding service.
        """

        if not isinstance(chunks, list):
            return False

        if len(chunks) == 0:
            return False

        required_keys = {
            "id",
            "text",
            "metadata"
        }

        for chunk in chunks:

            if not isinstance(chunk, dict):
                return False

            if not required_keys.issubset(chunk.keys()):
                return False

            if len(chunk["text"].strip()) == 0:
                return False

        return True

    # ======================================================
    # Document Statistics
    # ======================================================

    def document_statistics(
        self,
        chunks: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Return useful statistics
        for a parsed document.
        """

        if not self.validate_chunks(chunks):

            raise ValueError(
                "Invalid chunk structure."
            )

        total_characters = sum(
            len(chunk["text"])
            for chunk in chunks
        )

        average_chunk_size = (
            total_characters / len(chunks)
        )

        return {

            "total_chunks": len(chunks),

            "total_characters": total_characters,

            "average_chunk_size": round(
                average_chunk_size,
                2
            )
        }

    # ======================================================
    # Parser Information
    # ======================================================

    def parser_info(self) -> Dict[str, Any]:
        """
        Return parser information.
        """

        return {

            "supported_formats": list(
                SUPPORTED_EXTENSIONS
            ),

            "parser": "DocumentParserService",

            "pdf_engine": "PyMuPDF",

            "docx_engine": "python-docx"
        }

    # ======================================================
    # Health Check
    # ======================================================

    def health_check(self) -> Dict[str, Any]:
        """
        Verify parser availability.
        """

        try:

            return {

                "status": "healthy",

                "supported_formats": list(
                    SUPPORTED_EXTENSIONS
                )
            }

        except Exception as error:

            logger.exception(
                "Document parser health check failed."
            )

            return {

                "status": "unhealthy",

                "error": str(error)
            }
        
# ==========================================================
# Global Instance
# ==========================================================

document_parser = DocumentParserService()


# ==========================================================
# Module Test
# ==========================================================

if __name__ == "__main__":

    parser = DocumentParserService()

    print("\nParser Information")
    print("----------------------------")
    print(parser.parser_info())

    print("\nHealth Check")
    print("----------------------------")
    print(parser.health_check())

    sample_file = "sample.pdf"

    if os.path.exists(sample_file):

        chunks = parser.parse_and_chunk(sample_file)

        print()

        print("Chunks Created :", len(chunks))

        print()

        print(parser.document_statistics(chunks))

        print()

        print("First Chunk")

        print("----------------------------")

        print(chunks[0]["text"][:500])

    else:

        print()

        print(
            f"Place '{sample_file}' in this directory "
            "to test the parser."
        )        
