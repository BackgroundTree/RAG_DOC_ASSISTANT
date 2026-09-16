import chromadb
from sentence_transformers import SentenceTransformer


def retrieval_service(
    query: str,
    client: chromadb.ClientAPI,
    model: SentenceTransformer,
    collection_name: str,
    top_k: int = 6,
) -> tuple[str, list[str]]:
    collection = client.get_or_create_collection(name=collection_name)
    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding], n_results=top_k
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    context_blocks = []
    sources = []

    for doc, meta in zip(documents, metadatas):
        context_blocks.append(doc)
        if meta and "source" in meta:
            source_name = meta["source"]
            if source_name not in sources:
                sources.append(source_name)

    context_text = "\n\n".join(context_blocks)
    return context_text, sources