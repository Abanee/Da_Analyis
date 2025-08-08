import pandas as pd
from llama_index.core import VectorStoreIndex, Document
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
import faiss

class RAGPipeline:
    def __init__(self):
        try:
            self.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/multi-qa-MiniLM-L6-cos-v1")
            embed_dim = self.embed_model._model.get_sentence_embedding_dimension()
            self.llm = Ollama(model="llama3.2", request_timeout=120.0)
            self.vector_store = FaissVectorStore(faiss_index=faiss.IndexFlatL2(embed_dim))
            self.index = None
        except Exception as e:
            raise RuntimeError(f"Failed to initialize RAGPipeline: {str(e)}")
    def load_data(self, df, text):
    # """Load DataFrame and text into the RAG pipeline."""
        if not isinstance(df, pd.DataFrame) or df.empty:
            raise ValueError("Invalid or empty DataFrame provided.")
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Invalid or empty text provided.")
    
        try:
            df_text = df.to_string()
            documents = [Document(text=df_text + "\n" + text)]
            self.index = VectorStoreIndex.from_documents(
                documents,
                vector_store=self.vector_store,
                embed_model=self.embed_model
            )
        except Exception as e:
            raise RuntimeError(f"Failed to load data into RAG pipeline: {str(e)}")


    # def load_data(self, df, text):
    #     """Load DataFrame and text into the RAG pipeline."""
    #     if not isinstance(df, pd.DataFrame) or df.empty:
    #         raise ValueError("Invalid or empty DataFrame provided.")
    #     if not isinstance(text, str) or not text.strip():
    #         raise ValueError("Invalid or empty text provided.")

    #     try:
    #         df_text = df.to_string()
    #         documents = [Document(text=df_text + "\n" + text)]

    #         self.index = VectorStoreIndex.from_documents(
    #             documents,
    #             vector_store=self.vector_store,
    #             embed_model=self.embed_model
    #         )
    #     except Exception as e:
    #         raise RuntimeError(f"Failed to load data into RAG pipeline: {str(e)}")
    

    # def query(self, question):
    #     """Query the RAG pipeline with a question."""
    #     if not self.index:
    #         return "No data loaded."
    #     if not isinstance(question, str) or not question.strip():
    #         raise ValueError("Invalid or empty question provided.")

    #     try:
    #         query_engine = self.index.as_query_engine(llm=self.llm)
    #         response = query_engine.query(question)
    #         return response.response
    #     except Exception as e:
    #         raise RuntimeError(f"Failed to process query: {str(e)}")

    def query(self, question):
    # """Query the RAG pipeline with a question."""
        if not self.index:
            return "No data loaded."
        if not isinstance(question, str) or not question.strip():
            raise ValueError("Invalid or empty question provided.")
    
        try:
            query_engine = self.index.as_query_engine(llm=self.llm)
            response = query_engine.query(question)
        # Safely access response, ignoring missing 'usage'
            if hasattr(response, 'response'):
                return response.response
            else:
                return str(response)  # Fallback to string conversion
        except Exception as e:
        # Log the error for debugging (optional but good practice)
            print(f"Query error: {str(e)}")
            raise RuntimeError(f"Failed to process query: {str(e)}")

