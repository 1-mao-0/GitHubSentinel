from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain import hub
from typing import List, Dict
import numpy as np

class RAGTester:
    def __init__(self, vector_db_path="vectorstore"):
        self.vector_db = FAISS.load_local(
            vector_db_path, 
            HuggingFaceEmbeddings(),
            allow_dangerous_deserialization=True
        )
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        
        # 定义三种提示词模板
        self.prompts = {
            "hub": hub.pull("langchain-ai/rag-prompt-default"),
            "custom": self._build_custom_prompt(),
            "technical": self._build_technical_prompt()
        }

    def _build_custom_prompt(self):
        return ChatPromptTemplate.from_template("""
        根据以下上下文回答问题：
        {context}
        
        要求：
        1. 答案必须来自上下文
        2. 包含相关代码片段（如适用）
        3. 不确定时回答"根据现有资料无法确定"
        
        问题：{question}
        """)

    def _build_technical_prompt(self):
        return ChatPromptTemplate.from_messages([
            ("system", "你是一个资深技术专家，回答需满足：\n"
                      "1. 使用Markdown格式\n"
                      "2. 关键术语附加英文原文\n"
                      "3. 提供参考资料页码"),
            ("human", "上下文：\n{context}\n\n问题：{question}")
        ])

    def test_queries(self, queries: List[str], prompt_type: str) -> Dict:
        """测试指定提示词模板"""
        chain = (
            {"context": self.vector_db.as_retriever(k=3), "question": RunnablePassthrough()}
            | self.prompts[prompt_type]
            | self.llm
            | StrOutputParser()
        )
        
        results = {}
        for query in queries:
            results[query] = {
                "answer": chain.invoke(query),
                "sources": [doc.metadata.get("source") for doc in self.vector_db.similarity_search(query)]
            }
        return results

    def evaluate(self, test_cases: Dict[str, str]) -> Dict:
        """评估不同模板效果"""
        metrics = {}
        for prompt_name in self.prompts:
            correct = 0
            total = len(test_cases)
            
            for query, expected in test_cases.items():
                result = self.test_queries([query], prompt_name)
                if expected.lower() in result[query]["answer"].lower():
                    correct += 1
            
            metrics[prompt_name] = {
                "accuracy": correct / total,
                "avg_sources": np.mean([
                    len(self.test_queries([q], prompt_name)[q]["sources"])
                    for q in test_cases
                ])
            }
        return metrics

if __name__ == "__main__":
    tester = RAGTester()
    
    # 测试问题集
    test_queries = [
        "LangChain中如何定义Chain？",
        "如何连接多个组件？", 
        "PDF报告中提到的技术如何与LangChain结合？"
    ]
    
    # 对比测试
    print("\n测试结果对比:")
    for prompt_type in ["hub", "custom", "technical"]:
        print(f"\n=== {prompt_type.upper()} 模板 ===")
        results = tester.test_queries(test_queries[:1], prompt_type)  # 测试第一个问题
        print(f"问题: {test_queries[0]}")
        print(f"回答: {results[test_queries[0]]['answer'][:200]}...")
        print(f"来源: {results[test_queries[0]]['sources']}")
    
    # 完整评估
    test_cases = {
        "LangChain中如何定义Chain？": "Chain是组件的序列化组合",
        "如何连接多个组件？": "使用Pipeline或SequentialChain"
    }
    print("\n评估报告:")
    print(tester.evaluate(test_cases))
