import chromadb

def createCollection(texts):
    chroma_client = chromadb.Client()
    collection = chroma_client.create_collection(name="resumes")
    ids=[]
    metadata=[]
    for i in range(len(texts)):
        ids.append(str(i+1))
        metadata.append({"source":"resume"+str(i+1)})
    collection.add(
        documents=texts,
        metadatas=metadata,
        ids=ids
    )

    return collection