"use client";

/**
 * ==========================================================
 * UploadBox.tsx
 * ----------------------------------------------------------
 * Component responsible for uploading documents to the
 * FastAPI backend.
 * ==========================================================
 */

import { useState } from "react";
import { apiClient } from "@/lib/api-client";

interface UploadBoxProps {
    onUploadSuccess: (collectionName: string) => void;
}

export default function UploadBox({
    onUploadSuccess,
}: UploadBoxProps) {

    const [selectedFile, setSelectedFile] = useState<File | null>(null);

    const [uploading, setUploading] = useState(false);

    const [message, setMessage] = useState("");

    const [error, setError] = useState("");

    const [collectionName, setCollectionName] = useState("");

    // ======================================================
    // File Selection
    // ======================================================

    function handleFileChange(
        event: React.ChangeEvent<HTMLInputElement>
    ) {

        const files = event.target.files;

        if (!files || files.length === 0) {

            setSelectedFile(null);

            return;

        }

        setSelectedFile(files[0]);

        setMessage("");

        setError("");

    }

    // ======================================================
    // Upload Document
    // ======================================================

    async function handleUpload() {

        if (!selectedFile) {

            setError("Please select a document.");

            return;

        }

        try {

            setUploading(true);

            setError("");

            setMessage("");

            const response = await apiClient.uploadDocument(
                selectedFile
            );

            setCollectionName(
                response.collection_name
            );

            setMessage(
                response.message
            );

            onUploadSuccess(
                response.collection_name
            );

        }

        catch (err: any) {

            setError(
                err.message || "Upload failed."
            );

        }

        finally {

            setUploading(false);

        }

    }

    // ======================================================
    // Reset
    // ======================================================

    function resetUpload() {

        setSelectedFile(null);

        setCollectionName("");

        setMessage("");

        setError("");

    }

    // ======================================================
    // UI
    // ======================================================

    return (

        <div
            style={{
                border: "1px solid #ddd",
                padding: "20px",
                borderRadius: "10px",
                marginBottom: "20px",
            }}
        >

            <h2>Upload Document</h2>

            <p>
                Supported formats:
                PDF, DOCX and TXT
            </p>

            <input
                type="file"
                accept=".pdf,.docx,.txt"
                onChange={handleFileChange}
            />

            <br />
            <br />

            {selectedFile && (

                <div>

                    <strong>Selected File:</strong>

                    <br />

                    {selectedFile.name}

                    <br />

                    {(selectedFile.size / 1024).toFixed(2)} KB

                </div>

            )}

            <br />

            <button

                onClick={handleUpload}

                disabled={
                    uploading || !selectedFile
                }

            >

                {

                    uploading

                        ? "Uploading..."

                        : "Upload"

                }

            </button>

            <button

                onClick={resetUpload}

                style={{ marginLeft: "10px" }}

                disabled={uploading}

            >

                Reset

            </button>

            {message && (

                <div
                    style={{
                        marginTop: "20px",
                        color: "green",
                    }}
                >

                    <strong>Success</strong>

                    <br />

                    {message}

                </div>

            )}

            {error && (

                <div
                    style={{
                        marginTop: "20px",
                        color: "red",
                    }}
                >

                    <strong>Error</strong>

                    <br />

                    {error}

                </div>

            )}

            {collectionName && (

                <div
                    style={{
                        marginTop: "20px",
                        backgroundColor: "#f3f4f6",
                        padding: "10px",
                        borderRadius: "6px",
                    }}
                >

                    <strong>Collection:</strong>

                    <br />

                    {collectionName}

                </div>

            )}

        </div>

    );

}