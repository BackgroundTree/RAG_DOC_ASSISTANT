from fastapi import APIRouter, Request

from app.schemas.query import QueryRequest, QueryResponse
from app.services.generation import generate_answer_service
from app.services.retrieval import retrieval_service

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.post("/query", response_model=QueryResponse)
def query_rag(request: Request, payload: QueryRequest):
    client = request.app.state.chroma_client
    model = request.app.state.embed_model
    settings = request.app.state.settings

    context, sources = retrieval_service(
        query=payload.question,
        client=client,
        model=model,
        collection_name=settings.COLLECTION_NAME,
    )

    answer = generate_answer_service(
        query=payload.question,
        context=context,
        sources=sources,
        model_name=settings.OLLAMA_MODEL,
        base_url=settings.OLLAMA_BASE_URL,
    )

    return QueryResponse(answer=answer, sources=sources)