"use client";

import { useEffect, useState } from "react";
import { apiClient } from "@/lib/api-client";

interface SidebarProps {
    collectionName: string;
}

export default function Sidebar({ collectionName }: SidebarProps) {
    const [backendStatus, setBackendStatus] = useState("Checking...");
    const [statusTone, setStatusTone] = useState("warning");

    useEffect(() => {
        async function checkBackend() {
            try {
                await apiClient.healthCheck();
                setBackendStatus("Online");
                setStatusTone("success");
            } catch {
                setBackendStatus("Offline");
                setStatusTone("danger");
            }
        }

        checkBackend();
    }, []);

    return (
        <aside className="sidebar">
            <div>
                <p className="eyebrow">RAG Assistant</p>
                <h2>Knowledge Hub</h2>
                <p className="sidebar-copy">
                    A smart workspace for uploading documents and interrogating them with AI.
                </p>
            </div>

            <div className="sidebar-card">
                <div className="sidebar-row">
                    <span>Backend</span>
                    <span className={`status-pill ${statusTone}`}>{backendStatus}</span>
                </div>
            </div>

            <div className="sidebar-card">
                <h3>Active Collection</h3>
                {collectionName ? <p className="mono-text">{collectionName}</p> : <p className="muted">No document uploaded yet.</p>}
            </div>

            <div className="sidebar-card">
                <h3>Capabilities</h3>
                <ul className="feature-list">
                    <li>Document ingestion</li>
                    <li>Semantic retrieval</li>
                    <li>Context-aware chat</li>
                    <li>Source-backed answers</li>
                </ul>
            </div>
        </aside>
    );
}