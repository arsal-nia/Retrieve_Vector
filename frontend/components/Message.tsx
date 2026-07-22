"use client";

/**
 * ==========================================================
 * Message.tsx
 * ----------------------------------------------------------
 * Reusable component for displaying a single chat message.
 * It supports both user and AI assistant messages.
 * ==========================================================
 */

interface MessageProps {

    role: "user" | "assistant";

    content: string;

}

export default function Message({

    role,

    content

}: MessageProps) {

    const isUser = role === "user";

    return (

        <div

            style={{

                display: "flex",

                justifyContent: isUser
                    ? "flex-end"
                    : "flex-start",

                marginBottom: "15px"

            }}

        >

            <div

                style={{

                    maxWidth: "75%",

                    padding: "12px",

                    borderRadius: "10px",

                    backgroundColor: isUser
                        ? "#2563eb"
                        : "#e5e7eb",

                    color: isUser
                        ? "#ffffff"
                        : "#111827",

                    whiteSpace: "pre-wrap",

                    wordBreak: "break-word",

                    boxShadow:
                        "0px 2px 6px rgba(0,0,0,0.15)"

                }}

            >

                <div

                    style={{

                        fontWeight: "bold",

                        marginBottom: "6px"

                    }}

                >

                    {isUser ? "You" : "AI Assistant"}

                </div>

                <div>

                    {content}

                </div>

            </div>

        </div>

    );

}