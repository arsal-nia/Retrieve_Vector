"use client";

import { useRef, useState } from "react";
import { apiClient } from "@/lib/api-client";

interface UploadBoxProps {
  onUploadSuccess: (
    collectionName: string,
    fileName: string
  ) => void;
}

export default function UploadBox({ onUploadSuccess }: UploadBoxProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");
  const [collectionName, setCollectionName] = useState("");
  const fileInputRef = useRef<HTMLInputElement>(null);

  async function handleFileChange(event: React.ChangeEvent<HTMLInputElement>) {
    const files = event.target.files;
    if (!files || files.length === 0) {
      setSelectedFile(null);
      return;
    }
    const file = files[0];
    setSelectedFile(file);
    setError("");

    // Auto-upload upon selection for a smoother UX
    await uploadFile(file);
  }

  async function uploadFile(file: File) {
    try {
      setUploading(true);
      setError("");

      const response = await apiClient.uploadDocument(file);
      setCollectionName(response.collection);
onUploadSuccess(
    response.collection,
    file.name
);
    } catch (err: any) {
      setError(err.message || "Upload failed.");
    } finally {
      setUploading(false);
    }
  }

  function resetUpload() {
    setSelectedFile(null);
    setCollectionName("");
    setError("");

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }

    onUploadSuccess("", "");
  }

  const isUploaded = !!collectionName;

  return (
    <div className="flex flex-col gap-2">
      

      {!isUploaded ? (
  <>
    <input
      type="file"
      accept=".pdf,.docx,.txt"
      onChange={handleFileChange}
      ref={fileInputRef}
      disabled={uploading}
      className="hidden"
    />

    <button
      onClick={() => fileInputRef.current?.click()}
      disabled={uploading}
      className="upload-button"
    >
      {uploading ? "Uploading..." : " Upload Document"}
    </button>
  </>
) : (
        /* Compact File Badge when loaded */
        <div className="flex items-center justify-between p-2.5 bg-indigo-950/40 border border-indigo-500/30 rounded-lg">
          <div className="flex flex-col min-w-0 pr-2">
            <span className="document-file-name">
              📄 {selectedFile?.name || collectionName}
            </span>
            <span className="text-[10px] text-emerald-400 flex items-center gap-1 mt-0.5">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse" />
              Indexed & Ready
            </span>
          </div>
          <button
            onClick={resetUpload}
            title="Remove document"
            className="text-slate-400 hover:text-slate-200 text-xs px-1.5 py-0.5 rounded bg-slate-800 hover:bg-slate-700 transition-colors"
          >
            ✕
          </button>
        </div>
      )}

      {error && (
        <div className="text-[11px] text-rose-400 bg-rose-950/30 border border-rose-800/40 p-2 rounded">
          {error}
        </div>
      )}
    </div>
  );
}