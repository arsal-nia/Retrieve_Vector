"""
youtube.py
------------------------
Service responsible for searching YouTube videos
and retrieving transcripts for use in the
Retrieval-Augmented Generation (RAG) pipeline.

Workflow

User Query
      │
      ▼
Search YouTube
      │
      ▼
Select Video
      │
      ▼
Retrieve Transcript
      │
      ▼
Prepare for Embeddings
"""

import logging
from typing import Dict, Any, List

from youtubesearchpython import VideosSearch
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound
)


# ==========================================================
# Logging
# ==========================================================

logger = logging.getLogger(__name__)


# ==========================================================
# Configuration
# ==========================================================

DEFAULT_RESULTS = 5


# ==========================================================
# YouTube Service
# ==========================================================

class YouTubeService:
    """
    Handles YouTube searching and transcript retrieval.
    """

    def __init__(self):

        logger.info(
            "Initializing YouTubeService..."
        )

    # ======================================================
    # Search Videos
    # ======================================================

    def search_videos(
        self,
        query: str,
        limit: int = DEFAULT_RESULTS
    ) -> List[Dict[str, Any]]:
        """
        Search YouTube videos.

        Returns:
            List of video metadata.
        """

        logger.info(
            f"Searching YouTube for '{query}'."
        )

        try:

            search = VideosSearch(

                query,

                limit=limit

            )

            results = search.result()

            videos = []

            for item in results.get("result", []):

                videos.append({

                    "video_id": item.get("id"),

                    "title": item.get("title"),

                    "channel": item.get("channel", {}).get("name"),

                    "duration": item.get("duration"),

                    "published": item.get("publishedTime"),

                    "url": item.get("link")

                })

            logger.info(
                f"Found {len(videos)} videos."
            )

            return videos

        except Exception as error:

            logger.exception(
                "Failed to search YouTube."
            )

            return []
            # ======================================================
    # Get Video Transcript
    # ======================================================

    def get_transcript(
        self,
        video_id: str
    ) -> Dict[str, Any]:
        """
        Retrieve the transcript of a YouTube video.

        Args:
            video_id: YouTube video ID.

        Returns:
            Dictionary containing transcript text.
        """

        logger.info(
            f"Retrieving transcript for video: {video_id}"
        )

        try:

            transcript = YouTubeTranscriptApi.get_transcript(
                video_id
            )

            full_text = " ".join(

                segment["text"]

                for segment in transcript

            )

            logger.info(
                "Transcript retrieved successfully."
            )

            return {

                "success": True,

                "video_id": video_id,

                "transcript": full_text

            }

        except TranscriptsDisabled:

            logger.warning(
                "Transcripts are disabled for this video."
            )

            return {

                "success": False,

                "video_id": video_id,

                "transcript": "",

                "error": "Transcripts are disabled."

            }

        except NoTranscriptFound:

            logger.warning(
                "No transcript available."
            )

            return {

                "success": False,

                "video_id": video_id,

                "transcript": "",

                "error": "No transcript found."

            }

        except Exception as error:

            logger.exception(
                "Failed to retrieve transcript."
            )

            return {

                "success": False,

                "video_id": video_id,

                "transcript": "",

                "error": str(error)

            }

    # ======================================================
    # Prepare Transcript for RAG
    # ======================================================

    def prepare_transcript_for_rag(
        self,
        video_id: str
    ) -> Dict[str, Any]:
        """
        Prepare transcript in a format suitable
        for embeddings and vector storage.
        """

        result = self.get_transcript(video_id)

        if not result["success"]:

            return result

        return {

            "success": True,

            "documents": [

                result["transcript"]

            ],

            "metadata": [

                {

                    "source": "youtube",

                    "video_id": video_id,

                    "type": "youtube_transcript"

                }

            ]

        }
        # ======================================================
    # Service Information
    # ======================================================

    def service_info(self) -> Dict[str, Any]:
        """
        Return information about the YouTube service.
        """

        return {

            "service": "YouTubeService",

            "search_library": "youtube-search-python",

            "transcript_library": "youtube-transcript-api",

            "default_results": DEFAULT_RESULTS

        }

    # ======================================================
    # Health Check
    # ======================================================

    def health_check(self) -> Dict[str, Any]:
        """
        Verify the service has been initialized.
        """

        try:

            return {

                "status": "healthy",

                "search_enabled": True,

                "transcript_enabled": True

            }

        except Exception as error:

            logger.exception(
                "YouTube service health check failed."
            )

            return {

                "status": "unhealthy",

                "error": str(error)

            }

    # ======================================================
    # Search + Transcript Workflow
    # ======================================================

    def search_and_prepare(
        self,
        query: str
    ) -> Dict[str, Any]:
        """
        Search YouTube, retrieve the transcript of the
        first matching video, and prepare it for the
        RAG pipeline.
        """

        videos = self.search_videos(query, limit=1)

        if len(videos) == 0:

            return {

                "success": False,

                "error": "No videos found."

            }

        video = videos[0]

        transcript = self.prepare_transcript_for_rag(

            video["video_id"]

        )

        if not transcript["success"]:

            return transcript

        transcript["video"] = video

        return transcript
# ==========================================================
# Global Service Instance
# ==========================================================

youtube_service = YouTubeService()


# ==========================================================
# Module Test
# ==========================================================

if __name__ == "__main__":

    service = YouTubeService()

    print("\nService Information")
    print("----------------------------")
    print(service.service_info())

    print("\nHealth Check")
    print("----------------------------")
    print(service.health_check())

    query = "Brain Tumor MRI"

    print("\nSearching YouTube...")
    print("----------------------------")

    videos = service.search_videos(query)

    print(f"Videos Found: {len(videos)}")

    if videos:

        first_video = videos[0]

        print()

        print("First Video")

        print("----------------------------")

        print(first_video)

        print()

        print("Downloading Transcript")

        print("----------------------------")

        transcript = service.get_transcript(

            first_video["video_id"]

        )

        if transcript["success"]:

            print(

                transcript["transcript"][:1000]

            )

        else:

            print(

                transcript["error"]

            )