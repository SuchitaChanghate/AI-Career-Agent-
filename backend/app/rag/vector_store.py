import chromadb


# Create a persistent Chroma database
client = chromadb.PersistentClient(
    path="chroma_db"
)


# Create or load the resume collection
collection = client.get_or_create_collection(
    name="resume"
)


def store_resume(chunks):
    """
    Store resume chunks inside Chroma.
    """

    ids = [
        f"resume_{i}"
        for i in range(len(chunks))
    ]

    collection.upsert(
        documents=chunks,
        ids=ids
    )

    return len(chunks)


def search_resume(
    query: str,
    top_k: int = 5
):
    """
    Search the resume for information
    relevant to the user's question.
    """

    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )

    documents = results.get(
        "documents",
        [[]]
    )[0]

    return documents