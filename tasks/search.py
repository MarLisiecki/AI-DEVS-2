import json
import os

import requests
import qdrant_client
from solver.solver import Solver
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.qdrant import Qdrant

UNKNOWN_NEWSLETTER_URL = "https://unknow.news/archiwum.json"


def temp_qdrant_handler(question):
    client = qdrant_client.QdrantClient(
        url="http://localhost:6333/",
    )
    os.environ["QDRANT_COLLECTION"] = "unknown-newsletter"

    collection_config = qdrant_client.http.models.VectorParams(
        size=1536,  # 768 for instructor-xl, 1536 for OpenAI
        distance=qdrant_client.http.models.Distance.COSINE,
    )

    client.recreate_collection(
        collection_name=os.getenv("QDRANT_COLLECTION"), vectors_config=collection_config
    )
    print(client.get_collections())
    embeddings = OpenAIEmbeddings()

    vectorstore = Qdrant(
        client=client, collection_name="unknown-newsletter", embeddings=embeddings
    )

    def get_chunks():
        chunks = []
        with open("newsletter.json") as f:
            raw_text = json.loads(f.read())
            for element in raw_text:
                tmp = ""
                tmp += (
                    "Title: "
                    + element["title"]
                    + " Url: "
                    + element["url"]
                    + " Info: "
                    + element["info"]
                )
                chunks.append(tmp)
            print(chunks[0:3])
        return chunks[0:301]

    # get_chunks()

    texts = get_chunks()

    vectorstore.add_texts(texts)

    from langchain.chains import RetrievalQA
    from langchain.llms import OpenAI

    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(), chain_type="stuff", retriever=vectorstore.as_retriever()
    )

    query = "Which url can help answering the question: {question}".format(
        question=question
    )
    response = qa.run(query)

    return response


def search(input_data: dict) -> dict:
    print(input_data)
    get_newsletter(UNKNOWN_NEWSLETTER_URL)
    url = temp_qdrant_handler(question=input_data["question"])
    prepared_answer = {"answer": url.strip()}
    return prepared_answer


def get_newsletter(url: str) -> None:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    with open("newsletter.json", mode="w", encoding="utf-8") as file:
        content = json.dumps(response.json())
        file.write(content)


if __name__ == "__main__":
    # TODO REFACTOR
    sol = Solver("search")
    sol.solve(search)
