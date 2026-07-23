"""
rag_engine.py
------------------------
Central orchestration engine for the RAG pipeline. Coordinates text embedding,
semantic vector searching, context formatting, and LLM text generation.
"""

import os
import logging
from typing import List, Dict, Any, Tuple
from openai import OpenAI
from .embeddings import embedding_service
from .vector_store import VectorStoreService

logger = logging.getLogger(__name__)

class RagEngineService:
    """
    Service responsible for orchestrating the Retrieval-Augmented Generation pipeline.
    Connects query embeddings to vector storage retrieval to assemble context payloads and invoke LLMs.
    """

    def __init__(self) -> None:
        """Initializes the engine, hooks into the underlying Vector Store, and prepares local environment parameters."""
        self.vector_store = VectorStoreService()
        
        # Updated based on Docker Model Runner specifications
        # Using host.docker.internal to bridge the container to the host network
        self.local_url = os.getenv("LOCAL_LLM_URL", "http://host.docker.internal:12434/engines/llama.cpp/v1/")
        
        # Updated to match the exact model name shown in Docker Desktop Models UI
        self.model_name = os.getenv("LOCAL_MODEL_NAME", "docker.io/ai/gemma3-qat:latest")
        
        logger.info(f"RagEngineService initialized. Target Local Engine: {self.local_url} | Model: {self.model_name}")

    def retrieve_relevant_context(
        self, 
        query: str, 
        collection_name: str, 
        top_k: int = 4,
        similarity_threshold: float = 0.7
    ) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Orchestrates the retrieval leg of the RAG pipeline.
        Vectorizes the incoming query, queries the DB, filters results, and builds context.
        """
        if not query.strip():
            return "", []

        logger.info(f"Processing query through RAG pipeline for collection: '{collection_name}'")

        try:
            # 1. Convert the plain text query into a vector array
            query_vector = embedding_service.embed_query(query)
            
            # 2. Execute similarity search via the vector database wrapper
            search_results = self.vector_store.query_similarity(
                collection_name=collection_name,
                query_embeddings=[query_vector],
                top_k=top_k
            )

            # Safeguard against completely empty database responses
            if not search_results or not search_results.get("documents") or not search_results["documents"][0]:
                logger.info(f"No semantic context found in collection '{collection_name}' for query.")
                return "", []

            retrieved_docs: List[str] = search_results["documents"][0]
            retrieved_metadatas: List[Dict[str, Any]] = search_results.get("metadatas", [[]])[0]
            
            context_chunks: List[str] = []
            source_metadata: List[Dict[str, Any]] = []

            for idx, doc in enumerate(retrieved_docs):
                context_chunks.append(doc)
                if idx < len(retrieved_metadatas) and retrieved_metadatas[idx]:
                    source_metadata.append(retrieved_metadatas[idx])
                else:
                    source_metadata.append({"source": "unknown_chunk", "index": idx})

            # 3. Flatten the isolated text chunks into a unified context block
            formatted_context = "\n\n---\n\n".join(context_chunks)
            logger.info(f"Successfully compiled {len(context_chunks)} source chunks into context payload.")
            
            return formatted_context, source_metadata

        except Exception as e:
            logger.error(f"Critical execution failure inside RAG orchestrator: {str(e)}")
            return "", []

    def construct_augmented_prompt(self, query: str, context: str) -> List[Dict[str, str]]:
        """Synthesizes raw context fragments and user inquiries into an LLM system prompt template."""
        system_instruction = (
            "You are an expert, domain-specific AI assistant. Use the provided context fragments "
            "to answer the user's question accurately and objectively. If the answer cannot be found "
            "within the context, rely gracefully on your broader system knowledge or clarify what is missing."
        )
        
        user_payload = f"Context Information:\n{context}\n\nUser Question: {query}"
        
        return [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_payload}
        ]

    def generate_answer(self, query: str, collection_name: str) -> Dict[str, Any]:
        """
        Complete end-to-end RAG lifecycle loop execution.
        Extracts contextual document segments, constructs prompts, and routes them to Gemma 3.
        """
        # 1. Fetch matching factual data blocks from local vector database
        context, metadata = self.retrieve_relevant_context(query, collection_name)
        
        # 2. Build structured message schemas
        messages = self.construct_augmented_prompt(query, context)
        
        try:
            logger.info(f"Routing structured RAG prompt directly to local container engine model: {self.model_name}")
            
            # 3. Connect to the OpenAI-compatible endpoint running inside Docker Desktop
            client = OpenAI(
                base_url=self.local_url,
                api_key="anything"  # Matches the implementation shown in image_cff1e2.jpg
            )
            
            response = client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.3
            )
            
            answer = response.choices[0].message.content
            logger.info("Generation loop completed successfully. Returning compiled payload.")
            
            return {
                "answer": answer,
                "sources": metadata,
                "context_retrieved": bool(context)
            }
            
        except Exception as e:
            logger.error(f"Execution runtime error when communicating with local container LLM: {str(e)}")
            return {
                "answer": f"Retrieval executed perfectly, but generating the answer failed. (Is your Docker container model running?): {str(e)}",
                "sources": metadata,
                "context_retrieved": bool(context)
            }

# Global service instance instantiation ready for import in routers
rag_engine = RagEngineService()