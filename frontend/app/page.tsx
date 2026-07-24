"use client";

import { useState } from "react";
import Sidebar from "@/components/Sidebar";
import UploadBox from "@/components/UploadBox";
import ChatBox from "@/components/ChatBox";

export default function Home() {
    const [collectionName, setCollectionName] = useState("");

    return (
        <main className="app-shell">
            <Sidebar collectionName={collectionName} />

            <section className="main-panel">
                <div className="hero-card">
                    <div>
                        <p className="eyebrow">AI Knowledge Workspace</p>
                        <h1>Ask anything from your documents in a conversational experience.</h1>
                        <p className="hero-copy">
                            Upload a PDF, DOCX, or TXT file and chat naturally with your own knowledge base.
                        </p>
                    </div>

                    <div className="hero-badges">
                        <span>⚡ Instant RAG answers</span>
                        <span>🧠 Context-aware chat</span>
                        <span>📚 Source-backed responses</span>
                    </div>
                </div>

                <UploadBox onUploadSuccess={(collection) => setCollectionName(collection)} />
                <ChatBox collectionName={collectionName} />
            </section>
        </main>
    );
}