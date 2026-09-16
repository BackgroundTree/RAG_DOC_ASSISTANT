import ollama


def generate_answer_service(
    query: str,
    context: str,
    sources: list[str],
    model_name: str,
    base_url: str,
) -> str:
    client = ollama.Client(host=base_url)

    sources_str = ", ".join(sources) if sources else "None"
    system_prompt = (
        "You are an expert gaming assistant specializing in Yakuza 0. "
        "Answer the user's question using ONLY the provided context below. "
        "If the information is not contained in the context, state that you do not know. "
        "Always cite the source files if relevant information was used."
    )

    user_content = (
        f"Context:\n{context}\n\n"
        f"Sources:\n{sources_str}\n\n"
        f"Question: {query}"
    )

    response = client.chat(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
    )

    return response["message"]["content"]