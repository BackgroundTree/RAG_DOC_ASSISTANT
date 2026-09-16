from contextlib import asynccontextmanager
import chromadb
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer

from app.api.routes.query import router as query_router
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.settings = settings
    app.state.chroma_client = chromadb.PersistentClient(
        path=settings.CHROMA_DB_DIR
    )
    app.state.embed_model = SentenceTransformer(settings.EMBEDDING_MODEL)
    yield


app = FastAPI(title="Yakuza 0 RAG API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query_router)