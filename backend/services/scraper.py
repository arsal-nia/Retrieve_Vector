"""
scraper.py
------------------------
Service responsible for scraping and extracting
clean textual content from web pages.

The extracted content can later be embedded
and stored inside the vector database.
"""

import logging
from typing import Dict, Any

import requests
from bs4 import BeautifulSoup


# ==========================================================
# Logging
# ==========================================================

logger = logging.getLogger(__name__)


# ==========================================================
# Configuration
# ==========================================================

REQUEST_TIMEOUT = 15

USER_AGENT = (
    "Mozilla/5.0 "
    "(Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 "
    "(KHTML, like Gecko) "
    "Chrome/120.0 Safari/537.36"
)


# ==========================================================
# Scraper Service
# ==========================================================

class WebScraperService:
    """
    Service for downloading and extracting
    readable text from webpages.
    """

    def __init__(self):

        logger.info(
            "Initializing WebScraperService..."
        )

        self.session = requests.Session()

        self.session.headers.update({

            "User-Agent": USER_AGENT

        })

    # ======================================================
    # Download HTML
    # ======================================================

    def fetch_html(
        self,
        url: str
    ) -> str:
        """
        Download raw HTML from a webpage.
        """

        logger.info(
            f"Downloading webpage: {url}"
        )

        response = self.session.get(

            url,

            timeout=REQUEST_TIMEOUT

        )

        response.raise_for_status()

        return response.text

    # ======================================================
    # Parse HTML
    # ======================================================

    def parse_html(
        self,
        html: str
    ) -> BeautifulSoup:
        """
        Convert raw HTML into
        BeautifulSoup object.
        """

        return BeautifulSoup(

            html,

            "html.parser"

        )
        # ======================================================
    # Extract Page Title
    # ======================================================

    def extract_title(
        self,
        soup: BeautifulSoup
    ) -> str:
        """
        Extract the webpage title.
        """

        if soup.title:

            return soup.title.get_text(strip=True)

        return "Untitled Page"

    # ======================================================
    # Extract Main Text
    # ======================================================

    def extract_text(
        self,
        soup: BeautifulSoup
    ) -> str:
        """
        Remove unwanted HTML elements and
        extract readable text.
        """

        # Remove unwanted tags
        for tag in soup(

            [
                "script",
                "style",
                "header",
                "footer",
                "nav",
                "aside",
                "form",
                "noscript"
            ]

        ):

            tag.decompose()

        text = soup.get_text(separator="\n")

        return self.clean_text(text)

    # ======================================================
    # Clean Extracted Text
    # ======================================================

    def clean_text(
        self,
        text: str
    ) -> str:
        """
        Clean extracted webpage text by removing
        unnecessary blank lines and whitespace.
        """

        lines = []

        for line in text.splitlines():

            line = line.strip()

            if line:

                lines.append(line)

        return "\n".join(lines)

    # ======================================================
    # Scrape Complete Webpage
    # ======================================================

    def scrape_url(
        self,
        url: str
    ) -> Dict[str, Any]:
        """
        Download a webpage and return
        structured information.
        """

        logger.info(
            f"Scraping webpage: {url}"
        )

        try:

            html = self.fetch_html(url)

            soup = self.parse_html(html)

            title = self.extract_title(soup)

            content = self.extract_text(soup)

            logger.info(
                "Webpage scraped successfully."
            )

            return {

                "success": True,

                "url": url,

                "title": title,

                "content": content

            }

        except Exception as error:

            logger.exception(
                f"Failed to scrape webpage: {url}"
            )

            return {

                "success": False,

                "url": url,

                "title": "",

                "content": "",

                "error": str(error)

            }
            # ======================================================
    # Service Information
    # ======================================================

    def service_info(self) -> Dict[str, Any]:
        """
        Return information about the scraper service.
        """

        return {

            "service": "WebScraperService",

            "html_parser": "BeautifulSoup",

            "request_timeout": REQUEST_TIMEOUT,

            "user_agent": USER_AGENT

        }

    # ======================================================
    # Health Check
    # ======================================================

    def health_check(self) -> Dict[str, Any]:
        """
        Verify scraper initialization.
        """

        try:

            return {

                "status": "healthy",

                "session_initialized": self.session is not None,

                "parser": "BeautifulSoup"

            }

        except Exception as error:

            logger.exception(
                "Web scraper health check failed."
            )

            return {

                "status": "unhealthy",

                "error": str(error)

            }

    # ======================================================
    # Scrape and Prepare for RAG
    # ======================================================

    def scrape_for_rag(
        self,
        url: str
    ) -> Dict[str, Any]:
        """
        Scrape a webpage and return data in a format
        suitable for embedding and vector storage.
        """

        result = self.scrape_url(url)

        if not result["success"]:

            return result

        return {

            "success": True,

            "documents": [

                result["content"]

            ],

            "metadata": [

                {

                    "source": url,

                    "title": result["title"],

                    "type": "webpage"

                }

            ]

        }
# ==========================================================
# Global Service Instance
# ==========================================================

web_scraper = WebScraperService()


# ==========================================================
# Module Test
# ==========================================================

if __name__ == "__main__":

    scraper = WebScraperService()

    print("\nService Information")
    print("----------------------------")
    print(scraper.service_info())

    print("\nHealth Check")
    print("----------------------------")
    print(scraper.health_check())

    test_url = "https://en.wikipedia.org/wiki/Brain_tumor"

    print("\nScraping Test")
    print("----------------------------")

    result = scraper.scrape_url(test_url)

    if result["success"]:

        print(f"Title : {result['title']}")

        print()

        print("Content Preview")

        print("----------------------------")

        print(result["content"][:1000])

    else:

        print(result)    