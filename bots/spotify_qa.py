from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA

from .prompts import QA_PROMPT_TEMPLATE

class SpotifyQA():
    def __init__(self, base_url: str, model: str, index_path: str, k: int):
        self.prompt_template = QA_PROMPT_TEMPLATE
        self.llm = Ollama(
            base_url=base_url,
            model=model
        )
        self.embedding_model = OllamaEmbeddings(
            base_url=base_url,
            model=model
        )
        self.db_vectorestore = FAISS.load_local(
            index_path, 
            self.embedding_model
        )
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type='stuff',
            retriever=self.db_vectorestore.as_retriever(search_kwargs={'k': k}),
            return_source_documents=True,
            chain_type_kwargs={'prompt': self.prompt_template}
        )

    def generate_answer(self, query: str):
        response = self.qa_chain({"query": query})
        return response