"use client";

import { useState, type FormEvent, type KeyboardEvent } from "react";
import { apiClient, type SourceMetadata } from "@/lib/api-client";
import Message from "./Message";

interface ChatBoxProps {
    collectionName: string;
}

interface ChatMessage {
    role: "user" | "assistant";
    content: string;
}

interface ChatStatusInfo {
    contextRetrieved: boolean;
    collectionName: string;
}

export default function ChatBox({ collectionName }: ChatBoxProps) {
    const [question, setQuestion] = useState("");
    const [messages, setMessages] = useState<ChatMessage[]>([]);
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
                <div>
                    <p className="eyebrow">Conversation</p>
                    <h2>Ask your document anything</h2>
                </div>
                <span className="pill">Live chat</span>
            </div>

            {!collectionName && <div className="warning-box">Upload a document to unlock the chat experience.</div>}

            {collectionName && (
                <div className="warning-box">
                    Active collection: <strong>{chatStatus.collectionName}</strong> · Context retrieved: <strong>{chatStatus.contextRetrieved ? "Yes" : "No"}</strong>
                </div>
            )}

            <div className="chat-window">
                {messages.length === 0 ? (
                    <div className="empty-state">
                        <h3>Start a new conversation</h3>
                        <p>Use the prompt suggestions below or ask a specific question about your uploaded content.</p>
                    </div>
                ) : (
                    messages.map((message, index) => <Message key={`${message.role}-${index}`} role={message.role} content={message.content} />)
                )}

                {loading && (
                    <div className="typing-indicator" aria-live="polite">
                        <span />
                        <span />
                        <span />
                    </div>
                )}
            </div>

            {sources.length > 0 && (
                <div className="sources-row">
                    {sources.map((source, index) => (
                        <span key={`${source.source || "source"}-${index}`} className="source-chip">
                            {source.source || `Source ${index + 1}`}
                        </span>
                    ))}
                </div>
            )}

            <form onSubmit={askQuestion} className="composer">
                <div className="composer-shell">
                    <textarea
                        value={question}
                        onChange={(event) => setQuestion(event.target.value)}
                        onKeyDown={handleKeyDown}
                        placeholder={collectionName ? "Ask a question about your document..." : "Upload a document to begin"}
                        disabled={!collectionName || loading}
                        rows={3}
                    />
                    <button type="submit" disabled={!collectionName || loading}>
                        {loading ? "Thinking..." : "Send"}
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

            {error && <div className="error-box">{error}</div>}
        </div>
    );
}