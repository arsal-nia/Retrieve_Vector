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

        <div className={`message-container ${isUser ? "user-container" : "assistant-container"}`}>

            <div className={`message-header ${isUser ? "user-header" : "assistant-header"}`}>

                <div className={`avatar ${isUser ? "user-avatar" : "assistant-avatar"}`}>
                    {isUser ? "👤" : "🤖"}
                </div>

                <span className="message-author">
                    {isUser ? "You" : "Retrieve Vector"}
                </span>

            </div>

            <div className={`message-bubble ${isUser ? "user" : "assistant"}`}>
                <div className="message-content">
                    {isUser ? (
                        <p>{content}</p>
                    ) : (
                        <ReactMarkdown remarkPlugins={[remarkGfm]}>
                            {content}
                        </ReactMarkdown>
                    )}
                </div>
            </div>

        </div>

    </div>
);
}