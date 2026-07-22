"use client";

/**
 * ==========================================================
 * Sidebar.tsx
 * ----------------------------------------------------------
 * Sidebar component displaying project information,
 * backend status, and the currently loaded collection.
 * ==========================================================
 */

import { useEffect, useState } from "react";
import { apiClient } from "@/lib/api-client";

interface SidebarProps {

    collectionName: string;

}

export default function Sidebar({

    collectionName

}: SidebarProps) {

    const [backendStatus, setBackendStatus] = useState("Checking...");

    const [statusColor, setStatusColor] = useState("#f59e0b");

    // ======================================================
    // Check Backend Status
    // ======================================================

    useEffect(() => {

        async function checkBackend() {

            try {

                await apiClient.healthCheck();

                setBackendStatus("Online");

                setStatusColor("#16a34a");

            }

            catch {

                setBackendStatus("Offline");

                setStatusColor("#dc2626");

            }

        }

        checkBackend();

    }, []);

    return (

        <aside

            style={{

                width: "280px",

                padding: "20px",

                borderRight: "1px solid #d1d5db",

                backgroundColor: "#f8fafc",

                minHeight: "100vh"

            }}

        >

            <h2>

                AI RAG Assistant

            </h2>

            <hr />

            <h3>

                Backend Status

            </h3>

            <p

                style={{

                    color: statusColor,

                    fontWeight: "bold"

                }}

            >

                {backendStatus}

            </p>

            <hr />

            <h3>

                Active Collection

            </h3>

            {

                collectionName ? (

                    <p>

                        {collectionName}

                    </p>

                ) : (

                    <p>

                        No document uploaded.

                    </p>

                )

            }

            <hr />

            <h3>

                Features

            </h3>

            <ul>

                <li>Document Upload</li>

                <li>Semantic Search</li>

                <li>Vector Database</li>

                <li>Gemma 3 Integration</li>

                <li>Retrieval-Augmented Generation</li>

            </ul>

        </aside>

    );

}