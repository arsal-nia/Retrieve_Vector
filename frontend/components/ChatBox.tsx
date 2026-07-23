"use client";

/**
 * ==========================================================
 * ChatBox.tsx
 * ----------------------------------------------------------
 * Main chat interface for communicating with the
 * backend RAG engine.
 * ==========================================================
 */

import { useState } from "react";
import { apiClient, SourceMetadata } from "@/lib/api-client";
import Message from "./Message";

interface ChatBoxProps {
    collectionName: string;
}

interface ChatMessage {
    role: "user" | "assistant";
    content: string;
}

export default function ChatBox({
    collectionName,
}: ChatBoxProps) {

    const [question, setQuestion] = useState("");

    const [messages, setMessages] = useState<ChatMessage[]>([]);

    const [sources, setSources] = useState<SourceMetadata[]>([]);

    const [loading, setLoading] = useState(false);

    const [error, setError] = useState("");

    // ======================================================
    // Send Question
    // ======================================================

    async function askQuestion() {

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

        setMessages((previous) => [

            ...previous,

            userMessage,

        ]);

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

            setMessages((previous) => [

                ...previous,

                assistantMessage,

            ]);

            setSources(response.sources);

        }

        catch (err: any) {

            setError(

                err.message ||

                "Unable to contact backend."

            );

        }

        finally {

            setLoading(false);

        }

    }

    // ======================================================
    // Enter Key Support
    // ======================================================

    function handleKeyDown(

        event: React.KeyboardEvent<HTMLInputElement>

    ) {

        if (

            event.key === "Enter" &&

            !loading

        ) {

            askQuestion();

        }

    }
        // ======================================================
    // UI
    // ======================================================

    return (

        <div

            style={{

                border: "1px solid #d1d5db",

                borderRadius: "10px",

                padding: "20px",

                backgroundColor: "#ffffff"

            }}

        >

            <h2>

                AI Chat

            </h2>

            <p>

                Ask questions about your uploaded document.

            </p>

            {

                !collectionName && (

                    <div

                        style={{

                            color: "#dc2626",

                            marginBottom: "15px"

                        }}

                    >

                        Upload a document before chatting.

                    </div>

                )

            }

            <div

                style={{

                    height: "400px",

                    overflowY: "auto",

                    border: "1px solid #e5e7eb",

                    borderRadius: "8px",

                    padding: "15px",

                    marginBottom: "20px",

                    backgroundColor: "#f9fafb"

                }}

            >

                {

                    messages.length === 0 ? (

                        <p

                            style={{

                                color: "#6b7280"

                            }}

                        >

                            No conversation yet.

                        </p>

                    ) : (

                        messages.map(

                            (

                                message,

                                index

                            ) => (

                                <Message

                                    key={index}

                                    role={message.role}

                                    content={message.content}

                                />

                            )

                        )

                    )

                }

                {

                    loading && (

                        <div

                            style={{

                                color: "#2563eb",

                                fontStyle: "italic"

                            }}

                        >

                            AI is generating a response...

                        </div>

                    )

                }

            </div>

            <div

                style={{

                    display: "flex",

                    gap: "10px"

                }}

            >

                <input

                    type="text"

                    value={question}

                    placeholder={

                        collectionName

                            ? "Ask a question..."

                            : "Upload a document to begin..."

                    }

                    onChange={(event) =>

                        setQuestion(

                            event.target.value

                        )

                    }

                    onKeyDown={handleKeyDown}

                    style={{

                        flex: 1,

                        padding: "10px",

                        borderRadius: "8px",

                        border: "1px solid #d1d5db"

                    }}

                    disabled={!collectionName || loading}

                />

                <button

                    onClick={askQuestion}

                    disabled={!collectionName || loading}

                >

                    {

                        loading

                            ? "Sending..."

                            : "Send"

                    }

                </button>

            </div>
                        {

                error && (

                    <div

                        style={{

                            marginTop: "15px",

                            color: "#dc2626",

                            fontWeight: "bold"

                        }}

                    >

                        {error}

                    </div>

                )

            }

            {

                sources.length > 0 && (

                    <div

                        style={{

                            marginTop: "25px",

                            borderTop: "1px solid #e5e7eb",

                            paddingTop: "15px"

                        }}

                    >

                        <h3>

                            Retrieved Sources

                        </h3>

                        {

                            sources.map(

                                (

                                    source,

                                    index

                                ) => (

                                    <div

                                        key={index}

                                        style={{

                                            marginBottom: "10px",

                                            padding: "10px",

                                            border: "1px solid #d1d5db",

                                            borderRadius: "6px",

                                            backgroundColor: "#f9fafb"

                                        }}

                                    >

                                        <strong>

                                            Source {index + 1}

                                        </strong>

                                        <br />

                                        {

                                            Object.entries(source).map(

                                                (

                                                    [key, value]

                                                ) => (

                                                    <div

                                                        key={key}

                                                    >

                                                        <strong>

                                                            {key}:

                                                        </strong>{" "}

                                                        {String(value)}

                                                    </div>

                                                )

                                            )

                                        }

                                    </div>

                                )

                            )

                        }

                    </div>

                )

            }

        </div>

    );

}