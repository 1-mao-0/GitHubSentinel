import os
from langchain_community.document_loaders import (
    WebBaseLoader, 
    PyPDFLoader,
    CSVLoader,
    UnstructuredMarkdownLoader
)
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

class VectorDBBuilder:
    def __init__(self, embedding_model="all-MiniLM-L6-v2"):
        self.embedding = HuggingFaceEmbeddings(
            model_name=embedding_model,
            model_kwargs={'device': 'cuda'} if torch.cuda.is_available() else {}
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

    def load_documents(self, sources):
        """支持混合数据源加载"""
        docs = []
        for source in sources:
            if source.startswith('http'):
                loader = WebBaseLoader(source)
            elif source.endswith('.pdf'):
                loader = PyPDFLoader(source)
            elif source.endswith('.csv'):
                loader = CSVLoader(source)
            elif source.endswith('.md'):
                loader = UnstructuredMarkdownLoader(source)
            docs.extend(loader.load())
        return self.text_splitter.split_documents(docs)

    def build_vectorstore(self, docs, save_path="vectorstore"):
        """构建并保存向量数据库"""
        vector_db = FAISS.from_documents(docs, self.embedding)
        vector_db.save_local(save_path)
        return vector_db

if __name__ == "__main__":
    builder = VectorDBBuilder()
    
    # 配置数据源
    sources = [
        "https://docs.langchain.com/docs/",
        "local_tech_report.pdf",
        "faq_records.csv"
    ]
    
    # 构建向量库
    docs = builder.load_documents(sources)
    vector_db = builder.build_vectorstore(docs)
    print(f"向量库已构建，包含 {len(docs)} 个文档块")
