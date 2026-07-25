"use client";

import { useEffect, useState } from "react";
import { apiClient } from "@/lib/api-client";
import UploadBox from "@/components/UploadBox";
import { Conversation } from "@/lib/chat-types";

interface SidebarProps {
    collectionName: string;
    onUploadSuccess: (
        collection: string,
        fileName: string
    ) => void;
    onNewChat: () => void;

    conversations: Conversation[];

    currentConversationId: string;

    onSelectConversation: (id: string) => void;
}
export default function Sidebar({
    collectionName,
    onUploadSuccess,
    onNewChat,
    conversations,
    currentConversationId,
    onSelectConversation,
}: SidebarProps) {
    const [collapsed, setCollapsed] = useState(false);
    
    const [backendStatus, setBackendStatus] = useState("Checking...");
    const [statusTone, setStatusTone] = useState("warning");
const [uploadedFileName, setUploadedFileName] = useState("");
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
        <aside className={`sidebar ${collapsed ? "collapsed" : ""}`}>
            <button
    className="collapse-button"
    onClick={() => setCollapsed(!collapsed)}
>
    ☰
</button>
           

            {/* Logo / Title */}
            <div className="sidebar-header">
                <p className="eyebrow">RAG Assistant</p>
                <h2>Retrieve Vector</h2>
                <p className="sidebar-copy">
                    Chat with your documents
                </p>
            </div>
            

             <button
    className="new-chat-button"
    onClick={onNewChat}
>
    + New Chat
</button>
<div className="conversation-list">

    {conversations.map((conversation) => (

        <button
            key={conversation.id}
            className={
                conversation.id === currentConversationId
                    ? "conversation-item active"
                    : "conversation-item"
            }
            onClick={() =>
                onSelectConversation(conversation.id)
            }
        >
            {conversation.title}
        </button>

    ))}

</div>


            

            {/* Document */}
<div className="sidebar-card">
    <h3>Document</h3>

    {uploadedFileName ? (
        <div className="uploaded-file">

            <p className="file-name">
                {uploadedFileName}
            </p>

            <button
    className="remove-upload"
    onClick={() => {
        setUploadedFileName("");
        onUploadSuccess("", "");
    }}
>
    ×
</button>

        </div>
    ) : (
        <UploadBox
    onUploadSuccess={(collection, fileName) => {
        setUploadedFileName(fileName);
        onUploadSuccess(collection, fileName);
    }}
/>
    )}

</div>
    
            {/* Information */}
           {/* Backend Status */}
            <div className="sidebar-card">
                <h3>System Status</h3>

                <div className="sidebar-row">
                    <span>Backend</span>

                    <span className={`status-pill ${statusTone}`}>
                        {backendStatus}
                    </span>
                </div>
            </div>

        </aside>
    );
}