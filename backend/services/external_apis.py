"""
external_apis.py
------------------------
Service responsible for retrieving information from
external knowledge sources such as Wikipedia,
PubMed, and arXiv.

These APIs are used as a fallback whenever the
local vector database cannot answer a query.
"""

import logging
from typing import Dict, Any, List, Optional

import requests


# ==========================================================
# Logging
# ==========================================================

logger = logging.getLogger(__name__)


# ==========================================================
# Configuration
# ==========================================================

WIKIPEDIA_API = (
    "https://en.wikipedia.org/api/rest_v1/page/summary/"
)

PUBMED_API = (
    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
)

ARXIV_API = (
    "http://export.arxiv.org/api/query"
)

REQUEST_TIMEOUT = 15


# ==========================================================
# External API Service
# ==========================================================

class ExternalAPIService:
    """
    Handles communication with external
    information providers.

    Current providers

    • Wikipedia
    • PubMed
    • arXiv
    """

    def __init__(self):

        logger.info(
            "Initializing ExternalAPIService..."
        )

        self.session = requests.Session()

        self.session.headers.update({

            "User-Agent":
            "RetrieveVector/1.0"

        })

    # ======================================================
    # Generic GET Request
    # ======================================================

    def _get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        """
        Execute a GET request with
        centralized error handling.
        """

        response = self.session.get(

            url,

            params=params,

            timeout=REQUEST_TIMEOUT

        )

        response.raise_for_status()

        return response
        # ======================================================
    # Wikipedia Search
    # ======================================================

    def search_wikipedia(
        self,
        query: str
    ) -> Dict[str, Any]:
        """
        Retrieve a summary from Wikipedia.
        """

        logger.info(
            f"Searching Wikipedia for '{query}'."
        )

        try:

            response = self._get(
                WIKIPEDIA_API + query.replace(" ", "_")
            )

            data = response.json()

            return {

                "success": True,

                "source": "Wikipedia",

                "title": data.get("title", ""),

                "content": data.get("extract", ""),

                "url": data.get(
                    "content_urls",
                    {}
                ).get(
                    "desktop",
                    {}
                ).get(
                    "page",
                    ""
                )

            }

        except Exception as error:

            logger.error(
                f"Wikipedia search failed: {error}"
            )

            return {

                "success": False,

                "source": "Wikipedia",

                "content": "",

                "error": str(error)
            }

    # ======================================================
    # PubMed Search
    # ======================================================

    def search_pubmed(
        self,
        query: str,
        max_results: int = 5
    ) -> Dict[str, Any]:
        """
        Search PubMed article IDs.
        """

        logger.info(
            f"Searching PubMed for '{query}'."
        )

        try:

            response = self._get(

                PUBMED_API,

                params={

                    "db": "pubmed",

                    "term": query,

                    "retmode": "json",

                    "retmax": max_results

                }

            )

            data = response.json()

            article_ids = data.get(

                "esearchresult",

                {}

            ).get(

                "idlist",

                []

            )

            return {

                "success": True,

                "source": "PubMed",

                "article_ids": article_ids,

                "count": len(article_ids)

            }

        except Exception as error:

            logger.error(
                f"PubMed search failed: {error}"
            )

            return {

                "success": False,

                "source": "PubMed",

                "article_ids": [],

                "error": str(error)

            }

    # ======================================================
    # arXiv Search
    # ======================================================

    def search_arxiv(
        self,
        query: str,
        max_results: int = 5
    ) -> Dict[str, Any]:
        """
        Search arXiv research papers.
        """

        logger.info(
            f"Searching arXiv for '{query}'."
        )

        try:

            response = self._get(

                ARXIV_API,

                params={

                    "search_query": query,

                    "start": 0,

                    "max_results": max_results

                }

            )

            return {

                "success": True,

                "source": "arXiv",

                "raw_xml": response.text

            }

        except Exception as error:

            logger.error(
                f"arXiv search failed: {error}"
            )

            return {

                "success": False,

                "source": "arXiv",

                "raw_xml": "",

                "error": str(error)

            }
            # ======================================================
    # Search All Sources
    # ======================================================

    def search_all_sources(
        self,
        query: str
    ) -> Dict[str, Any]:
        """
        Search all supported external sources.

        Returns a unified response that can later
        be used by the RAG engine as a fallback.
        """

        logger.info(
            f"Searching all external sources for '{query}'."
        )

        return {

            "wikipedia": self.search_wikipedia(query),

            "pubmed": self.search_pubmed(query),

            "arxiv": self.search_arxiv(query)

        }

    # ======================================================
    # Service Information
    # ======================================================

    def service_info(self) -> Dict[str, Any]:
        """
        Return information about
        the configured external services.
        """

        return {

            "service": "ExternalAPIService",

            "providers": [

                "Wikipedia",

                "PubMed",

                "arXiv"

            ],

            "timeout_seconds": REQUEST_TIMEOUT

        }

    # ======================================================
    # Health Check
    # ======================================================

    def health_check(self) -> Dict[str, Any]:
        """
        Verify the service is initialized.

        This does not make external requests;
        it only checks that the HTTP session
        has been created successfully.
        """

        try:

            return {

                "status": "healthy",

                "providers": [

                    "Wikipedia",

                    "PubMed",

                    "arXiv"

                ]

            }

        except Exception as error:

            logger.exception(
                "External API service health check failed."
            )

            return {

                "status": "unhealthy",

                "error": str(error)

            }
# ==========================================================
# Global Service Instance
# ==========================================================

external_api_service = ExternalAPIService()


# ==========================================================
# Module Test
# ==========================================================

if __name__ == "__main__":

    service = ExternalAPIService()

    print("\nService Information")
    print("----------------------------")
    print(service.service_info())

    print("\nHealth Check")
    print("----------------------------")
    print(service.health_check())

    print("\nWikipedia Test")
    print("----------------------------")

    wikipedia_result = service.search_wikipedia(
        "Brain Tumor"
    )

    print(wikipedia_result)

    print("\nPubMed Test")
    print("----------------------------")

    pubmed_result = service.search_pubmed(
        "Brain Tumor"
    )

    print(pubmed_result)

    print("\narXiv Test")
    print("----------------------------")

    arxiv_result = service.search_arxiv(
        "Brain Tumor"
    )

    print(arxiv_result)