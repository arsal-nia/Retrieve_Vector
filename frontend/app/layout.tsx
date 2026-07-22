/**
 * ==========================================================
 * layout.tsx
 * ----------------------------------------------------------
 * Root layout for the AI RAG Assistant application.
 * This layout is applied to every page.
 * ==========================================================
 */

import type { Metadata } from "next";

import "./globals.css";

export const metadata: Metadata = {

    title: "AI RAG Assistant",

    description:
        "Retrieval-Augmented Generation Assistant using FastAPI, ChromaDB, Sentence Transformers, and Gemma 3.",

};

interface RootLayoutProps {

    children: React.ReactNode;

}

export default function RootLayout({

    children,

}: RootLayoutProps) {

    return (

        <html lang="en">

            <body>

                {children}

            </body>

        </html>

    );

}