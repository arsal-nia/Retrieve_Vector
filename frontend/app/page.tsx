"use client";

/**
 * ==========================================================
 * page.tsx
 * ----------------------------------------------------------
 * Main page of the AI RAG Assistant.
 * Coordinates document upload, sidebar, and chat.
 * ==========================================================
 */

import { useState } from "react";
import Sidebar from "@/components/Sidebar";
import UploadBox from "@/components/UploadBox";
import ChatBox from "@/components/ChatBox";

export default function Home() {
    // ======================================================
    // Shared State
    // ======================================================
    // This state acts as the bridge. When UploadBox updates this,
    // ChatBox and Sidebar will automatically update and unlock.
    const [collectionName, setCollectionName] = useState("");

    return (
        <main
            style={{
                display: "flex",
                minHeight: "100vh",
                backgroundColor: "#f3f4f6"
            }}
        >
            {/* ==========================================
                Sidebar
            ========================================== */}
            <Sidebar
                collectionName={collectionName}
            />

            {/* ==========================================
                Main Content
            ========================================== */}
            <div
                style={{
                    flex: 1,
                    padding: "30px"
                }}
            >
                <h1>
                    AI Retrieval-Augmented Generation Assistant
                </h1>

                <p>
                    Upload a document and ask questions about its contents.
                </p>

                <hr />
                <br />

                {/* ==========================================
                    Document Upload
                ========================================== */}
                <UploadBox
                    onUploadSuccess={(collection) => setCollectionName(collection)}
                />

                <br />

                {/* ==========================================
                    Chat Section
                ========================================== */}
                <ChatBox
                    collectionName={collectionName}
                />
            </div>
        </main>
    );
}