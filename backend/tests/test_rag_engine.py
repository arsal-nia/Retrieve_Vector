from services.rag_engine import RagEngineService


def test_retrieve_relevant_context_returns_empty_when_collection_missing():
    service = RagEngineService()
    context, metadata = service.retrieve_relevant_context(
        "What is in this document?",
        "missing_collection",
    )

    assert context == ""
    assert metadata == []
