import requests
import json

def test_api():
    test_cases = [
        ("LangChain中如何定义Chain？", "custom"),
        ("如何实现文档问答？", "technical")
    ]
    
    for query, prompt_type in test_cases:
        response = requests.post(
            "http://localhost:8000/query",
            json={"text": query, "prompt_type": prompt_type}
        )
        result = response.json()
        
        print(f"\n问题: {query}")
        print(f"模板: {prompt_type}")
        print(f"回答: {result['answer'][:200]}...")
        print(f"来源: {result['sources']}")

if __name__ == "__main__":
    test_api()
