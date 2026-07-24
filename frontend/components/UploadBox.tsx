"use client";

import { useRef, useState } from "react";
import { apiClient } from "@/lib/api-client";

interface UploadBoxProps {
    onUploadSuccess: (collectionName: string) => void;
}

export default function UploadBox({ onUploadSuccess }: UploadBoxProps) {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [uploading, setUploading] = useState(false);
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");
    const [collectionName, setCollectionName] = useState("");
    const fileInputRef = useRef<HTMLInputElement>(null);

    function handleFileChange(event: React.ChangeEvent<HTMLInputElement>) {
        const files = event.target.files;
        if (!files || files.length === 0) {
            setSelectedFile(null);
            return;
        }
        setSelectedFile(files[0]);
        setMessage("");
        setError("");
    }

    async function handleUpload() {
        if (!selectedFile) {
            setError("Please select a document first.");
            return;
        }

        try {
            setUploading(true);
            setError("");
            setMessage("");

            const response = await apiClient.uploadDocument(selectedFile);
            setCollectionName(response.collection);
            setMessage(response.message || "Document uploaded successfully.");
            onUploadSuccess(response.collection);
        } catch (err: any) {
            setError(err.message || "Upload failed.");
        } finally {
            setUploading(false);
        }
    }

    function resetUpload() {
        setSelectedFile(null);
        setCollectionName("");
        setMessage("");
        setError("");

        if (fileInputRef.current) {
            fileInputRef.current.value = "";
        }

        onUploadSuccess("");
    }

    const isUploaded = !!collectionName;

    return (
        <div className="upload-card">
            <div className="card-header">
                <div>
                    <p className="eyebrow">Knowledge Base</p>
                    <h2>Upload a document</h2>
                </div>
                <span className="pill">PDF / DOCX / TXT</span>
            </div>

            <p className="muted">Add a file to build a searchable memory for your assistant.</p>

            <label className="file-picker">
                <input
                    type="file"
                    accept=".pdf,.docx,.txt"
                    onChange={handleFileChange}
                    ref={fileInputRef}
                    disabled={uploading || isUploaded}
                />
                <span>{selectedFile ? `Selected: ${selectedFile.name}` : "Choose a file"}</span>
            </label>

            {selectedFile && (
                <div className="file-meta">
                    <strong>{selectedFile.name}</strong>
                    <span>{(selectedFile.size / 1024).toFixed(2)} KB</span>
                </div>
            )}

            <div className="action-row">
                <button onClick={handleUpload} disabled={uploading || !selectedFile || isUploaded}>
                    {uploading ? "Uploading..." : isUploaded ? "Uploaded" : "Upload"}
                </button>
                <button className="secondary" onClick={resetUpload} disabled={uploading}>
                    Reset
                </button>
            </div>

            {message && <div className="success-box">{message}</div>}
            {error && <div className="error-box">{error}</div>}

            {collectionName && (
                <div className="collection-box">
                    <strong>Collection ready:</strong>
                    <span>{collectionName}</span>
                </div>
            )}
        </div>
    );
}