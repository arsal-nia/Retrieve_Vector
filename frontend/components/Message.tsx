"use client";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface MessageProps {
    role: "user" | "assistant";
    content: string;
}

export default function Message({ role, content }: MessageProps) {
    const isUser = role === "user";

    return (
        <div className={`message-row ${isUser ? "is-user" : "is-assistant"}`}>
            <div className={`message-bubble ${isUser ? "user" : "assistant"}`}>
                <div className="message-meta">{isUser ? "You" : "Assistant"}</div>
                <div className="message-content">
                    {isUser ? (
                        <div>{content}</div>
                    ) : (
                        <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
                    )}
                </div>
            </div>
        </div>
    );
}