from fastapi import FastAPI
from pydantic import BaseModel
from rag_tester import RAGTester
import uvicorn

app = FastAPI()
tester = RAGTester()

class QueryRequest(BaseModel):
    text: str
    prompt_type: str = "custom"

@app.post("/query")
async def rag_query(request: QueryRequest):
    result = tester.test_queries([request.text], request.prompt_type)
    return {
        "answer": result[request.text]["answer"],
        "sources": result[request.text]["sources"]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
