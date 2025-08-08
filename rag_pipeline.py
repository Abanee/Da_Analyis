# import pandas as pd
# from llama_index.core import VectorStoreIndex, Document
# from llama_index.vector_stores.faiss import FaissVectorStore
# from llama_index.embeddings.huggingface import HuggingFaceEmbedding
# from llama_index.llms.ollama import Ollama
# import faiss

# class RAGPipeline:
#     def __init__(self):
#         try:
#             self.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/multi-qa-MiniLM-L6-cos-v1")
#             embed_dim = self.embed_model._model.get_sentence_embedding_dimension()
#             self.llm = Ollama(model="llama3.2", request_timeout=120.0)
#             self.vector_store = FaissVectorStore(faiss_index=faiss.IndexFlatL2(embed_dim))
#             self.index = None
#         except Exception as e:
#             raise RuntimeError(f"Failed to initialize RAGPipeline: {str(e)}")
#     def load_data(self, df, text):
#     # """Load DataFrame and text into the RAG pipeline."""
#         if not isinstance(df, pd.DataFrame) or df.empty:
#             raise ValueError("Invalid or empty DataFrame provided.")
#         if not isinstance(text, str) or not text.strip():
#             raise ValueError("Invalid or empty text provided.")
    
#         try:
#             df_text = df.to_string()
#             documents = [Document(text=df_text + "\n" + text)]
#             self.index = VectorStoreIndex.from_documents(
#                 documents,
#                 vector_store=self.vector_store,
#                 embed_model=self.embed_model
#             )
#         except Exception as e:
#             raise RuntimeError(f"Failed to load data into RAG pipeline: {str(e)}")


#     # def load_data(self, df, text):
#     #     """Load DataFrame and text into the RAG pipeline."""
#     #     if not isinstance(df, pd.DataFrame) or df.empty:
#     #         raise ValueError("Invalid or empty DataFrame provided.")
#     #     if not isinstance(text, str) or not text.strip():
#     #         raise ValueError("Invalid or empty text provided.")

#     #     try:
#     #         df_text = df.to_string()
#     #         documents = [Document(text=df_text + "\n" + text)]

#     #         self.index = VectorStoreIndex.from_documents(
#     #             documents,
#     #             vector_store=self.vector_store,
#     #             embed_model=self.embed_model
#     #         )
#     #     except Exception as e:
#     #         raise RuntimeError(f"Failed to load data into RAG pipeline: {str(e)}")
    

#     # def query(self, question):
#     #     """Query the RAG pipeline with a question."""
#     #     if not self.index:
#     #         return "No data loaded."
#     #     if not isinstance(question, str) or not question.strip():
#     #         raise ValueError("Invalid or empty question provided.")

#     #     try:
#     #         query_engine = self.index.as_query_engine(llm=self.llm)
#     #         response = query_engine.query(question)
#     #         return response.response
#     #     except Exception as e:
#     #         raise RuntimeError(f"Failed to process query: {str(e)}")

#     def query(self, question):
#     # """Query the RAG pipeline with a question."""
#         if not self.index:
#             return "No data loaded."
#         if not isinstance(question, str) or not question.strip():
#             raise ValueError("Invalid or empty question provided.")
    
#         try:
#             query_engine = self.index.as_query_engine(llm=self.llm)
#             response = query_engine.query(question)
#         # Safely access response, ignoring missing 'usage'
#             if hasattr(response, 'response'):
#                 return response.response
#             else:
#                 return str(response)  # Fallback to string conversion
#         except Exception as e:
#         # Log the error for debugging (optional but good practice)
#             print(f"Query error: {str(e)}")
#             raise RuntimeError(f"Failed to process query: {str(e)}")



# sencong pase
# import pandas as pd
# from llama_index.core import VectorStoreIndex, Document
# from llama_index.vector_stores.faiss import FaissVectorStore
# from llama_index.embeddings.huggingface import HuggingFaceEmbedding
# from llama_index.llms.ollama import Ollama
# import faiss

# class RAGPipeline:
#     def __init__(self):
#         try:
#             # Use a stable QA embedding
#             self.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/multi-qa-MiniLM-L6-cos-v1")
#             # Get embedding dimension from model
#             embed_dim = self.embed_model._model.get_sentence_embedding_dimension()
#             self.llm = Ollama(model="llama3.2", request_timeout=180.0)
#             self.vector_store = FaissVectorStore(faiss_index=faiss.IndexFlatL2(embed_dim))
#             self.index = None
#         except Exception as e:
#             raise RuntimeError(f"Failed to initialize RAGPipeline: {str(e)}")

#     def load_data(self, df, text):
#         # """Load DataFrame and text into the RAG pipeline."""
#         if not isinstance(df, pd.DataFrame) or df.empty:
#             raise ValueError("Invalid or empty DataFrame provided.")
#         if not isinstance(text, str) or not text.strip():
#             raise ValueError("Invalid or empty text provided.")

#         try:
#             df_text = df.to_string()
#             full_text = df_text + "\n" + text
#             documents = [Document(text=full_text)]
#             self.index = VectorStoreIndex.from_documents(
#                 documents,
#                 vector_store=self.vector_store,
#                 embed_model=self.embed_model
#             )
#         except Exception as e:
#             raise RuntimeError(f"Failed to load data into RAG pipeline: {str(e)}")

#     def query(self, question):
#         # """Query the RAG pipeline with a question."""
#         if not self.index:
#             return "No data loaded."
#         if not isinstance(question, str) or not question.strip():
#             raise ValueError("Invalid or empty question provided.")

#         try:
#             query_engine = self.index.as_query_engine(llm=self.llm)
#             response = query_engine.query(question)
#             # Safely return text regardless of response object shape
#             if hasattr(response, "response"):
#                 return response.response
#             return str(response)
#         except Exception as e:
#             # Don’t assume response.usage or other fields exist
#             raise RuntimeError(f"Failed to process query: {str(e)}")

# 3rd time rewrite the code
import pandas as pd
from llama_index.core import VectorStoreIndex, Document, Prompt
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
import faiss
import time

class RAGPipeline:
    def init(
        self,
        model_name: str = "llama3.2",
        embed_model_name: str = "sentence-transformers/multi-qa-MiniLM-L6-cos-v1",
        request_timeout: float = 300.0,
        similarity_top_k: int = 5,
        use_guided_prompt: bool = True,
        warmup: bool = False,
    ):
# """
# model_name: Ollama model to use
# embed_model_name: sentence-transformers embedding model
# request_timeout: Ollama request timeout in seconds
# similarity_top_k: how many retrieved chunks are passed to the LLM (lower is faster)
# use_guided_prompt: keep answers grounded in provided context
# warmup: send a tiny prompt to Ollama at init to reduce first-call latency
# """
        try:
            self.embed_model = HuggingFaceEmbedding(model_name=embed_model_name)
            embed_dim = self.embed_model._model.get_sentence_embedding_dimension()

            self.llm = Ollama(
                model=model_name,
                request_timeout=request_timeout,
            )
            self.vector_store = FaissVectorStore(faiss_index=faiss.IndexFlatL2(embed_dim))
            self.index = None
            self.similarity_top_k = similarity_top_k
            self.use_guided_prompt = use_guided_prompt

            if warmup:
                self._warmup_llm()
        except Exception as e:
            raise RuntimeError(f"Failed to initialize RAGPipeline: {str(e)}")

def _warmup_llm(self):
    try:
        _ = self.llm.complete("OK")
        time.sleep(0.3)
    except Exception:
        pass

def load_data(self, df: pd.DataFrame, text: str):
    """Load DataFrame and text into the RAG pipeline."""
    if not isinstance(df, pd.DataFrame) or df.empty:
        raise ValueError("Invalid or empty DataFrame provided.")
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Invalid or empty text provided.")

    try:
        df_text = df.to_string()
        full_text = df_text + "\n" + text
        documents = [Document(text=full_text)]
        self.index = VectorStoreIndex.from_documents(
            documents,
            vector_store=self.vector_store,
            embed_model=self.embed_model,
        )
    except Exception as e:
        raise RuntimeError(f"Failed to load data into RAG pipeline: {str(e)}")

def query(self, question: str):
    """Query the RAG pipeline with a question."""
    if not self.index:
        return "No data loaded."
    if not isinstance(question, str) or not question.strip():
        raise ValueError("Invalid or empty question provided.")

    try:
        if self.use_guided_prompt:
            qa_prompt = Prompt(
                "You are a data assistant. Use only the provided context to answer.\n"
                "If the answer cannot be found in the context, say so.\n\n"
                "Context:\n{context_str}\n\n"
                "Question: {query_str}\n\n"
                "Answer clearly with numbers and column names when relevant."
            )
            query_engine = self.index.as_query_engine(
                llm=self.llm,
                similarity_top_k=self.similarity_top_k,
                text_qa_template=qa_prompt,
            )
        else:
            query_engine = self.index.as_query_engine(
                llm=self.llm,
                similarity_top_k=self.similarity_top_k,
            )

        response = query_engine.query(question)

        if hasattr(response, "response") and isinstance(response.response, str):
            return response.response
        return str(response)

    except Exception as e:
        print(f"[RAG query error] {e}")
        raise RuntimeError(f"Failed to process query: {str(e)}")
