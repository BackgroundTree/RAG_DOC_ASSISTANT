"""
API client module for the Yakuza 0 RAG Assistant frontend.

Handles all communication with the backend RAG API.
"""

import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

# Load environment variables from a .env file, if present.
load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Timeout (in seconds) for outgoing requests to the backend.
REQUEST_TIMEOUT_SECONDS = 60


def send_query(question: str) -> Dict[str, Any]:
    """
    Send a user question to the backend RAG API and return a normalized response.

    Args:
        question: The natural-language question submitted by the user.

    Returns:
        A dictionary with the following keys:
            - "answer": str, the generated answer (empty string on failure).
            - "sources": list[str], cited sources (empty list on failure).
            - "error": str | None, a human-friendly error message, or None on success.
    """
    endpoint = f"{API_BASE_URL}/query"

    try:
        response = requests.post(
            endpoint,
            json={"question": question},
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()

        payload = response.json()

        answer = payload.get("answer", "")
        sources = payload.get("sources", []) or []

        if not isinstance(sources, list):
            sources = [str(sources)]

        return {
            "answer": answer,
            "sources": sources,
            "error": None,
        }

    except requests.exceptions.Timeout:
        return {
            "answer": "",
            "sources": [],
            "error": (
                "The request to the Kamurocho archives timed out. "
                "The server may be busy — please try again in a moment."
            ),
        }

    except requests.exceptions.ConnectionError:
        return {
            "answer": "",
            "sources": [],
            "error": (
                f"Could not connect to the backend at {API_BASE_URL}. "
                "Please make sure the API server is running and reachable."
            ),
        }

    except requests.exceptions.HTTPError as http_err:
        status_code = http_err.response.status_code if http_err.response is not None else "unknown"
        return {
            "answer": "",
            "sources": [],
            "error": f"The server returned an error (status code: {status_code}). Please try again later.",
        }

    except requests.exceptions.RequestException as req_err:
        return {
            "answer": "",
            "sources": [],
            "error": f"An unexpected error occurred while contacting the server: {req_err}",
        }

    except ValueError:
        # Raised by response.json() when the response body isn't valid JSON.
        return {
            "answer": "",
            "sources": [],
            "error": "The server returned an unreadable response. Please try again later.",
        }