# Retrieve Vector

> A Retrieval-Augmented Generation (RAG) based AI Assistant that enables users to interact with uploaded documents through intelligent question answering while maintaining conversational context.

# Repository Overview

| Property | Value |
|-----------|-------|
| Project Name | Retrieve Vector |
| Project Type | Retrieval-Augmented Generation (RAG) |
| Frontend | Next.js + React |
| Backend | FastAPI |
| Language Model | Google Gemini |
| Vector Database | ChromaDB |
| Embedding Model | Sentence Transformers |
| Programming Languages | Python, TypeScript |
| Database | SQLite |
| Document Formats | PDF, DOCX |

# Table Of Contents
-  [Project Overview](#project-overview)
-  [Installation Guide](#installation-guide)
-  [User Guide](#user-guide)
-  [System Architecture](#system-architecture)
-  [Technology Stack](#technology-stack)
-  [API Overview](#api-overview)

## Project Overview

Retrieve Vector is a full-stack AI-powered document assistant that combines Large Language Models (LLMs) with Retrieval-Augmented Generation (RAG) to provide accurate, context-aware answers from user-uploaded documents.

Instead of relying solely on an AI model's pre-trained knowledge, the system first retrieves the most relevant information from the uploaded document using semantic search. The retrieved content is then supplied as context to the language model, allowing it to generate responses that are grounded in the document rather than producing generic or fabricated answers.

The application is designed to simplify document exploration by enabling users to upload supported files, ask natural language questions, and receive precise answers based only on the document's contents.

In addition to document-based question answering, the system maintains chat history, allowing users to revisit previous conversations without losing context.





## Home Screen

![Home Screen](../screenshots/home-page.png)

## Upload Document

![Upload Document](../screenshots/upload-document.png)

## Chat

![Chat](../screenshots/chat.png)

## Chat History

![Chat History](../screenshots/chat-history.png)
---
## Problem Statement

Reading lengthy documents to locate specific information can be time-consuming and inefficient.

Traditional keyword search often fails to understand the user's intent, requiring users to manually browse through multiple pages to find relevant content.

Retrieve Vector addresses this challenge by combining semantic document retrieval with modern language models, allowing users to ask questions in plain English and receive concise, context-aware answers directly extracted from the uploaded document.

---

## Objectives

The project aims to:

- Build an intelligent document question-answering assistant.
- Implement Retrieval-Augmented Generation (RAG) for grounded responses.
- Allow users to upload documents and query their contents.
- Retrieve only the most relevant document sections before generating answers.
- Maintain conversation history for a better user experience.
- Provide an intuitive chat-based interface for document interaction.

---

## Core Features

-  Upload supported documents.
-  Semantic search over document contents.
-  AI-powered question answering using Retrieval-Augmented Generation (RAG).
-  Interactive chat interface.
-  Persistent chat history.
-  Fast document retrieval using vector embeddings.
-  Context-aware responses generated only from uploaded documents.
-  Modern and responsive user interface.

---

# Technology Stack

Retrieve Vector is built using a modern full-stack architecture that combines an intuitive frontend with a scalable backend and an AI-powered Retrieval-Augmented Generation (RAG) pipeline.

| Layer | Technology | Purpose |
|--------|------------|---------|
| Frontend | Next.js, React.js, TypeScript | Interactive user interface |
| Backend | FastAPI (Python) | REST API development |
| AI Framework | LangChain | RAG orchestration |
| Language Model | Google Gemini | Answer generation |
| Embeddings | Sentence Transformers | Convert text into vector embeddings |
| Vector Database | ChromaDB | Store and retrieve document embeddings |
| Document Processing | PyMuPDF, python-docx | Extract text from uploaded documents |
| Database | SQLite | Store chat history and metadata |
| Styling | CSS | User Interface styling |

---

# System Architecture

The application follows a client-server architecture where the frontend communicates with the backend through REST APIs. The backend processes uploaded documents, generates embeddings, retrieves relevant information from the vector database, and sends contextual information to the language model before returning the final response.

```text
                 ┌────────────────────────────┐
                 │        Frontend            │
                 │  (Next.js + React.js)      │
                 └─────────────┬──────────────┘
                               │
                          REST API Calls
                               │
                               ▼
                 ┌────────────────────────────┐
                 │     FastAPI Backend        │
                 └─────────────┬──────────────┘
                               │
         ┌─────────────────────┼──────────────────────┐
         │                     │                      │
         ▼                     ▼                      ▼
 Document Processing     Vector Database       Chat History
 (Parsing & Chunking)      (ChromaDB)           (SQLite)

                               │
                               ▼
                      Relevant Context
                               │
                               ▼
                      Google Gemini LLM
                               │
                               ▼
                     Generated Response
                               │
                               ▼
                           Frontend
```

---

# Project Workflow

The following workflow illustrates how the system processes every uploaded document and user query.

```text
Upload Document
        │
        ▼
Extract Text
        │
        ▼
Split into Chunks
        │
        ▼
Generate Embeddings
        │
        ▼
Store in ChromaDB
        │
        ▼
Document Ready
        │
        ▼
User Asks Question
        │
        ▼
Convert Question to Embedding
        │
        ▼
Similarity Search
        │
        ▼
Retrieve Relevant Chunks
        │
        ▼
Send Context + Question to Gemini
        │
        ▼
Generate Final Answer
        │
        ▼
Display Response
        │
        ▼
Save Chat History
```

---

# How Retrieval-Augmented Generation (RAG) Works

Retrieve Vector uses a Retrieval-Augmented Generation (RAG) pipeline to ensure responses are based on the uploaded document instead of relying solely on the language model's pre-trained knowledge.

The workflow consists of the following stages:

### Step 1 — Document Upload

The user uploads a supported document through the application interface.

Supported document types include:

- PDF
- DOCX

After upload, the backend receives the file and prepares it for processing.

---

### Step 2 — Document Parsing

The backend extracts all readable text from the uploaded document.

At this stage:

- Images are ignored.
- Formatting is removed.
- Raw text is extracted.

The extracted text becomes the knowledge source for the remainder of the pipeline.

---

### Step 3 — Text Chunking

Instead of processing the entire document at once, the extracted content is divided into smaller overlapping chunks.

Chunking improves:

- Retrieval accuracy
- Embedding quality
- Response relevance
- Processing efficiency

Each chunk represents a small section of the document.

---

### Step 4 — Embedding Generation

Every chunk is converted into a numerical vector (embedding).

These embeddings capture the semantic meaning of the text rather than exact keywords, enabling similarity-based retrieval.

---

### Step 5 — Vector Storage

The generated embeddings are stored inside ChromaDB.

Each stored vector maintains a reference to its original document chunk, allowing the system to retrieve the relevant source text when answering questions.

---

### Step 6 — User Query Processing

When the user submits a question, the query is also converted into an embedding using the same embedding model.

This ensures that both the document chunks and the user's question exist in the same semantic vector space.

---

### Step 7 — Similarity Search

The query embedding is compared against all stored document embeddings.

The vector database identifies the chunks that are most semantically similar to the user's question.

Only the highest-ranking chunks are retrieved.

---

### Step 8 — Context Generation

The retrieved document chunks are combined with the user's question to create a contextual prompt.

This prompt provides the language model with only the information necessary to answer the question accurately.

---

### Step 9 — Answer Generation

Google Gemini receives:

- The user's question
- The retrieved document context

Using this information, it generates a natural language response that is grounded in the uploaded document.

---

### Step 10 — Response Delivery

The generated answer is returned to the frontend and displayed within the chat interface.

The conversation is also stored in the chat history, allowing users to revisit previous interactions later.

---
# Why Retrieval-Augmented Generation?

Traditional AI chatbots rely primarily on pre-trained knowledge, which can lead to inaccurate or fabricated responses when answering questions about specific documents.

Retrieve Vector uses a Retrieval-Augmented Generation (RAG) pipeline to overcome this limitation.

| Traditional Chatbot | Retrieve Vector |
|---------------------|-----------------|
| Relies on model memory | Retrieves relevant document content first |
| May hallucinate information | Grounds answers in uploaded documents |
| Generic responses | Context-aware responses |
| No document understanding | Semantic understanding of uploaded files |
| Cannot cite uploaded content | Uses retrieved document chunks as context |


# Project Structure

The project follows a modular architecture that separates the frontend, backend, document processing pipeline, vector storage, and AI services. This structure improves maintainability, scalability, and readability while keeping different responsibilities isolated.

```text
Retrieve_Vector/
│
├── backend/
│   ├── routers/
│   │   ├── chat.py
│   │   └── documents.py
│   │
│   ├── services/
│   │   ├── embeddings.py
│   │   ├── rag_engine.py
│   │   ├── vector_store.py
│   │   ├── document_parser.py
│   │   ├── external_apis.py
│   │   ├── scraper.py
│   │   └── youtube.py
│   │
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── app/
│   ├── components/
│   └── lib/
│
├── docker-compose.yml
├── README.md
└── LICENSE
```

---

# Directory Breakdown

## Backend

The backend is developed using **FastAPI** and contains all business logic related to document processing, retrieval, response generation, and API communication.

### `routers/`

Contains all REST API endpoints responsible for handling incoming requests from the frontend.

Current responsibilities include:

- Chat endpoints
- Document upload endpoints

---

### `services/`

This directory contains the core logic of the application.

#### `rag_engine.py`

Acts as the central orchestration layer.

Responsibilities include:

- Processing user questions
- Retrieving relevant document chunks
- Building prompts
- Calling the language model
- Returning final responses

---

#### `embeddings.py`

Responsible for converting document chunks into vector embeddings before storing them inside the vector database.

---

#### `vector_store.py`

Handles all interactions with ChromaDB including:

- Saving embeddings
- Searching vectors
- Returning the most relevant document chunks

---

#### `document_parser.py`

Processes uploaded documents.

Responsibilities include:

- Reading PDF files
- Reading DOCX files
- Extracting text
- Preparing content for chunking

---

#### `external_apis.py`

Contains functionality related to external information retrieval.

This service can be extended to integrate third-party knowledge sources when required.

---

#### `scraper.py`

Provides a fallback mechanism for collecting information through web scraping if external services are unavailable.

---

#### `youtube.py`

Designed to manage video recommendations related to user queries.

---

### `main.py`

The application entry point.

Responsible for:

- Creating the FastAPI application
- Registering routers
- Configuring middleware
- Starting the server

---

## Frontend

The frontend is built using **Next.js** and provides the complete user interface.

It manages:

- Chat interface
- Document uploads
- Chat history
- User interactions
- API communication

---

### `app/`

Contains application pages and routing.

---

### `components/`

Reusable UI components including:

- Chat window
- Message bubbles
- Upload controls
- Sidebar
- Buttons
- Forms

---

### `lib/`

Contains helper utilities responsible for communicating with backend APIs.

---

# Installation Guide

Follow the steps below to set up the project on your local machine.

## Step 1 — Clone the Repository

```bash
git clone <repository-url>
```

```bash
cd Retrieve_Vector
```

---

## Step 2 — Create a Virtual Environment

Windows

```bash
python -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv
```

Activate

```bash
source venv/bin/activate
```

---

## Step 3 — Install Backend Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 4 — Install Frontend Dependencies

```bash
cd frontend
```

```bash
npm install
```

or

```bash
yarn install
```

---

# Environment Variables

Create a `.env` file inside the backend directory.

Example:

```env
GEMINI_API_KEY=YOUR_API_KEY

CHROMA_DB_PATH=./chroma_db

DATABASE_URL=sqlite:///chat_history.db
```

> **Note:** Replace the placeholder values with your own credentials before running the application.

---

# Running the Application

## Start the Backend

```bash
uvicorn main:app --reload
```

The backend server will start at:

```
http://127.0.0.1:8000
```

---

## Start the Frontend

```bash
npm run dev
```

The frontend will start at:

```
http://localhost:3000
```

---

# Verifying the Installation

After both servers are running:

- Open the frontend in your browser.
- Upload a supported document.
- Wait until processing is complete.
- Ask a question related to the uploaded document.
- Verify that the response is generated successfully.
- Open the chat history to ensure conversations are being stored.

If all of these steps complete successfully, the application has been configured correctly and is ready for use.

---



# User Guide

This section explains how to use Retrieve Vector from a user's perspective. The workflow is designed to be simple and intuitive, allowing users to upload a document and immediately begin interacting with it through natural language.

---

### Step 1 — Launch the Application

After starting both the frontend and backend servers, open the application in your browser.

```
http://localhost:3000
```

The home page presents a clean chat interface where users can upload documents and start asking questions.

---







### Step 2 — Upload a Document

Click the **Upload Document** button and choose a supported document from your local machine.

Supported formats include:

- PDF (.pdf)
- Microsoft Word (.docx)

After the upload is complete, the backend automatically begins processing the document.

During processing, the system:

- Extracts the document text
- Splits the text into smaller chunks
- Generates vector embeddings
- Stores the embeddings inside ChromaDB

Once processing finishes, the document becomes available for question answering.

---


### Step 3 — Ask Questions

After the document has been indexed, users can ask questions in natural language through the chat interface.

Example questions include:

- What is the main topic of this document?
- Summarize the introduction.
- Explain the methodology.
- What conclusions were reached?
- List the important points discussed.

The system searches only the uploaded document and generates responses based on the retrieved content.


---

### Step 4 — View AI Responses

For every question submitted, the application performs semantic retrieval before generating an answer.

The response displayed in the chat is based on the most relevant sections of the uploaded document rather than general AI knowledge.

This approach improves response accuracy and reduces the likelihood of hallucinated information.

---




### Step 5 — Continue the Conversation

Users can continue asking follow-up questions without needing to upload the document again.

Because the conversation remains associated with the uploaded document, subsequent questions continue to retrieve information from the same knowledge base.

This enables users to explore documents naturally through multi-turn conversations.

---

### Step 6 — Access Chat History

All conversations are stored for future reference.

Users can revisit previous chats from the chat history panel without losing the context of earlier interactions.

This allows documents to be explored over multiple sessions without restarting the conversation.

---


# Complete Working of the System

The following section explains the complete internal execution flow whenever a user uploads a document and asks a question.

## Phase 1 — Document Processing

```
User Uploads Document
          │
          ▼
Backend Receives File
          │
          ▼
Document Parser Extracts Text
          │
          ▼
Clean Text
          │
          ▼
Split into Chunks
          │
          ▼
Generate Embeddings
          │
          ▼
Store in ChromaDB
          │
          ▼
Document Ready
```

---

## Phase 2 — Question Answering

```
User Sends Question
          │
          ▼
Convert Question into Embedding
          │
          ▼
Search ChromaDB
          │
          ▼
Retrieve Most Relevant Chunks
          │
          ▼
Build Context Prompt
          │
          ▼
Send Context + Question to Gemini
          │
          ▼
Generate Final Response
          │
          ▼
Display Answer
          │
          ▼
Save Conversation
```

---

# API Overview

The backend exposes RESTful endpoints that connect the frontend with the RAG pipeline.

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/chat` | POST | Processes user questions and returns AI responses |
| `/upload-document` | POST | Uploads and processes supported documents |
| `/chat-history` | GET | Retrieves previous conversations |

> *Note:* The available endpoints shown above are based on the architecture documents you provided. If your implemented project exposes different routes, update this table to match your actual API.

---


# Future Enhancements

Future versions of Retrieve Vector may include:

- Multi-document conversations
- Support for additional file formats
- Source citations for every generated response
- Streaming AI responses
- User authentication
- Cloud deployment
- Role-based access
- Document summarization
- OCR support for scanned PDFs
- Export chat history

# Acknowledgements

This project was built using the following open-source technologies:

- FastAPI
- Next.js
- React
- LangChain
- ChromaDB
- Sentence Transformers
- Google Gemini
- PyMuPDF
- python-docx

# Author

- **Muhammad Arsal**
- **Ameema Iman**

BS Data Science

COMSATS University Islamabad

GitHub: https://github.com/arsal-nia/Retrieve_Vector
