/**
 * ==========================================================
 * api-client.ts
 * ----------------------------------------------------------
 * Centralized API service for communicating with the
 * FastAPI backend.
 * ==========================================================
 */

const API_BASE_URL =
    process.env.NEXT_PUBLIC_API_URL ||
    "http://localhost:8000";


// ==========================================================
// Interfaces
// ==========================================================

// ==========================================================
// Interfaces
// ==========================================================

export interface UploadResponse {
    success: boolean;
    filename: string;
    collection: string;
    chunks: number;
    message: string;
}


export interface ChatRequest {

    query: string;

    collection_name: string;

}


export interface SourceMetadata {

    source?: string;

    page?: number;

    index?: number;

    [key: string]: any;

}


export interface ChatResponse {

    answer: string;

    context_retrieved: boolean;

    sources: SourceMetadata[];

}


// ==========================================================
// API Client Class
// ==========================================================

class ApiClient {

    /**
     * ---------------------------------------------
     * Upload Document
     * ---------------------------------------------
     */

    async uploadDocument(
        file: File
    ): Promise<UploadResponse> {

        const formData = new FormData();

        formData.append("file", file);

        const response = await fetch(

            `${API_BASE_URL}/documents/upload`,

            {

                method: "POST",

                body: formData

            }

        );

        if (!response.ok) {

            const error = await response.text();

            throw new Error(

                error || "Failed to upload document."

            );

        }

        return await response.json();

    }


    /**
     * ---------------------------------------------
     * Chat Endpoint
     * ---------------------------------------------
     */

    async askQuestion(

        payload: ChatRequest

    ): Promise<ChatResponse> {

        const response = await fetch(

            `${API_BASE_URL}/chat`,

            {

                method: "POST",

                headers: {

                    "Content-Type": "application/json"

                },

                body: JSON.stringify(payload)

            }

        );

        if (!response.ok) {

            const error = await response.text();

            throw new Error(

                error || "Failed to communicate with backend."

            );

        }

        return await response.json();

    }


    /**
     * ---------------------------------------------
     * Backend Health Check
     * ---------------------------------------------
     */

    async healthCheck(): Promise<any> {

        const response = await fetch(

            `${API_BASE_URL}/health`

        );

        if (!response.ok) {

            throw new Error(

                "Backend server is unavailable."

            );

        }

        return await response.json();

    }

}


// ==========================================================
// Export Singleton
// ==========================================================

export const apiClient = new ApiClient();