from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_elasticsearch import ElasticsearchStore
from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from elasticsearch import Elasticsearch
from load_fake_data import load_fake_data

# Initialize FastAPI app
app = FastAPI()

@app.on_event("startup")
def startup_event():
    es_client = Elasticsearch('http://elasticsearch:9200')
    try:
        if not es_client.indices.exists(index="products"):
            mapping = {
                "properties": {
                    "vector": {
                        "type": "dense_vector"
                    }
                }
            }
            es_client.indices.create(index="products", mappings=mapping)
    except Exception as e:
        print(e)

@app.post("/load-data")
def load_data_endpoint():
    try:
        load_fake_data()
        return {"message": "Fake data loaded successfully."}
    except Exception as e:
        return {"error": str(e)}

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Pydantic model for request body
class ChatRequest(BaseModel):
    prompt: str

# 1. Embedding Model
embeddings = OllamaEmbeddings(model="qwen3-embedding:0.6b", base_url="http://host.docker.internal:11434")

# 2. Elasticsearch Vector Store
vector_store = ElasticsearchStore(
    es_url="http://elasticsearch:9200",
    index_name="products",
    embedding=embeddings
)

# 3. LLM
llm = ChatOllama(model="ytagalar/trendyol-llm-7b-chat-dpo-v1.0-gguf", base_url="http://host.docker.internal:11434")

# 4. RAG Chain
retriever = vector_store.as_retriever()

prompt_template = """
Sen bir Trendyol asistanısın. Aşağıdaki bağlama göre kullanıcıya Türkçe olarak detaylı ve arkadaşça bir yanıt ver.
Eğer bir ürün bulunduysa, ürünün adını <product> tagleri arasına al.

Bağlam:
{context}

Soru: {question}
"""

prompt = ChatPromptTemplate.from_template(prompt_template)

# LangGraph State
class GraphState(TypedDict):
    question: str
    context: List[str]
    response: str

# LangGraph Nodes
def retrieve_documents(state):
    question = state["question"]
    documents = retriever.get_relevant_documents(question)
    return {"context": documents, "question": question}

def generate_response(state):
    question = state["question"]
    context = state["context"]
    
    runnable = prompt | llm | StrOutputParser()
    response = runnable.invoke({"context": context, "question": question})
    
    return {"response": response}

# LangGraph Edges
workflow = StateGraph(GraphState)

workflow.add_node("retrieve", retrieve_documents)
workflow.add_node("generate", generate_response)

workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", END)

app_graph = workflow.compile()

@app.post("/chat")
def chat(request: ChatRequest):
    try:
        inputs = {"question": request.prompt}
        result = app_graph.invoke(inputs)
        return {"response": result["response"]}
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def read_root():
    return FileResponse('static/index.html')
