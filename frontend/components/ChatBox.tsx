"use client";

import { useState, type FormEvent, type KeyboardEvent } from "react";
import { apiClient, type SourceMetadata } from "@/lib/api-client";
import Message from "./Message";
import { ChatMessage } from "@/lib/chat-types";

interface ChatBoxProps {
    collectionName: string;
    messages: ChatMessage[];
    setMessages: React.Dispatch<React.SetStateAction<ChatMessage[]>>;
}



interface ChatStatusInfo {
    contextRetrieved: boolean;
    collectionName: string;
}

export default function ChatBox({
    collectionName,
    messages,
    setMessages,
}: ChatBoxProps) {
    const [question, setQuestion] = useState("");
    
    const [sources, setSources] = useState<SourceMetadata[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [chatStatus, setChatStatus] = useState<ChatStatusInfo>({
        contextRetrieved: false,
        collectionName: collectionName,
    });

    const suggestedPrompts = [
        "Summarize the most important points",
        "What are the key takeaways?",
        "Find the most relevant section",
    ];

    async function askQuestion(event?: FormEvent) {
        event?.preventDefault();

        if (!question.trim()) {
            setError("Please enter a question.");
            return;
        }

        if (!collectionName) {
            setError("Please upload a document first.");
            return;
        }

        setError("");
        const userMessage: ChatMessage = {
            role: "user",
            content: question,
        };

        setMessages((previous) => [...previous, userMessage]);
        const currentQuestion = question;
        setQuestion("");

        try {
            setLoading(true);
            const response = await apiClient.askQuestion({
                query: currentQuestion,
                collection_name: collectionName,
            });

            const assistantMessage: ChatMessage = {
                role: "assistant",
                content: response.answer,
            };

            setMessages((previous) => [...previous, assistantMessage]);
            setSources(response.sources || []);
            setChatStatus({
                contextRetrieved: response.context_retrieved,
                collectionName,
            });
        } catch (err: any) {
            setError(err.message || "Unable to contact the backend.");
        } finally {
            setLoading(false);
        }
    }

    function handleKeyDown(event: KeyboardEvent<HTMLTextAreaElement>) {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            void askQuestion();
        }
    }

    return (
    <div className="chat-card">

        <div className="card-header">

    <div className="chat-header">

        <div className="chat-avatar">
            🤖
        </div>

        <div>

            <h2>Retrieve Vector</h2>

            <p className="muted">
                AI Assistant for your documents
            </p>

        </div>

    </div>

    {collectionName && (

        <div className="status-pill success">

            Connected

        </div>

    )}

</div>

        {!collectionName && (
            <div className="warning-box">
                Upload a document to begin chatting.
            </div>
        )}

        {/* Messages */}
        <div className="chat-window">

            {messages.length === 0 ? (
                <div className="empty-state">

    <div className="empty-icon">
        
    </div>

    <h2>
        How can I help you today?
    </h2>

    <p>
        Upload a document and start chatting with your AI assistant.
    </p>

</div>
            ) : (
                messages.map((message, index) => (
                    <Message
                        key={`${message.role}-${index}`}
                        role={message.role}
                        content={message.content}
                    />
                ))
            )}

            {loading && (
                <div className="typing-indicator">
                    <span />
                    <span />
                    <span />
                </div>
            )}

        </div>

       
        

        {/* Composer */}

        <form
            onSubmit={askQuestion}
            className="composer"
        >

            <div className="composer-shell">

                <textarea
                    value={question}
                    onChange={(event) =>
                        setQuestion(event.target.value)
                    }
                    onKeyDown={handleKeyDown}
                    placeholder={
    loading
        ? "Thinking..."
        : collectionName
            ? "Message Retrieve Vector..."
            : "Upload a document first..."
}
                    disabled={!collectionName || loading}
                    rows={2}
                />

                <button
    type="submit"
    disabled={!collectionName || loading}
>
    ➤
</button>

            </div>

            <div className="prompt-row">

                {suggestedPrompts.map((prompt) => (
                    <button
                        key={prompt}
                        type="button"
                        className="prompt-chip"
                        onClick={() => setQuestion(prompt)}
                        disabled={!collectionName || loading}
                    >
                        {prompt}
                    </button>
                ))}

            </div>

        </form>

        {error && (
            <div className="error-box">
                {error}
            </div>
        )}

    </div>
);
}